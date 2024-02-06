import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field


class SReferralCode(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    code: str = Field(max_length=256, min_length=2)
    expiration_date: date
    created_at: datetime
    is_default: bool
