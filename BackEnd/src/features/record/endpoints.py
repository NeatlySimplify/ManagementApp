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


@recordRoute.get('/{record}', response_class=JSONResponse)
@handle_result()
async def get_record(
        record: UUID,
        user = Depends(get_current_user),
        db=Depends(get_gel_client)
    ):
    db = db.with_globals({"ext::auth::client_token": user})
    return await getRecord(db, record)


@recordRoute.post('/', response_class=JSONResponse)
@handle_result()
async def create_record(
        data: RecordCreate,
        user = Depends(get_current_user),
        db=Depends(get_gel_client)
):
    db = db.with_globals({"ext::auth::client_token": user})
    return await createRecord(
        db,
        name=data.name,
        id_service=data.service_id,
        active=data.status,
        status=data.optional_status,
        type_tag=data.type_tag,
        value=data.value,
        details=data.notes,
        entities=data.entities
    )


@recordRoute.put('/', response_class=JSONResponse)
async def update_record(
    data: RecordUpdate,
    user = Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"ext::auth::client_token": user})
    return await updateRecord(
        db,
        record=data.id,
        name=data.name,
        id_service=data.service_id,
        active=data.status,
        status=data.optional_status,
        type_tag=data.type_tag,
        value=data.value,
        details=data.notes
    )


@recordRoute.delete('/{record}', response_class=JSONResponse)
@handle_result()
async def delete_record(
    record: UUID,
    user = Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"ext::auth::client_token": user})
    return await deleteRecord(db, record)


@recordRoute.put('/{record}/add-event/', response_class=JSONResponse)
@handle_result()
async def link_event(
    event: UUID,
    record: UUID,
    user = Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"ext::auth::client_token": user})
    return await linkEvent(db, schedule=event, record=record)


@recordRoute.put('/{record}/del-event/', response_class=JSONResponse)
@handle_result()
async def unlink_event(
    event: UUID,
    record: UUID,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"ext::auth::client_token": user})
    return await unlinkEvent(db, schedule=event, record=record)


@recordRoute.put('/{record}/add-entity/', response_class=JSONResponse)
@handle_result()
async def link_entity(
    entity: UUID,
    record: UUID,
    user = Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"ext::auth::client_token": user})
    return await linkEntity(db, entity=entity, record=record)


@recordRoute.put('/{record}/del-entity/', response_class=JSONResponse)
@handle_result()
async def unlink_entity(
    entity: UUID,
    record: UUID,
    user = Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"ext::auth::client_token": user})
    return await unlinkEntity(db, entity=entity, record=record)


@recordRoute.put('/{record}/add-movement/', response_class=JSONResponse)
@handle_result()
async def link_movement(
    movement: UUID,
    record: UUID,
    user = Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"ext::auth::client_token": user})
    return await linkMovement(db, movement=movement, record=record)

@recordRoute.put('/{record}/del-movement/', response_class=JSONResponse)
@handle_result()
async def unlink_movement(
    movement: UUID,
    record: UUID,
    user = Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"ext::auth::client_token": user})
    return await unlinkMovement(db ,movement=movement, record=record)
