import datetime
import icalendar
import requests

from domain.entities.schedule import ScheduleEntity
from domain.entities.subject import SubjectEntity
from domain.services.schedule import ScheduleService
from domain.values.week_kind import WeekKindEnum


class ScheduleServiceImpl(ScheduleService):
    url = "https://schedule-of.mirea.ru/schedule/api/search?limit=15&match=%s"
    def __init__(self, group: str):
        self.url = self.url % group
        
    def _get_schedule_ical_url(self) -> str:
        ical = requests.get(self.url).json()
        
        return ical["data"][0]["iCalLink"]

    def get_schedule(self) -> tuple[ScheduleEntity, ScheduleEntity]:
        ical = requests.get(self._get_schedule_ical_url()).content

        calendar = icalendar.Calendar.from_ical(ical)

        subjects_odd = []
        subjects_even = []

        for i, event in enumerate(calendar.walk("VEVENT")):
            if not isinstance(event.get("DTSTART").dt, datetime.datetime):
                continue

            subject = SubjectEntity(
                name=str(event.get("SUMMARY")),
                time_start=event.get("DTSTART").dt.time(),
                time_end=event.get("DTEND").dt.time(),
                location=str(event.get("LOCATION")),
                day=int(event.get("DTSTART").dt.day)
            )

            if subject.day >= 10 and subject.day <= 15:
                subjects_odd.append(subject)
            else:
                subjects_even.append(subject)

        return (
            ScheduleEntity(
                week=WeekKindEnum.odd,
                subjects=subjects_odd,
            ),
            ScheduleEntity(
                week=WeekKindEnum.even,
                subjects=subjects_even,
            )
        )