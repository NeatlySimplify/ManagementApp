from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.dependencies.auth import get_current_user
from src.dependencies.response_decorator import handle_result
from src.features.entity.crud import (
    create_entity,
    create_address,
    create_contact,
    get_entity,
    update_entity,
    update_address,
    update_contact,
    delete_entity,
    delete_address,
    delete_contact
)
from src.features.entity.schema import (
    EntityCreate,
    EntityUpdate,
    AddressCreate,
    AddressUpdate,
    ContactCreate,
    ContactUpdate,
    ModelID
)


entityRoute = APIRouter(prefix='/api/entity')


@entityRoute.get('/', response_class=JSONResponse)
@handle_result()
async def getEntity(
        entity:ModelID,
        user=Depends(get_current_user)
    ):
    return await get_entity(entity=entity.id)


@entityRoute.post('/', response_class=JSONResponse)
@handle_result()
async def createEntity(
        entity: EntityCreate,
        user=Depends(get_current_user)
    ):
    return await create_entity(
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
        user=Depends(get_current_user)
    ):
    return await update_entity(
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


@entityRoute.delete('/', response_class=JSONResponse)
@handle_result()
async def deleteEntity(
        entity: ModelID,
        user=Depends(get_current_user)
    ):
    return await delete_entity(entity.id)


@entityRoute.post('/address', response_class=JSONResponse)
@handle_result()
async def createAddress(
        address: AddressCreate,
        user=Depends(get_current_user)
    ):
    return await create_address(
        address.id,
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
        user=Depends(get_current_user)
    ):
    return await update_address(
        address.id,
        address.state,
        address.city,
        address.district,
        address.street,
        address.number,
        address.complement,
        address.postal,
    )


@entityRoute.delete('/address', response_class=JSONResponse)
@handle_result()
async def deleteAddress(
        address: ModelID,
        entity: ModelID,
        user=Depends(get_current_user)
    ):
    return await delete_address(entity.id, address.id)


@entityRoute.post('/contact', response_class=JSONResponse)
@handle_result()
async def createContact(
        contact: ContactCreate,
        user=Depends(get_current_user)
    ):
    return await create_contact(
        entity=contact.id,
        number=contact.number,
        email=contact.email,
        name=contact.name,
        details=contact.details
    )


@entityRoute.put('/contact', response_class=JSONResponse)
@handle_result()
async def updateContact(
        contact: ContactUpdate,
        user=Depends(get_current_user)
    ):
    return await update_contact(
        contact=contact.id,
        number=contact.number,
        email=contact.email,
        name=contact.name,
        details=contact.details
    )


@entityRoute.delete('/contact', response_class=JSONResponse)
@handle_result()
async def deleteContact(
        entity: ModelID,
        contact: ModelID,
        user=Depends(get_current_user)
    ):
    return await delete_contact(entity.id, contact.id)
