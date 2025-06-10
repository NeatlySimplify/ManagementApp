from dataclasses import asdict
from uuid import UUID

from src.dependencies import db
from src.features.generics.crud import _create_details, _delete_details
from src.features.generics.schema import CreateDictType, UpdateDictType
from src.queries.record import (
    CreateRecord_async_edgeql,
    DeleteRecord_async_edgeql,
    GetRecord_async_edgeql,
    LinkEntity_async_edgeql,
    LinkEvent_async_edgeql,
    LinkMovement_async_edgeql,
    UnlinkEntity_async_edgeql,
    UnlinkMovement_async_edgeql,
    UnlinkScheduler_async_edgeql,
    UpdateRecord_async_edgeql,
)


@db.handle_database_errors
async def getRecord(
        db,
        record: UUID,
    ) -> dict | None:
    result = await GetRecord_async_edgeql.GetRecord(db, id=record)
    if result is None: return None
    result_dict = asdict(result)
    return result_dict



@db.handle_database_errors
async def createRecord(
        db,
        user: UUID,
        name: str,
        id_service: str | None,
        active: bool | None,
        status: str | None,
        type: str,
        value: str,
        details: list[CreateDictType] | None,
        entity: UUID,
    ) -> dict | None:
    result = await CreateRecord_async_edgeql.CreateRecord(
        db,
        user=user,
        entity=entity,
        name=name,
        id_service=id_service,
        active=active,
        status=status,
        type=type,
        value=value,
    )
    if result is not None:
        result = asdict(result)
        id = result["id"]
        if details is not None:
            for data in details:
                await _create_details(db, title=data.title, field=data.field, origin=id)
    return result


@db.handle_database_errors
async def deleteRecord(
        db,
        record: UUID,
    ) -> dict | None:
    result = await DeleteRecord_async_edgeql.DeleteRecord(
        db,
        id=record
    )
    if result is not None:
            result = asdict(result)
    return result


@db.handle_database_errors
async def updateRecord(
        db,
        id: UUID,
        name: str | None,
        id_service: str | None,
        active: bool | None,
        status: str | None,
        type: str | None,
        value: str | None,
        details: UpdateDictType | None,
    ) -> dict | None:
    result = await UpdateRecord_async_edgeql.UpdateRecord(
        db,
        id=id,
        name=name,
        id_service=id_service,
        active=active,
        status=status,
        type=type,
        value=value,
    )
    if result is not None:
        result = asdict(result)
        id = result["id"]
        if  details is not None and details.change:
            await _delete_details(db, origin=id)
            for data in details.body:
                await _create_details(db, title=data.title, field=data.field, origin=id)

    return result


@db.handle_database_errors
async def linkEntity(
        db,
        entity: UUID,
        record: UUID,
    ) -> LinkEntity_async_edgeql.LinkEntityResult | None:
    return await LinkEntity_async_edgeql.LinkEntity(
        db,
        entity_id=entity,
        record_id=record
    )


@db.handle_database_errors
async def linkEvent(
        db,
        schedule: UUID,
        record: UUID,
    ) -> LinkEvent_async_edgeql.LinkEventResult | None:
    return await LinkEvent_async_edgeql.LinkEvent(
        db,
        schedule_id=schedule,
        record_id=record
    )


@db.handle_database_errors
async def linkMovement(
        db,
        movement: UUID,
        record: UUID,
    ) -> LinkMovement_async_edgeql.LinkMovementResult | None:
    return await LinkMovement_async_edgeql.LinkMovement(
        db,
        movement_id=movement,
        record=record
    )


@db.handle_database_errors
async def unlinkEntity(
        db,
        entity: UUID,
        record: UUID,
    ) -> UnlinkEntity_async_edgeql.UnlinkEntityResult | None:
    return await UnlinkEntity_async_edgeql.UnlinkEntity(
        db,
        entity_id=entity,
        id_record=record
    )


@db.handle_database_errors
async def unlinkEvent(
        db,
        schedule: UUID,
        record: UUID,
    ) -> UnlinkScheduler_async_edgeql.UnlinkSchedulerResult | None:
    return await UnlinkScheduler_async_edgeql.UnlinkScheduler(
        db,
        schedule_id=schedule,
        record=record
    )


@db.handle_database_errors
async def unlinkMovement(
        db,
        movement: UUID,
        record: UUID,
    ) -> UnlinkMovement_async_edgeql.UnlinkMovementResult | None:
    return await UnlinkMovement_async_edgeql.UnlinkMovement(
        db,
        movement_id=movement,
        record=record
    )
