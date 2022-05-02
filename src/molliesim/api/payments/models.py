from enum import Enum

from uuid import uuid4
from pydantic import BaseModel, ValidationError, validator, Field


class CurrencyEnum(str, Enum):
    EUR = "EUR"
    USD = "USD"


class Amount(BaseModel):
    currency: CurrencyEnum
    value: str

    @validator("value", pre=True)
    def valid_value(cls, v):
        if type(v) != str:
            raise ValueError("The amount contains an invalid value")
        return v

    @validator("currency", pre=True)
    def valid_currency(cls, v):
        if v not in set(item.value for item in CurrencyEnum):
            raise ValueError("The amount contains an invalid currency")
        return v


class Payment(BaseModel):
    amount: Amount
    description: str
    webhookUrl: str
    redirectUrl: str
    sequenceType: str
    id: str = None

    def __init__(self, **data):
        super().__init__(**data)
        self.id = None

    class Config:
        extra = "forbid"
