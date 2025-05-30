from fastapi import Depends
from src.dependencies import db
from uuid import UUID
from decimal import Decimal
from src.queries.record import (
    CreateRecord_async_edgeql,
    DeleteRecord_async_edgeql,
    GetRecord_async_edgeql,
    LinkEntity_async_edgeql,
    LinkEvent_async_edgeql,
    LinkMovement_async_edgeql,
    UnlinkEntity_async_edgeql,
    UnlinkScheduler_async_edgeql,
    UnlinkMovement_async_edgeql,
    UpdateRecord_async_edgeql
)


@db.handle_database_errors
async def getRecord(
        record: UUID,
        db=Depends(db.get_gel_client)
    ) -> GetRecord_async_edgeql.GetRecordResult | None:
    return await GetRecord_async_edgeql.GetRecord(db, id=record)


@db.handle_database_errors
async def createRecord(
        user: UUID,
        name: str,
        id_service: str | None,
        active: bool | None,
        status: str | None,
        type: str,
        value: Decimal,
        details: dict | None,
        entity: UUID,
        db=Depends(db.get_gel_client)
    ) -> CreateRecord_async_edgeql.CreateRecordResult | None:
    return await CreateRecord_async_edgeql.CreateRecord(
        db,
        user=user,
        entity=entity,
        name=name,
        id_service=id_service,
        active=active,
        status=status,
        type=type,
        value=value,
        details=details,
    )


@db.handle_database_errors
async def deleteRecord(
        record: UUID,
        db=Depends(db.get_gel_client)
    ) -> DeleteRecord_async_edgeql.DeleteRecordResult | None:
    return await DeleteRecord_async_edgeql.DeleteRecord(
        db,
        id=record
    )


@db.handle_database_errors
async def updateRecord(
        id: UUID,
        name: str | None,
        id_service: str | None,
        active: bool | None,
        status: str | None,
        type: str | None,
        value: Decimal | None,
        details: dict | None,
        db=Depends(db.get_gel_client)
    ) -> UpdateRecord_async_edgeql.UpdateRecordResult | None:
    return await UpdateRecord_async_edgeql.UpdateRecord(
        db,
        id=id,
        name=name,
        id_service=id_service,
        active=active,
        status=status,
        type=type,
        value=value,
        details=details
    )


@db.handle_database_errors
async def linkEntity(
        entity: UUID,
        record: UUID,
        db=Depends(db.get_gel_client)
    ) -> LinkEntity_async_edgeql.LinkEntityResult | None:
    return await LinkEntity_async_edgeql.LinkEntity(
        db,
        entity_id=entity,
        record_id=record
    )


@db.handle_database_errors
async def linkEvent(
        schedule: UUID,
        record: UUID,
        db=Depends(db.get_gel_client)
    ) -> LinkEvent_async_edgeql.LinkEventResult | None:
    return await LinkEvent_async_edgeql.LinkEvent(
        db,
        schedule_id=schedule,
        record_id=record
    )


@db.handle_database_errors
async def linkMovement(
        movement: UUID,
        record: UUID,
        db=Depends(db.get_gel_client)
    ) -> LinkMovement_async_edgeql.LinkMovementResult | None:
    return await LinkMovement_async_edgeql.LinkMovement(
        db,
        movement_id=movement,
        record=record
    )


@db.handle_database_errors
async def unlinkEntity(
        entity: UUID,
        record: UUID,
        db=Depends(db.get_gel_client)
    ) -> UnlinkEntity_async_edgeql.UnlinkEntityResult | None:
    return await UnlinkEntity_async_edgeql.UnlinkEntity(
        db,
        entity_id=entity,
        id_record=record
    )


@db.handle_database_errors
async def unlinkEvent(
        schedule: UUID,
        record: UUID,
        db=Depends(db.get_gel_client)
    ) -> UnlinkScheduler_async_edgeql.UnlinkSchedulerResult | None:
    return await UnlinkScheduler_async_edgeql.UnlinkScheduler(
        db,
        schedule_id=schedule,
        record=record
    )


@db.handle_database_errors
async def unlinkMovement(
        movement: UUID,
        record: UUID,
        db=Depends(db.get_gel_client)
    ) -> UnlinkMovement_async_edgeql.UnlinkMovementResult | None:
    return await UnlinkMovement_async_edgeql.UnlinkMovement(
        db,
        movement_id=movement,
        record=record
    )
