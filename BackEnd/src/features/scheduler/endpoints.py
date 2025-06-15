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


@eventRoute.get('/{id}', response_class=JSONResponse)
@handle_result()
async def getScheduler(id: UUID, user=Depends(get_current_user), db=Depends(get_gel_client)):
    return await getEvent(db, id)


@eventRoute.post('/', response_class=JSONResponse)
@handle_result()
async def createScheduler(data: SchedulerCreate, user=Depends(get_current_user), db=Depends(get_gel_client)):
    return await createEvent(
        db,
        user_id=user,
        origin=data.origin,
        type=data.type_entry,
        name=data.name,
        status=data.status,
        date=data.date,
        beginning_time=data.beginning_time,
        ending_time=data.ending_time,
        details=data.notes
    )


@eventRoute.put('/', response_class=JSONResponse)
@handle_result()
async def updateScheduler(data: SchedulerUpdate, user=Depends(get_current_user), db=Depends(get_gel_client)):
    return await updateEvent(
        db,
        name=data.name,
        type=data.type_entry,
        event_id=data.id,
        status=data.status,
        beginning_time=data.beginning_time,
        ending_time=data.ending_time,
        date=data.date,
        details=data.notes
    )


@eventRoute.delete('/{id}', response_class=JSONResponse)
@handle_result()
async def deleteScheduler(id: UUID, user=Depends(get_current_user), db=Depends(get_gel_client)):
    return await deleteEvent(db, id)
