from pydantic import BaseModel
from typing import List

class ShareholderBase(BaseModel):
    name: str
    email: str

class ShareholderCreate(ShareholderBase):
    password: str

class Shareholder(ShareholderBase):
    id: int
    total_shares: int

    class Config:
        orm_mode = True
