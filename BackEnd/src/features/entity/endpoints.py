from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.dependencies.auth import get_current_user
from src.dependencies.db import get_gel_client
from src.dependencies.response_decorator import handle_result
from src.features.entity.crud import (
    create_address,
    create_contact,
    create_entity,
    delete_address,
    delete_contact,
    delete_entity,
    get_entity,
    update_address,
    update_contact,
    update_entity,
)
from src.features.entity.schema import (
    AddressCreate,
    AddressUpdate,
    ContactCreate,
    ContactUpdate,
    EntityCreate,
    EntityUpdate,
)

entityRoute = APIRouter(prefix='/api/entity')


@entityRoute.get('/{entity}', response_class=JSONResponse)
@handle_result()
async def getEntity(
    entity: UUID,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await get_entity(db, entity=entity)


@entityRoute.post('/', response_class=JSONResponse)
@handle_result()
async def createEntity(
    entity: EntityCreate,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await create_entity(
        db,
        email=entity.email,
        type_tag=entity.type_tag,
        document=entity.document,
        name=entity.name,
        sex=entity.sex,
        relationship_status=entity.relationship_status,
        details=entity.notes,
        birth=entity.birth,
        status=entity.status,
        document_type=entity.document_type
    )


@entityRoute.put('/', response_class=JSONResponse)
@handle_result()
async def updateEntity(
    entity: EntityUpdate,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await update_entity(
        db,
        email=entity.email,
        type_tag=entity.type_tag,
        status=entity.status,
        document_type=entity.document_type,
        document=entity.document,
        name=entity.name,
        sex=entity.sex,
        relationship_status=entity.relationship_status,
        details=entity.notes,
        birth=entity.birth,
        entity=entity.id,
    )


@entityRoute.delete('/{entity}', response_class=JSONResponse)
@handle_result()
async def deleteEntity(
    entity: UUID,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user[0]})
    return await delete_entity(db, entity)


@entityRoute.post('/address', response_class=JSONResponse)
@handle_result()
async def createAddress(
    address: AddressCreate,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await create_address(
        db,
        address.entity,
        address.state,
        address.city,
        address.district,
        address.street,
        address.number,
        address.complement,
        address.postal,
    )


@entityRoute.put('/address', response_class=JSONResponse)
@handle_result()
async def updateAddress(
    address: AddressUpdate,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await update_address(
        db,
        address.id,
        address.state,
        address.city,
        address.district,
        address.street,
        address.number,
        address.complement,
        address.postal,
    )


@entityRoute.delete('/{entity}/address/', response_class=JSONResponse)
@handle_result()
async def deleteAddress(
    entity: UUID,
    address: UUID,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await delete_address(db, entity, address)


@entityRoute.post('/contact', response_class=JSONResponse)
@handle_result()
async def createContact(
    contact: ContactCreate,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await create_contact(
        db,
        entity=contact.entity,
        number=contact.number,
        email=contact.extra_email,
        type_tag=contact.type_tag,
        details=contact.notes
    )


@entityRoute.put('/contact', response_class=JSONResponse)
@handle_result()
async def updateContact(
    contact: ContactUpdate,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await update_contact(
        db,
        contact=contact.entity,
        number=contact.number,
        extra_email=contact.extra_email,
        type_tag=contact.type_tag,
        details=contact.notes
    )


@entityRoute.delete('/{entity}/contact/', response_class=JSONResponse)
@handle_result()
async def deleteContact(
    entity:UUID,
    contact: UUID,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    return await delete_contact(db, entity, contact)
