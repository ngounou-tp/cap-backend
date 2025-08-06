from pydantic import BaseModel
from datetime import datetime

class IssuanceCreate(BaseModel):
    shareholder_id: int
    number_of_shares: int
    price_per_share: float

class Issuance(BaseModel):
    id: int
    shareholder_id: int
    number_of_shares: int
    price_per_share: float
    date: datetime

    class Config:
        orm_mode = True
