from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.dependencies.auth import get_current_user
from src.dependencies.response_decorator import handle_result
from src.features.record.crud import (
    getRecord,
    createRecord,
    updateRecord,
    deleteRecord,
    linkEvent,
    linkEntity,
    linkMovement,
    unlinkEvent,
    unlinkEntity,
    unlinkMovement
)
from src.features.record.schema import (
    RecordCreate,
    RecordUpdate,
    ModelID
)

recordRoute = APIRouter(prefix='/api/record')


@recordRoute.get('/', response_class=JSONResponse)
@handle_result()
async def get_record(
        record: ModelID,
        user = Depends(get_current_user)
    ):
    return await getRecord(record.id)


@recordRoute.post('/', response_class=JSONResponse)
@handle_result()
async def create_record(
        entity: ModelID,
        data: RecordCreate,
        user = Depends(get_current_user)
    ):
    return await createRecord(
        user=user,
        name=data.name,
        id_service=data.id_service,
        active=data.active,
        status=data.status,
        type=data.type,
        value=data.value,
        details=data.details,
        entity=entity.id
    )


@recordRoute.put('/', response_class=JSONResponse)
async def update_record(data: RecordUpdate, user = Depends(get_current_user)):
    return await updateRecord(
        id=data.id,
        name=data.name,
        id_service=data.id_service,
        active=data.active,
        status=data.status,
        type=data.type,
        value=data.value,
        details=data.details
    )


@recordRoute.delete('/', response_class=JSONResponse)
@handle_result()
async def delete_record(record: ModelID, user = Depends(get_current_user)):
    return await deleteRecord(record.id)


@recordRoute.put('/event/add', response_class=JSONResponse)
@handle_result()
async def link_event(record: ModelID, event: ModelID,user = Depends(get_current_user)):
    return await linkEvent(schedule=event.id, record=record.id)


@recordRoute.put('/event/remove', response_class=JSONResponse)
@handle_result()
async def unlink_event(record: ModelID, event: ModelID,user = Depends(get_current_user)):
    return await unlinkEvent(schedule=event.id, record=record.id)


@recordRoute.put('/entity/add', response_class=JSONResponse)
@handle_result()
async def link_entity(record: ModelID, entity: ModelID,user = Depends(get_current_user)):
    return await linkEntity(entity=entity.id, record=record.id)


@recordRoute.put('/entity/remove', response_class=JSONResponse)
@handle_result()
async def unlink_entity(record: ModelID, entity: ModelID,user = Depends(get_current_user)):
    return await unlinkEntity(entity=entity.id, record=record.id)


@recordRoute.put('/movement/add', response_class=JSONResponse)
@handle_result()
async def link_movement(record: ModelID, movement: ModelID,user = Depends(get_current_user)):
    return await linkMovement(movement=movement.id, record=record.id)


@recordRoute.put('/movement/remove', response_class=JSONResponse)
@handle_result()
async def unlink_movement(record: ModelID, movement: ModelID,user = Depends(get_current_user)):
    return await unlinkMovement(movement=movement.id, record=record.id)
