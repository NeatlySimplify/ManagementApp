from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.dependencies.auth import get_current_user
from src.dependencies.db import get_gel_client
from src.dependencies.response_decorator import handle_result
from src.features.record.crud import (
    createRecord,
    deleteRecord,
    getRecord,
    linkEntity,
    linkEvent,
    linkMovement,
    unlinkEntity,
    unlinkEvent,
    unlinkMovement,
    updateRecord,
)
from src.features.record.schema import (
    RecordCreate,
    RecordUpdate,
)

recordRoute = APIRouter(prefix='/api/record')


@recordRoute.get('/{id}', response_class=JSONResponse)
@handle_result()
async def get_record(
        id: UUID,
        user = Depends(get_current_user),
        db=Depends(get_gel_client)
    ):
    return await getRecord(db, id)


@recordRoute.post('/', response_class=JSONResponse)
@handle_result()
async def create_record(
        data: RecordCreate,
        user = Depends(get_current_user),
        db=Depends(get_gel_client)
    ):
    return await createRecord(
        db,
        user=user,
        name=data.name,
        id_service=data.id_service,
        active=data.active,
        status=data.status,
        type=data.type_record,
        value=data.value,
        details=data.notes,
        entity=data.entity
    )


@recordRoute.put('/', response_class=JSONResponse)
async def update_record(data: RecordUpdate, user = Depends(get_current_user), db=Depends(get_gel_client)):
    return await updateRecord(
        db,
        id=data.id,
        name=data.name,
        id_service=data.id_service,
        active=data.active,
        status=data.status,
        type=data.type_record,
        value=data.value,
        details=data.notes
    )


@recordRoute.delete('/{id}', response_class=JSONResponse)
@handle_result()
async def delete_record(id: UUID, user = Depends(get_current_user), db=Depends(get_gel_client)):
    return await deleteRecord(db, id)


@recordRoute.put('/{id}/add-event/', response_class=JSONResponse)
@handle_result()
async def link_event(event: UUID, id: UUID, user = Depends(get_current_user), db=Depends(get_gel_client)):
    return await linkEvent(db, schedule=event, record=id)


@recordRoute.put('/{id}/del-event/', response_class=JSONResponse)
@handle_result()
async def unlink_event(event: UUID, id: UUID, user=Depends(get_current_user), db=Depends(get_gel_client)):
    return await unlinkEvent(db, schedule=event, record=id)


@recordRoute.put('/{id}/add-entity/', response_class=JSONResponse)
@handle_result()
async def link_entity(entity: UUID, id: UUID, user = Depends(get_current_user), db=Depends(get_gel_client)):
    return await linkEntity(db, entity=entity, record=id)


@recordRoute.put('/{id}/del-entity/', response_class=JSONResponse)
@handle_result()
async def unlink_entity(entity: UUID, id: UUID, user = Depends(get_current_user), db=Depends(get_gel_client)):
    return await unlinkEntity(db, entity=entity, record=id)


@recordRoute.put('/{id}/add-movement/', response_class=JSONResponse)
@handle_result()
async def link_movement(movement: UUID, id: UUID, user = Depends(get_current_user), db=Depends(get_gel_client)):
    return await linkMovement(db, movement=movement, record=id)

@recordRoute.put('/{id}/del-movement/', response_class=JSONResponse)
@handle_result()
async def unlink_movement(movement: UUID, id: UUID, user = Depends(get_current_user), db=Depends(get_gel_client)):
    return await unlinkMovement(db ,movement=movement, record=id)
