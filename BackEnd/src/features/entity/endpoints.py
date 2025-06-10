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


@entityRoute.get('/{id}', response_class=JSONResponse)
@handle_result()
async def getEntity(
    id: UUID,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    return await get_entity(db, entity=id)


@entityRoute.post('/', response_class=JSONResponse)
@handle_result()
async def createEntity(
    entity: EntityCreate,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    return await create_entity(
        db,
        user=user,
        email=entity.email,
        type=entity.type,
        govt_id=entity.govt_id,
        name=entity.name,
        sex=entity.sex,
        relationship_status=entity.relationship_status,
        details=entity.details,
        birth=entity.birth,
        status=entity.status,
        id_type=entity.id_type
    )


@entityRoute.put('/', response_class=JSONResponse)
@handle_result()
async def updateEntity(
    entity: EntityUpdate,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    return await update_entity(
        db,
        email=entity.email,
        type=entity.type,
        status=entity.status,
        id_type=entity.id_type,
        govt_id=entity.govt_id,
        name=entity.name,
        sex=entity.sex,
        relationship_status=entity.relationship_status,
        details=entity.details,
        birth=entity.birth,
        entity=entity.id,
    )


@entityRoute.delete('/{id}', response_class=JSONResponse)
@handle_result()
async def deleteEntity(
    id: UUID,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    return await delete_entity(db, id)


@entityRoute.post('/address', response_class=JSONResponse)
@handle_result()
async def createAddress(
    address: AddressCreate,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
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


@entityRoute.delete('/{id}/address/', response_class=JSONResponse)
@handle_result()
async def deleteAddress(
    id: UUID,
    address: UUID,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    return await delete_address(db, id, address)


@entityRoute.post('/contact', response_class=JSONResponse)
@handle_result()
async def createContact(
    contact: ContactCreate,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    return await create_contact(
        db,
        entity=contact.entity,
        number=contact.number,
        email=contact.email,
        name=contact.name,
        details=contact.details
    )


@entityRoute.put('/contact', response_class=JSONResponse)
@handle_result()
async def updateContact(
    contact: ContactUpdate,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    return await update_contact(
        db,
        contact=contact.id,
        number=contact.number,
        email=contact.email,
        name=contact.name,
        details=contact.details
    )


@entityRoute.delete('/{id}/contact/', response_class=JSONResponse)
@handle_result()
async def deleteContact(
    id:UUID,
    contact: UUID,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    return await delete_contact(db, id, contact)
