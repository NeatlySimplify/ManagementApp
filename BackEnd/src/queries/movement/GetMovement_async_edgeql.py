# AUTOGENERATED FROM 'src/queries/movement/GetMovement.edgeql' WITH:
#     $ gel-py


from __future__ import annotations
import dataclasses
import datetime
import decimal
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
class GetMovementResult(NoPydanticValidation):
    id: uuid.UUID
    type_movement: str | None
    value: decimal.Decimal
    installment: int
    notes: str | None
    record: GetMovementResultRecord | None
    accounts: list[GetMovementResultAccountsItem]
    payment: list[GetMovementResultPaymentItem]


@dataclasses.dataclass
class GetMovementResultAccountsItem(NoPydanticValidation):
    id: uuid.UUID
    account_name: str


@dataclasses.dataclass
class GetMovementResultPaymentItem(NoPydanticValidation):
    id: uuid.UUID
    name: str | None
    status: bool | None
    value: decimal.Decimal | None
    payment_date: datetime.date | None
    is_due: datetime.date | None


@dataclasses.dataclass
class GetMovementResultRecord(NoPydanticValidation):
    id: uuid.UUID
    name: str | None
    id_service: str | None


async def GetMovement(
    executor: gel.AsyncIOExecutor,
    *,
    movement: uuid.UUID,
) -> GetMovementResult | None:
    return await executor.query_single(
        """\
        select Movement{
            type_movement:= .type,
            value,
            installment,
            notes,
            record: {
                id,
                name,
                id_service
            },
            accounts:{
                id,
                account_name
            },
            payment: {
                id,
                name,
                status,
                value,
                payment_date,
                is_due,
            }
        } filter .id = <uuid>$movement\
        """,
        movement=movement,
    )
