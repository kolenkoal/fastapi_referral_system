from fastapi import APIRouter, Depends, Response, status

from src.auth.auth import current_user
from src.exceptions import (
    EmailNotFoundException,
    ReferralCodeNotFoundException,
    ReferralCodeNotImplementedException,
    raise_http_exception,
)
from src.referral_codes.dao import ReferralCodeDAO
from src.referral_codes.schemas import SReferralCode, SReferralCodeInfo
from src.responses import (
    EMAIL_NOT_FOUND_RESPONSE,
    UNAUTHORIZED_REFERRAL_CODE_NOT_FOUND_RESPONSE,
    UNAUTHORIZED_RESPONSE,
)
from src.users.models import User


router = APIRouter(prefix="/referral_codes", tags=["Referral Codes"])


@router.post(
    "",
    name="Create a referral code.",
    response_model=SReferralCode,
    responses=UNAUTHORIZED_RESPONSE,
)
async def create_referral_code(user: User = Depends(current_user)):
    referral_code = await ReferralCodeDAO.add(user)

    if not referral_code:
        raise ReferralCodeNotImplementedException

    return referral_code


@router.delete(
    "/{referral_code_id}",
    name="Delete certain referral code.",
    responses=UNAUTHORIZED_REFERRAL_CODE_NOT_FOUND_RESPONSE,
)
async def delete_referral_code(
    referral_code_id, user: User = Depends(current_user)
):
    deleted_address = await ReferralCodeDAO.delete(referral_code_id, user)

    if not deleted_address:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/email/{referrer_email}",
    name="Get referral code by referrer ID.",
    response_model=SReferralCodeInfo,
    responses=EMAIL_NOT_FOUND_RESPONSE,
)
async def get_referral_code_by_email(referrer_email):
    if not await ReferralCodeDAO.check_email(referrer_email):
        raise_http_exception(EmailNotFoundException)

    referral_code = await ReferralCodeDAO.get_by_email(referrer_email)

    if not referral_code:
        raise ReferralCodeNotFoundException

    return referral_code
