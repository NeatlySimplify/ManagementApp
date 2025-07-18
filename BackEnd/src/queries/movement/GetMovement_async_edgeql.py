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
    type_tag: str | None
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
    event: GetMovementResultPaymentItemEvent | None


@dataclasses.dataclass
class GetMovementResultPaymentItemEvent(NoPydanticValidation):
    id: uuid.UUID
    type_tag: str | None
    name: str | None
    status: bool | None
    date_beginning: datetime.datetime | None
    date_ending: datetime.datetime | None


@dataclasses.dataclass
class GetMovementResultRecord(NoPydanticValidation):
    id: uuid.UUID
    name: str | None
    service_id: str | None


async def GetMovement(
    executor: gel.AsyncIOExecutor,
    *,
    movement: uuid.UUID,
) -> GetMovementResult | None:
    return await executor.query_single(
        """\
        select Movement{
            type_tag,
            value,
            installment,
            notes,
            record: {
                id,
                name,
                service_id
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
                event:{
                    id,
                    type_tag,
                    name,
                    status,
                    date_beginning,
                    date_ending
                }
            }
        } filter .id = <uuid>$movement\
        """,
        movement=movement,
    )
