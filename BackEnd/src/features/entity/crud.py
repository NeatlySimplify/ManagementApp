from fastapi import Depends
from src.dependencies import db
from uuid import UUID
from datetime import date
from src.queries.entity import (
    CreateAddress_async_edgeql,
    CreateContact_async_edgeql,
    CreateEntity_async_edgeql,
    DeleteAddress_async_edgeql,
    DeleteContact_async_edgeql,
    DeleteEntity_async_edgeql,
    GetEntity_async_edgeql,
    UpdateAddress_async_edgeql,
    UpdateContact_async_edgeql,
    UpdateEntity_async_edgeql
)


@db.handle_database_errors
async def create_entity(
        user: UUID,
        email: str,
        type: str,
        id_type: str,
        status: bool | None,
        govt_id: str,
        name: str,
        sex: str | None,
        relationship_status: str | None,
        details: dict | None,
        birth: date | None,
        db = Depends(db.get_gel_client)
    ) -> CreateEntity_async_edgeql.CreateEntityResult | None:
    return await CreateEntity_async_edgeql.CreateEntity(
        executor=db,
        user=user,
        email=email,
        type=type,
        id_type=id_type,
        status=status,
        govt_id=govt_id,
        name=name,
        sex=sex,
        relationship_status=relationship_status,
        details=details,
        birth=birth
    )


@db.handle_database_errors
async def update_entity(
        entity: UUID,
        email: str | None,
        type: str | None,
        id_type: str | None,
        status: bool | None,
        govt_id: str | None,
        name: str | None,
        sex: str | None,
        relationship_status: str | None,
        details: dict | None,
        birth: date | None,
        db = Depends(db.get_gel_client)
    ) -> UpdateEntity_async_edgeql.UpdateEntityResult | None:
    return await UpdateEntity_async_edgeql.UpdateEntity(
        executor=db,
        email=email,
        type=type,
        id_type=id_type,
        status=status,
        govt_id=govt_id,
        name=name,
        sex=sex,
        relationship_status=relationship_status,
        details=details,
        birth=birth,
        entity=entity
    )


@db.handle_database_errors
async def delete_entity(
        entity: UUID,
        db = Depends(db.get_gel_client)
    ) -> DeleteEntity_async_edgeql.DeleteEntityResult | None:
    return await DeleteEntity_async_edgeql.DeleteEntity(
        executor=db,
        entity=entity
    )


@db.handle_database_errors
async def get_entity(
        entity: UUID,
        db = Depends(db.get_gel_client)
    ) -> GetEntity_async_edgeql.GetEntityResult | None:
    return await GetEntity_async_edgeql.GetEntity(
        executor=db,
        entity=entity
    )


@db.handle_database_errors
async def create_address(
        entity: UUID,
        state,
        city,
        district,
        street,
        number,
        complement,
        postal,
        db=Depends(db.get_gel_client)
    ) -> CreateAddress_async_edgeql.CreateAddressResult | None:
    return await CreateAddress_async_edgeql.CreateAddress(
        executor=db,
        state=state,
        city=city,
        district=district,
        street=street,
        number=number,
        complement=complement,
        postal=postal,
        entity_id=entity
    )


@db.handle_database_errors
async def update_address(
        address: UUID,
        state: str | None,
        city: str | None,
        district: str | None,
        street: str | None,
        number: int | None,
        complement: str | None,
        postal: str | None,
        db=Depends(db.get_gel_client)
    ):
    await UpdateAddress_async_edgeql.UpdateAddress(
        executor=db,
        state=state,
        city=city,
        district=district,
        street=street,
        number=number,
        complement=complement,
        postal=postal,
        address=address
    )
    return


@db.handle_database_errors
async def delete_address(
        entity: UUID,
        address: UUID,
        db=Depends(db.get_gel_client)
    ) -> DeleteAddress_async_edgeql.DeleteAddressResult | None:
    return await DeleteAddress_async_edgeql.DeleteAddress(
        executor=db,
        address=address,
        entity_id=entity
    )


@db.handle_database_errors
async def create_contact(
        entity: UUID,
        number: dict,
        name: str,
        email: str | None,
        details: dict | None,
        db=Depends(db.get_gel_client)
    ) -> CreateContact_async_edgeql.CreateContactResult | None:
    return await CreateContact_async_edgeql.CreateContact(
        executor=db,
        number=number,
        name=name,
        email=email,
        details=details,
        entity=entity
        )


@db.handle_database_errors
async def update_contact(
        contact: UUID,
        number: dict | None,
        email: str | None,
        name: str | None,
        details: dict | None,
        db=Depends(db.get_gel_client)
    ) -> UpdateContact_async_edgeql.UpdateContactResult | None:
    await UpdateContact_async_edgeql.UpdateContact(
        executor=db,
        number=number,
        name=name,
        details=details,
        email=email,
        contact=contact
    )


@db.handle_database_errors
async def delete_contact(
        entity: UUID,
        contact: UUID,
        db=Depends(db.get_gel_client)
    ) -> DeleteContact_async_edgeql.DeleteContactResult | None:
    return await DeleteContact_async_edgeql.DeleteContact(
        executor=db,
        contact=contact,
        entity_id=entity
    )
