from pydantic import BaseModel


class CreateDictType(BaseModel):
    title: str
    field: str


class UpdateDictType(BaseModel):
    body: list[CreateDictType]
    change:bool
