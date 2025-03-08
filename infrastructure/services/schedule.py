import datetime
import icalendar
import requests

from domain.entities.day_schedule import DayScheduleEntity
from domain.entities.week_schedule import WeekScheduleEntity
from domain.entities.subject import SubjectEntity
from domain.services.schedule import ScheduleService
from domain.values.day import DayEnum
from domain.values.week_kind import WeekKindEnum


class ScheduleServiceImpl(ScheduleService):
    url = "https://schedule-of.mirea.ru/schedule/api/search?limit=15&match=%s"

    def __init__(self, group: str):
        self.url = self.url % group

    def _get_schedule_ical_url(self) -> str:
        ical = requests.get(self.url).json()

        return ical["data"][0]["iCalLink"]

    def get_schedule(self) -> tuple[WeekScheduleEntity, WeekScheduleEntity]:
        ical = requests.get(self._get_schedule_ical_url()).content

        calendar = icalendar.Calendar.from_ical(ical)

        subjects_odd = [DayScheduleEntity(day_of_week=DayEnum(x + 1), subjects=[]) for x in range(6)]
        subjects_even = [DayScheduleEntity(day_of_week=DayEnum(x + 1), subjects=[]) for x in range(6)]

        times_start = []

        for event in calendar.walk("VEVENT"):
            if not isinstance(event.get("DTSTART").dt, datetime.datetime):
                continue

            if event.get("DTSTART") in times_start:
                continue

            times_start.append(event.get("DTSTART"))

            subject = SubjectEntity(
                name=str(event.get("SUMMARY")),
                time_start=event.get("DTSTART").dt.time(),
                time_end=event.get("DTEND").dt.time(),
                location=str(event.get("LOCATION")),
                day=int(event.get("DTSTART").dt.day),
            )

            if subject.day >= 10 and subject.day <= 15:
                subjects_odd[subject.day - 10].subjects.append(subject)
            else:
                subjects_even[subject.day - 17].subjects.append(subject)

        return (
            WeekScheduleEntity(
                week=WeekKindEnum.odd,
                schedule=subjects_odd,
            ),
            WeekScheduleEntity(
                week=WeekKindEnum.even,
                schedule=subjects_even,
            ),
        )
