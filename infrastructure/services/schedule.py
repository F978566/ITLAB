import datetime
from typing import List
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
    default_url = "https://schedule-of.mirea.ru/schedule/api/search?limit=15&match="

    def _get_schedule_ical_url(self, title: str) -> str:
        self.url = self.url % title
        ical = requests.get(self.url).json()

        return ical["data"]
    
    def get_schedule_list(self, title: str) -> List[tuple[WeekScheduleEntity, WeekScheduleEntity]]:
        ical_data_list = self._get_schedule_ical_url(title)
        schedule_list = []
        
        for data in ical_data_list:
            schedule_list.append(self._get_schedule(data["iCalLink"]))
        
        return schedule_list

    def _get_schedule(self, schedule_url: str) -> tuple[WeekScheduleEntity, WeekScheduleEntity]:
        ical = requests.get(schedule_url).content

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
                full_group_title=calendar.get("X-WR-CALNAME")
            ),
            WeekScheduleEntity(
                week=WeekKindEnum.even,
                schedule=subjects_even,
                full_group_title=calendar.get("X-WR-CALNAME")
            ),
        )
