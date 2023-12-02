import datetime
from typing import List
import uuid
from models.location import Location


from models.reports import Report

__reports: List[Report] = []


async def get_reports() -> List:
    # Would be an async data call here.
    return list(__reports)


async def add_report(description: str, location: Location) -> Report:
    now = datetime.datetime.now()
    report = Report(
        id=str(uuid.uuid4()),
        location=location,
        description=description,
        created_date=now,
    )

    # Simulate saving to the db.
    # Would be an async data call here.
    __reports.append(report)

    __reports.sort(key=lambda r: r.created_date, reverse=True)

    return report
