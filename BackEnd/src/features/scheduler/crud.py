import json
from dataclasses import asdict
from datetime import datetime
from uuid import UUID

from src.dependencies import db
from src.queries.schedule import (
    CreateSchedule_async_edgeql,
    DeleteSchedule_async_edgeql,
    GetSchedule_async_edgeql,
    UpdateSchdeule_async_edgeql,
)


@db.handle_database_errors
async def createEvent(
        db,
        type_tag: str,
        name: str,
        status: bool | None,
        date: datetime,
        ending_time: datetime | None,
        details: dict[str, str | int | float] | None
) -> dict | None:
    result = await CreateSchedule_async_edgeql.CreateSchedule(
        db,
        type_tag=type_tag,
        name=name,
        status=status,
        date=date,
        ending_time=ending_time,
        notes=json.dumps(details) if details is not None else None
    )
    if result is not None:
        result = asdict(result)
    return result


@db.handle_database_errors
async def updateEvent(
        db,
        event_id: UUID,
        name: str | None,
        status: bool | None,
        type_tag: str | None,
        date: datetime | None,
        ending_time: datetime | None,
        details: dict[str, str | int | float] | None,
    ) -> dict | None:
    result = await UpdateSchdeule_async_edgeql.UpdateSchdeule(
        db,
        name=name,
        type_tag=type_tag,
        id=event_id,
        status=status,
        date=date,
        ending_time=ending_time,
        notes=json.dumps(details) if details is not None else None,
    )
    if result is not None:
        result = asdict(result)
    return result


async def getEvent(db, event_id: UUID) -> dict | None:
    result: GetSchedule_async_edgeql.GetScheduleResult | None = (
        await GetSchedule_async_edgeql.GetSchedule(db, id=event_id)
    )
    if result is None:
        return None
    result_dict = asdict(result)
    if result_dict["notes"] is not None:
        result_dict["notes"] = json.loads(result_dict["notes"])
    return result_dict


async def deleteEvent(db, event_id: UUID) -> dict | None:
    result: DeleteSchedule_async_edgeql.DeleteScheduleResult | None = (
        await DeleteSchedule_async_edgeql.DeleteSchedule(db, event=event_id)
    )
    if result is None:
        return None
    return asdict(result)
