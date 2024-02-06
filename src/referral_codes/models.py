from datetime import date
from uuid import UUID

from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models import created_at, str256, uuidpk, uuidpk_not_unique


class ReferralCode(Base):
    __tablename__ = "referral_codes"

    id: Mapped[uuidpk]
    user_id: Mapped[uuidpk_not_unique] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    code: Mapped[str256]
    expiration_date: Mapped[date]
    created_at: Mapped[created_at]
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )

    user = relationship("User", back_populates="referral_codes")

    users_referrals: Mapped[list["User"]] = relationship(  # noqa
        back_populates="referrals",
        secondary="user_referral_codes",
    )


class UserReferralCode(Base):
    __tablename__ = "user_referral_codes"

    user_id: Mapped[UUID] = mapped_column(
        GUID, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )

    referral_id: Mapped[UUID] = mapped_column(
        GUID,
        ForeignKey("referral_codes.id", ondelete="CASCADE"),
        primary_key=True,
    )

    created_at: Mapped[created_at]
