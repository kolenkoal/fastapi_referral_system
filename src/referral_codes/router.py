from fastapi import APIRouter, Depends, Response, status

from src.auth.auth import current_user
from src.exceptions import ReferralCodeNotImplementedException
from src.referral_codes.dao import ReferralCodeDAO
from src.referral_codes.schemas import SReferralCode
from src.responses import (
    UNAUTHORIZED_REFERRAL_CODE_NOT_FOUND_RESPONSE,
    UNAUTHORIZED_RESPONSE,
)
from src.users.models import User


router = APIRouter(
    prefix="/referral_codes",
    tags=["Referral Codes"],
)


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


# post
# delete
# get by email
# post register/referral/referralcode
# get referral by id
