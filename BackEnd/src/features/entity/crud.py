import json
from dataclasses import asdict
from datetime import date
from uuid import UUID

from src.dependencies import db
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
    UpdateEntity_async_edgeql,
)


@db.handle_database_errors
async def create_entity(
    db,
    email: str,
    type_tag: str,
    document_type: str,
    status: bool | None,
    document: str,
    name: str,
    sex: str | None,
    relationship_status: str | None,
    details: dict[str, str | int | float] | None,
    birth: date | None,
) -> dict | None:
    result = await CreateEntity_async_edgeql.CreateEntity(
        executor=db,
        email=email,
        type_tag=type_tag,
        document_type=document_type,
        status=status,
        document=document,
        name=name,
        sex=sex,
        relationship_status=relationship_status,
        birth=birth,
        notes=json.dumps(details) if details is not None else None
    )
    if result is not None:
        result = asdict(result)
    return result


@db.handle_database_errors
async def update_entity(
    db,
    entity: UUID,
    email: str | None,
    type_tag: str | None,
    document_type: str | None,
    status: bool | None,
    document: str | None,
    name: str | None,
    sex: str | None,
    relationship_status: str | None,
    details: dict[str, str | int | float] | None,
    birth: date | None,
) -> dict | None:
    result = await UpdateEntity_async_edgeql.UpdateEntity(
        executor=db,
        email=email,
        type_tag=type_tag,
        document_type=document_type,
        status=status,
        document=document,
        name=name,
        sex=sex,
        relationship_status=relationship_status,
        birth=birth,
        notes=json.dumps(details) if details is not None else None,
        entity=entity
    )
    if result is not None:
        result = asdict(result)
    return result


@db.handle_database_errors
async def delete_entity(
    db,
    entity: UUID,
) -> dict | None:

    result = await DeleteEntity_async_edgeql.DeleteEntity(
        executor=db,
        entity=entity
    )
    if result is not None:
        result = asdict(result)
    return result


@db.handle_database_errors
async def get_entity(
    db,
    entity: UUID,
) -> dict | None:
    result = await GetEntity_async_edgeql.GetEntity(
        executor=db,
        entity=entity
    )
    if result is None:
        return None
    result_dict = asdict(result)
    if result_dict["notes"] is not None:
        result_dict["notes"] = json.loads(result_dict["notes"])
    for i in result_dict["phone"]:
        if i["notes"] is not None:
            i["notes"] = json.loads(i["notes"])
    return result_dict


@db.handle_database_errors
async def create_address(
    db,
    entity: UUID,
    state: str,
    city: str,
    district: str,
    street: str,
    number: int | None,
    complement: str | None,
    postal: str | None,
) -> dict | None:
    result = await CreateAddress_async_edgeql.CreateAddress(
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
    if result is not None:
        result = asdict(result)["address"]
    return result


@db.handle_database_errors
async def update_address(
    db,
    address: UUID,
    state: str | None,
    city: str | None,
    district: str | None,
    street: str | None,
    number: int | None,
    complement: str | None,
    postal: str | None,
) -> dict | None:
    result = await UpdateAddress_async_edgeql.UpdateAddress(
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
    if result is not None:
        result = asdict(result)
    return result


@db.handle_database_errors
async def delete_address(
    db,
    entity: UUID,
    address: UUID,
) -> DeleteAddress_async_edgeql.DeleteAddressResult | None:
    return await DeleteAddress_async_edgeql.DeleteAddress(
        executor=db,
        address=address,
        entity_id=entity
    )


@db.handle_database_errors
async def create_contact(
    db,
    entity: UUID,
    number: str,
    type_tag: str,
    email: str | None,
    details: dict[str, str | int | float] | None,
) -> dict | None:
    result = await CreateContact_async_edgeql.CreateContact(
        executor=db,
        type_tag=type_tag,
        extra_email=email,
        number=number,
        entity=entity,
        notes=json.dumps(details) if details is not None else None
    )
    if result is not None:
        result = asdict(result)
    if result["contact"] is None:
        return None
    return result


@db.handle_database_errors
async def update_contact(
    db,
    contact: UUID,
    number: str | None,
    extra_email: str | None,
    type_tag: str | None,
    details: dict[str, str | int | float] | None,
) -> dict | None:
    result = await UpdateContact_async_edgeql.UpdateContact(
        executor=db,
        type_tag=type_tag,
        extra_email=extra_email,
        contact=contact,
        notes=json.dumps(details) if details is not None else None,
        number=number,
    )
    if result is not None:
        result = asdict(result)
    return result


@db.handle_database_errors
async def delete_contact(
    db,
    entity: UUID,
    contact: UUID,
) -> dict | None:
    result = await DeleteContact_async_edgeql.DeleteContact(
        executor=db,
        contact=contact,
        entity_id=entity
    )
    if result is not None:
        result = asdict(result)
    return result
