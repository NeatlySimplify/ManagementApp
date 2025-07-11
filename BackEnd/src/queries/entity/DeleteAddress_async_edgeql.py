# AUTOGENERATED FROM 'src/queries/entity/DeleteAddress.edgeql' WITH:
#     $ gel-py


from __future__ import annotations
import dataclasses
import gel
import uuid


class NoPydanticValidation:
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        # Pydantic 2.x
        from pydantic_core.core_schema import any_schema
        return any_schema()

    @classmethod
    def __get_validators__(cls):
        # Pydantic 1.x
        from pydantic.dataclasses import dataclass as pydantic_dataclass
        _ = pydantic_dataclass(cls)
        cls.__pydantic_model__.__get_validators__ = lambda: []
        return []


@dataclasses.dataclass
class DeleteAddressResult(NoPydanticValidation):
    id: uuid.UUID


async def DeleteAddress(
    executor: gel.AsyncIOExecutor,
    *,
    address: uuid.UUID,
    entity_id: uuid.UUID,
) -> DeleteAddressResult | None:
    return await executor.query_single(
        """\
        with delete_address:= (
            delete Address filter .id = <uuid>$address
        )
        update Entity filter .id = <uuid>$entity_id set {
            address -= delete_address
        }\
        """,
        address=address,
        entity_id=entity_id,
    )
