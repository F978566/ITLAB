from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.problem import ProblemEntity
from domain.entities.problem_list import ProblemListEntity
from domain.entities.week_schedule import WeekScheduleEntity
from domain.repositories.full_title import FullTitleRepository
from domain.repositories.problems import ProblemsRepository
from domain.repositories.schedule import ScheduleRepository
from domain.repositories.title import TitleRepository
from infrastructure.db.models.models import FullTitleModel, ProblemModel, TitleModel


class ScheduleProblemsService:
    def __init__(
        self,
        schedule_repository: ScheduleRepository,
        title_repository: TitleRepository,
        full_title_repository: FullTitleRepository,
        problems_repository: ProblemsRepository,
    ):
        self.schedule_repository = schedule_repository
        self.problems: dict[str, ProblemListEntity] = {}
        self.title_repository = title_repository
        self.full_title_repository = full_title_repository
        self.problems_repository = problems_repository
        self.title = ""

    async def _save_to_db(self, db: AsyncSession):
        title = TitleModel(
            title=self.title if self.title != "" else "empty",
        )
        db.add(title)

        await db.commit()

        for full_title_problems in self.problems.keys():
            full_title = FullTitleModel(
                full_title=full_title_problems, title_id=title.id
            )
            db.add(full_title)
            await db.commit()
            for problem in self.problems[full_title_problems].problems:
                pr = ProblemModel(
                    title_id=full_title.id,
                    name=problem.name,
                    description=problem.description,
                )
                db.add(pr)

        await db.commit()

    async def _get_from_db(self, title: str, db: AsyncSession):
        title_model = await self.title_repository.get_title_by_name(title, db)
        # print(title_model.oid)
        full_title_list = await self.full_title_repository.get_full_titles(title_model.oid, db)

        for full_title in full_title_list:
            self.problems[full_title.title] = ProblemListEntity(
                full_group_title=full_title.title,
                problems=(await self.problems_repository.get_problems(full_title.oid, db)),
            )

    async def find_problems(self, db: AsyncSession):
        if await self.title_repository.check_title_exist(
            self.title if self.title != "" else "empty", db
        ):
            await self._get_from_db(self.title if self.title != "" else "empty", db)
            return

        schedule_list = self.schedule_repository.get_schedule_list(self.title)
        for schedule in schedule_list:
            self.big_workload_differences(schedule)
            for week_schedule in schedule:
                self.long_commute(week_schedule)
                self.late_start(week_schedule)

        await self._save_to_db(db)

    def big_workload_differences(
        self, schedule: tuple[WeekScheduleEntity, WeekScheduleEntity]
    ):
        odd_differences = self.workload_differences(schedule[0])
        even_differences = self.workload_differences(schedule[1])

        problems_list = ProblemListEntity(
            problems=[], full_group_title=schedule[0].full_group_title
        )

        if odd_differences >= 4 or even_differences >= 4:
            problems_list.problems.append(
                ProblemEntity(
                    name="Big workload difference",
                    description=f"The differences between the busiest and the least busy day in one week is {odd_differences} classes",
                    full_group_title=schedule[0].full_group_title,
                )
            )

        if problems_list.full_group_title in self.problems:
            self.problems[problems_list.full_group_title].problems.extend(
                problems_list.problems
            )
        else:
            self.problems[problems_list.full_group_title] = problems_list

    def workload_differences(self, week_schedule: WeekScheduleEntity):
        max_classes = 0
        min_classes = 1_000_000
        day_schedule = {}

        for day in week_schedule.schedule:
            for schedule in day.subjects:
                if schedule.day in day_schedule:
                    day_schedule[schedule.day] += 1
                else:
                    day_schedule[schedule.day] = 1

        for schedule in day_schedule:
            max_classes = max(max_classes, day_schedule[schedule])
            min_classes = min(min_classes, day_schedule[schedule])

        return max_classes - min_classes

    def long_commute(self, week_schedule: WeekScheduleEntity):
        get_auditorium = lambda x: x.split("-")[0]
        time_difference = lambda x, y: abs(
            x.hour * 60 + x.minute - x.hour * 60 - y.minute
        )

        problems_list = ProblemListEntity(
            problems=[], full_group_title=week_schedule.full_group_title
        )

        for day in week_schedule.schedule:
            if len(day.subjects) <= 1:
                continue

            prev_subject = day.subjects[0]
            for subject in day.subjects[1:]:
                if (
                    all([subject.location != "None", prev_subject.location != "None"])
                    and get_auditorium(subject.location)
                    != get_auditorium(prev_subject.location)
                    and time_difference(subject.time_start, prev_subject.time_end) <= 10
                ):
                    problems_list.problems.append(
                        ProblemEntity(
                            name="Long commute",
                            description=f"A student may be late for their next class if they have to walk from {prev_subject.location} to {subject.location} in 10 minute day - {day.day_of_week.name} week - {week_schedule.week.name}",
                            full_group_title=week_schedule.full_group_title,
                        )
                    )
                prev_subject = subject

        if problems_list.full_group_title in self.problems:
            self.problems[problems_list.full_group_title].problems.extend(
                problems_list.problems
            )
        else:
            self.problems[problems_list.full_group_title] = problems_list

    def late_start(self, week_schedule: WeekScheduleEntity):
        problems_list = ProblemListEntity(
            problems=[], full_group_title=week_schedule.full_group_title
        )

        for day in week_schedule.schedule:
            if len(day.subjects) == 0:
                continue

            first_class = sorted(day.subjects, key=lambda x: x.time_start.hour)[0]
            if first_class.time_start.hour > 12:
                problems_list.problems.append(
                    ProblemEntity(
                        name="Late start",
                        description=f"It is better to start the day earlier than at {first_class.time_start.hour} in the morning - {day.day_of_week.name} week - {week_schedule.week.name}",
                        full_group_title=week_schedule.full_group_title,
                    )
                )

        if problems_list.full_group_title in self.problems:
            self.problems[problems_list.full_group_title].problems.extend(
                problems_list.problems
            )
        else:
            self.problems[problems_list.full_group_title] = problems_list
