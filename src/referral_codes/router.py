from fastapi import APIRouter, Depends

from src.auth.auth import current_user
from src.exceptions import ReferralCodeNotImplementedException
from src.referral_codes.dao import ReferralCodeDAO
from src.responses import UNAUTHORIZED_RESPONSE
from src.users.models import User


router = APIRouter(
    prefix="/referral_codes",
    tags=["Referral Codes"],
)


@router.post(
    "",
    name="Create a referral code.",
    # response_model=SReferralCode,
    responses=UNAUTHORIZED_RESPONSE,
)
async def create_referral_code(user: User = Depends(current_user)):
    referral_code = await ReferralCodeDAO.add(user)

    if not referral_code:
        raise ReferralCodeNotImplementedException

    return referral_code


# post
# delete
# get by email
# post register/referral/referralcode
# get referral by id
