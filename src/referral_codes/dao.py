from datetime import date, timedelta

from sqlalchemy import and_, insert, select

from src.dao import BaseDAO
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
            pass
        # if there are, deactivate them or delete
        # create and return

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
