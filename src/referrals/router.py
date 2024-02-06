from fastapi import APIRouter, Depends

from src.auth.auth import current_user
from src.exceptions import ReferralNotFoundException
from src.referral_codes.dao import ReferralCodeDAO
from src.responses import UNAUTHORIZED_FORBIDDEN_REFERRER_NOT_FOUND_RESPONSE
from src.users.models import User
from src.users.schemas import ReferrerReferrals


router = APIRouter(prefix="/referrals", tags=["Referrals"])


@router.get(
    "/{referrer_id}",
    name="Get referrals by referrer ID.",
    responses=UNAUTHORIZED_FORBIDDEN_REFERRER_NOT_FOUND_RESPONSE,
    response_model=ReferrerReferrals,
)
async def get_referrals_by_referrer_id(
    referrer_id, user: User = Depends(current_user)
):
    referrals = await ReferralCodeDAO.get_referrals_by_referrer_id(
        user, referrer_id
    )

    if not referrals:
        raise ReferralNotFoundException

    return referrals
