from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class Lead(BaseModel):
    name: str
    samples: Optional[int] = 0
    signal: list[int]


class ECGBase(BaseModel):
    date: datetime
    leads: list[Lead] | None = None


class ECGCreate(ECGBase):
    pass


class ECG(ECGBase):
    id: int
    negative_count: int
    owner: int

    class Config:
        from_attributes = True
