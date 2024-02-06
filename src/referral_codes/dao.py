from datetime import date, timedelta

from sqlalchemy import and_, delete, insert, select

from src.dao import BaseDAO
from src.exceptions import (
    ForbiddenException,
    ReferralCodeNotFoundException,
    raise_http_exception,
)
from src.referral_codes.models import ReferralCode
from src.referral_codes.utils.referral_code import generate_referral_code
from src.utils.session import manage_session


class ReferralCodeDAO(BaseDAO):
    model = ReferralCode

    @classmethod
    @manage_session
    async def add(cls, user, session=None):
        user_referral_code = await cls._get_user_referral_codes(user)

        if not user_referral_code:
            return await cls._create_referral_code(user)
        else:
            return await cls._change_referral_code(user, user_referral_code.id)

    @classmethod
    @manage_session
    async def _get_user_referral_codes(cls, user, session=None):
        get_user_referral_code_query = select(cls.model).where(
            and_(
                cls.model.user_id == user.id,
                cls.model.is_active == True,  # noqa
            )
        )
        user_referral_code_result = await session.execute(
            get_user_referral_code_query
        )

        user_referral_code = user_referral_code_result.scalar_one_or_none()

        return user_referral_code

    @classmethod
    @manage_session
    async def _create_referral_code(cls, user, session=None):
        code = generate_referral_code()
        expiration_date = date.today() + timedelta(days=360)

        insert_referral_code_query = (
            insert(ReferralCode).values(
                user_id=user.id, code=code, expiration_date=expiration_date
            )
        ).returning(ReferralCode)

        referral_code_result = await session.execute(
            insert_referral_code_query
        )

        await session.commit()

        return referral_code_result.scalar_one_or_none()

    @classmethod
    @manage_session
    async def _change_referral_code(
        cls, user, user_referral_code_id, session=None
    ):
        await cls.delete(user_referral_code_id, user)
        return await cls._create_referral_code(user)

    @classmethod
    @manage_session
    async def delete(cls, referral_code_id, user, session=None):
        referral_code = await cls.get_by_id(referral_code_id)

        if not referral_code:
            raise_http_exception(ReferralCodeNotFoundException)

        if referral_code.user_id != user.id:
            raise_http_exception(ForbiddenException)

        delete_current_referral_code_query = delete(cls.model).where(
            cls.model.id == referral_code_id
        )

        await session.execute(delete_current_referral_code_query)
        await session.commit()

        current_referral_code = await cls._get_user_referral_codes(user)

        if current_referral_code:
            return await cls._change_referral_code(
                user, current_referral_code.id
            )

    @classmethod
    @manage_session
    async def get_by_id(cls, referral_code_id, session=None):
        get_referral_code_query = select(cls.model).where(
            cls.model.id == referral_code_id
        )

        referral_code = (
            await session.execute(get_referral_code_query)
        ).scalar_one_or_none()

        return referral_code
