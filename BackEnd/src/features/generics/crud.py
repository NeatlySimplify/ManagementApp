from dataclasses import asdict
from uuid import UUID

from src.dependencies import db
from src.queries.generics import CreateDetails_async_edgeql, DeleteDetails_async_edgeql


@db.handle_database_errors
async def _create_details(db, title: str, field: str, origin: UUID) -> dict | None:
    result = await CreateDetails_async_edgeql.CreateDetails(db, title=title, field=field, id=origin)
    if result is not None:
        result = asdict(result)
    return result



@db.handle_database_errors
async def _delete_details(db, origin: UUID) -> list[DeleteDetails_async_edgeql.DeleteDetailsResult] | None:
    return await DeleteDetails_async_edgeql.DeleteDetails(db, id=origin)
