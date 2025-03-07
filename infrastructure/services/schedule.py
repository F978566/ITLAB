import datetime
import icalendar
import requests

from domain.entities.schedule import ScheduleEntity
from domain.entities.subject import SubjectEntity
from domain.services.schedule import ScheduleService
from domain.values.week_kind import WeekKindEnum


class ScheduleServiceImpl(ScheduleService):
    def __init__(self, url: str):
        self.url = url

    def get_schedule(self):
        ical = requests.get(self.url).content

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

            if i % 2 == 1:
                subjects_odd.append(subject)
            else:
                subjects_even.append(subject)

            print(
                event.get("DTSTART").dt.day,
                event.get("DTSTART").dt.time(),
                " - ",
                event.get("DTEND").dt.time(),
                event.get("SUMMARY"),
                event.get("LOCATION"),
            )

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