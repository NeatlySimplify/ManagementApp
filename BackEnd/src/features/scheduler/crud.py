from dataclasses import asdict
from datetime import date, time
from uuid import UUID

from src.dependencies import db
from src.features.generics.crud import _create_details, _delete_details
from src.features.generics.schema import CreateDictType, UpdateDictType
from src.queries.schedule import (
    CreateSchedule_async_edgeql,
    DeleteSchedule_async_edgeql,
    GetSchedule_async_edgeql,
    UpdateSchdeule_async_edgeql,
)


@db.handle_database_errors
async def createEvent(
        db,
        user_id: UUID,
        origin: UUID | None,
        type: str,
        name: str,
        status: bool | None,
        date: date,
        beginning_time: time | None,
        ending_time: time | None,
        details: list[CreateDictType] | None
    ) -> dict | None:
    result = await CreateSchedule_async_edgeql.CreateSchedule(
        db,
        user=user_id,
        origin=origin,
        type=type,
        name=name,
        status=status,
        date=date,
        beginning_time=beginning_time,
        ending_time=ending_time,
    )
    if result is not None:
        result = asdict(result)
        id = result["id"]
        if details is not None:
            for data in details:
                print("From the loop inside CRUD createEvent")
                print(data, id)
                result_detail = await _create_details(db, title=data.title, field=data.field, origin=id)
                print(result_detail)
    return result


@db.handle_database_errors
async def updateEvent(
        db,
        event_id: UUID,
        name: str | None,
        status: bool | None,
        type: str | None,
        date: date | None,
        beginning_time: time | None,
        ending_time: time | None,
        details: UpdateDictType | None,
    ) -> dict | None:
    result = await UpdateSchdeule_async_edgeql.UpdateSchdeule(
        db,
        name=name,
        type=type,
        id=event_id,
        status=status,
        date=date,
        beginning_time=beginning_time,
        ending_time=ending_time,
    )
    if result is not None:
        result = asdict(result)
        id = result["id"]
        if details is not None and details.change:
            await _delete_details(db, origin=id)
            for data in details.body:
                print("From the loop inside CRUD updateEvent")
                print(data, id)
                result_detail = await _create_details(db, title=data.title, field=data.field, origin=id)
                print(result_detail)


    return result


async def getEvent(db, event_id: UUID) -> dict | None:
    result: GetSchedule_async_edgeql.GetScheduleResult | None = await GetSchedule_async_edgeql.GetSchedule(db, id=event_id)
    if result is None:
        return None
    result_dict = asdict(result)
    return result_dict


async def deleteEvent(db, event_id: UUID) -> DeleteSchedule_async_edgeql.DeleteScheduleResult | None:
    return await DeleteSchedule_async_edgeql.DeleteSchedule(db, event=event_id)
