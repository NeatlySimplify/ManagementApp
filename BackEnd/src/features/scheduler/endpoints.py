from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.dependencies.auth import get_current_user
from src.dependencies.response_decorator import handle_result
from src.features.scheduler.schema import (
    SchedulerUpdate,
    SchedulerCreate,
    ModelID
)
from src.features.scheduler.crud import getEvent, updateEvent, deleteEvent, createEvent


eventRoute = APIRouter(prefix='/api/scheduler')


@eventRoute.get('/', response_class=JSONResponse)
@handle_result()
async def getScheduler(data: ModelID, user=Depends(get_current_user)):
    return await getEvent(data.id)


@eventRoute.post('/', response_class=JSONResponse)
@handle_result()
async def createScheduler(data: SchedulerCreate, user=Depends(get_current_user)):
    return await createEvent(
        user_id=user,
        origin=data.origin,
        type=data.type,
        name=data.name,
        status=data.status,
        date=data.date,
        beginning_time=data.beginning_time,
        ending_time=data.ending_time,
        details=data.details
    )


@eventRoute.put('/', response_class=JSONResponse)
@handle_result()
async def updateScheduler(data: SchedulerUpdate, user=Depends(get_current_user)):
    return await updateEvent(
        name=data.name,
        type=data.type,
        event_id=data.id,
        status=data.status,
        beginning_time=data.beginning_time,
        ending_time=data.ending_time,
        date=data.date,
        details=data.details
    )


@eventRoute.delete('/', response_class=JSONResponse)
@handle_result()
async def deleteScheduler(data: ModelID, user=Depends(get_current_user)):
    return await deleteEvent(data.id)
