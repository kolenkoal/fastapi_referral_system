from datetime import date, timedelta

from sqlalchemy import and_, delete, insert, select
from sqlalchemy.orm import joinedload

from src.dao import BaseDAO
from src.exceptions import (
    ForbiddenException,
    ReferralCodeNotFoundException,
    ReferralCodeNotImplementedException,
    ReferrerNotFoundException,
    UserIsAlreadyReferral,
    raise_http_exception,
)
from src.referral_codes.models import ReferralCode, UserReferralCode
from src.referral_codes.utils.referral_code import generate_referral_code
from src.users.models import User
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
        referral_code = await cls._get_by_id(referral_code_id)

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
    async def _get_by_id(cls, referral_code_id, session=None):
        get_referral_code_query = select(cls.model).where(
            cls.model.id == referral_code_id
        )

        referral_code = (
            await session.execute(get_referral_code_query)
        ).scalar_one_or_none()

        return referral_code

    @classmethod
    @manage_session
    async def _get_by_user_id(cls, user_id, session=None):
        get_referral_code_query = select(cls.model).where(
            cls.model.user_id == user_id
        )

        referral_code = (
            await session.execute(get_referral_code_query)
        ).scalar_one_or_none()

        return referral_code

    @classmethod
    @manage_session
    async def _get_by_referral_code(cls, code, session=None):
        get_referral_code_query = select(cls.model).where(
            cls.model.code == code
        )

        referral_code = (
            await session.execute(get_referral_code_query)
        ).scalar_one_or_none()

        return referral_code

    @classmethod
    @manage_session
    async def get_by_email(cls, referrer_email, session=None):
        get_referral_code_query = (
            select(cls.model)
            .join(User, User.id == cls.model.user_id)
            .where(User.email == referrer_email)
        )

        referral_code = (
            await session.execute(get_referral_code_query)
        ).scalar_one_or_none()

        return referral_code

    @classmethod
    @manage_session
    async def check_email(cls, referrer_email, session=None):
        get_email_query = select(User.email).where(
            User.email == referrer_email
        )

        email = (await session.execute(get_email_query)).scalar_one_or_none()

        return email

    @classmethod
    @manage_session
    async def insert_referral(cls, code, created_user_id, session=None):
        await cls._check_existing_referral(code, created_user_id)

        new_referral = await cls._add_referral(code, created_user_id)

        if not new_referral:
            raise_http_exception(ReferralCodeNotImplementedException)

        return code

    @classmethod
    @manage_session
    async def _check_existing_referral(
        cls, code, created_user_id, session=None
    ):
        referral_code = await cls._get_by_referral_code(code)

        get_user_referral_query = select(UserReferralCode).where(
            and_(
                UserReferralCode.referral_id == created_user_id,
                UserReferralCode.referrer_id == referral_code.user_id,
            )
        )

        user_referral = (
            await session.execute(get_user_referral_query)
        ).scalar_one_or_none()

        if user_referral:
            raise_http_exception(UserIsAlreadyReferral)

        return False

    @classmethod
    @manage_session
    async def _add_referral(cls, code, created_user_id, session=None):
        referrer_referral_code = await cls._get_by_referral_code(code)

        insert_referral_query = (
            insert(UserReferralCode)
            .values(
                referrer_id=referrer_referral_code.user_id,
                referral_id=created_user_id,
            )
            .returning(UserReferralCode)
        )

        new_referral = (
            await session.execute(insert_referral_query)
        ).scalar_one_or_none()

        await session.commit()

        return new_referral

    @classmethod
    @manage_session
    async def get_referrals_by_referrer_id(
        cls, user, referrer_id, session=None
    ):
        referrer_code = await cls._get_by_user_id(referrer_id)

        if not referrer_code:
            raise_http_exception(ReferrerNotFoundException)

        if referrer_code.user_id != user.id:
            raise_http_exception(ForbiddenException)

        return await cls._get_referrer_referrals(referrer_code.user_id)

    @classmethod
    @manage_session
    async def _get_referrer_referrals(cls, referrer_id, session=None):
        get_referrer_referrals_query = (
            select(User)
            .join(UserReferralCode, UserReferralCode.referrer_id == User.id)
            .options(joinedload(User.referrals))
            .where(UserReferralCode.referrer_id == referrer_id)
        )

        referrer_referrals_result = await session.execute(
            get_referrer_referrals_query
        )

        referrer_referrals = (
            referrer_referrals_result.unique().mappings().all()
        )

        return referrer_referrals[0]["User"]
