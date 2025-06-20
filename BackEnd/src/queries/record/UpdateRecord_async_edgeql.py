# AUTOGENERATED FROM 'src/queries/record/UpdateRecord.edgeql' WITH:
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
class UpdateRecordResult(NoPydanticValidation):
    id: uuid.UUID


async def UpdateRecord(
    executor: gel.AsyncIOExecutor,
    *,
    value: str | None = None,
    name: str | None = None,
    id_service: str | None = None,
    status: str | None = None,
    type: str | None = None,
    active: bool | None = None,
    notes: str | None = None,
    id: uuid.UUID,
) -> UpdateRecordResult | None:
    return await executor.query_single(
        """\
        with raw_value:= <optional str>$value,
        decimal_value:= (to_decimal(raw_value, 'FM999999999999.99') if exists raw_value else <decimal>{})
        update Record filter .id = <uuid>$id set {
            name:= <optional str>$name ?? .name,
            id_service := <optional str>$id_service ?? .id_service,
            status := <optional str>$status ?? .status,
            type:= <optional str>$type ?? .type,
            active:= <optional bool>$active ?? .active,
            value := decimal_value ?? .value,
            notes:=<optional json>$notes ?? .notes,
        }\
        """,
        value=value,
        name=name,
        id_service=id_service,
        status=status,
        type=type,
        active=active,
        notes=notes,
        id=id,
    )
