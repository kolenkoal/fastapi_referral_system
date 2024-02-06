import uuid
from datetime import date, datetime

from pydantic import BaseModel


class SReferralCode(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    code: str
    expiration_date: date
    created_at: datetime
    is_active: bool
