from datetime import date, time
from fastapi import Depends
from src.dependencies import db
from uuid import UUID
from src.queries.schedule import (
    CreateSchedule_async_edgeql,
    UpdateSchdeule_async_edgeql,
    GetSchedule_async_edgeql,
    DeleteSchedule_async_edgeql
)


@db.handle_database_errors
async def createEvent(
        user_id: UUID,
        origin: UUID | None,
        type: str,
        name: str,
        status: bool | None,
        date: date,
        beginning_time: time | None,
        ending_time: time | None,
        details: dict | None,
        db=Depends(db.get_gel_client)
    ) -> CreateSchedule_async_edgeql.CreateScheduleResult | None:
    return await CreateSchedule_async_edgeql.CreateSchedule(
        db,
        user=user_id,
        origin=origin,
        type=type,
        name=name,
        status=status,
        date=date,
        beginning_time=beginning_time,
        ending_time=ending_time,
        details=details
    )


@db.handle_database_errors
async def updateEvent(
        event_id: UUID,
        name: str | None,
        status: bool | None,
        type: str | None,
        date: date | None,
        beginning_time: time | None,
        ending_time: time | None,
        details: dict | None,
        db=Depends(db.get_gel_client)
    ) -> UpdateSchdeule_async_edgeql.UpdateSchdeuleResult | None:
    return await UpdateSchdeule_async_edgeql.UpdateSchdeule(
        db,
        name=name,
        type=type,
        id=event_id,
        status=status,
        date=date,
        beginning_time=beginning_time,
        ending_time=ending_time,
        details=details
    )


async def getEvent(event_id: UUID, db=Depends(db.get_gel_client)) -> GetSchedule_async_edgeql.GetScheduleResult | None:
    return await GetSchedule_async_edgeql.GetSchedule(db, id=event_id)


async def deleteEvent(event_id: UUID, db=Depends(db.get_gel_client)) -> DeleteSchedule_async_edgeql.DeleteScheduleResult | None:
    return await DeleteSchedule_async_edgeql.DeleteSchedule(db, event=event_id)
