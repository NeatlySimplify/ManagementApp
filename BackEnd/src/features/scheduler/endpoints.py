from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.dependencies.auth import get_current_user
from src.dependencies.db import get_gel_client
from src.dependencies.response_decorator import handle_result
from src.features.scheduler.crud import createEvent, deleteEvent, getEvent, updateEvent
from src.features.scheduler.schema import (
    SchedulerCreate,
    SchedulerUpdate,
)

eventRoute = APIRouter(prefix='/api/scheduler')


@eventRoute.get('/{schedule}', response_class=JSONResponse)
@handle_result()
async def getScheduler(
    schedule: UUID,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await getEvent(db, schedule)


@eventRoute.post('/', response_class=JSONResponse)
@handle_result()
async def createScheduler(
    data: SchedulerCreate,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await createEvent(
        db,
        type_tag=data.type_tag,
        name=data.name,
        status=data.status,
        date=data.date,
        beginning_time=data.beginning_time,
        ending_time=data.ending_time,
        details=data.notes
    )


@eventRoute.put('/', response_class=JSONResponse)
@handle_result()
async def updateScheduler(
    data: SchedulerUpdate,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await updateEvent(
        db,
        name=data.name,
        type_tag=data.type_tag,
        event_id=data.id,
        status=data.status,
        beginning_time=data.beginning_time,
        ending_time=data.ending_time,
        date=data.date,
        details=data.notes
    )


@eventRoute.delete('/{schedule}', response_class=JSONResponse)
@handle_result()
async def deleteScheduler(
    schedule: UUID,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await deleteEvent(db, schedule)
