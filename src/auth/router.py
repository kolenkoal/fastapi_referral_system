from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi_users import exceptions, models, schemas
from fastapi_users.manager import BaseUserManager
from fastapi_users.router.common import ErrorCode, ErrorModel

from src.auth.auth import auth_backend, fastapi_users
from src.auth.manager import get_user_manager
from src.auth.utils.verify_email import verify_email
from src.exceptions import InvalidEmailException, raise_http_exception
from src.referral_codes.dao import ReferralCodeDAO
from src.users.schemas import UserCreate, UserRead


router = APIRouter(prefix="/auth", tags=["Auth"])

router.include_router(fastapi_users.get_auth_router(auth_backend))
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))


@router.post(
    "/register/referral/{referral_code}",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    name="register:register",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.REGISTER_USER_ALREADY_EXISTS: {
                            "summary": "A user with this email already exists.",
                            "value": {
                                "detail": ErrorCode.REGISTER_USER_ALREADY_EXISTS
                            },
                        },
                        ErrorCode.REGISTER_INVALID_PASSWORD: {
                            "summary": "Password validation failed.",
                            "value": {
                                "detail": {
                                    "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                                    "reason": "Password should be"
                                    "at least 3 characters",
                                }
                            },
                        },
                    }
                }
            },
        },
    },
)
async def register_with_referral_code(
    referral_code: str,
    request: Request,
    user_create: UserCreate,  # type: ignore
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(
        get_user_manager
    ),
):
    try:
        if not verify_email(user_create.email):
            raise_http_exception(InvalidEmailException)

        created_user = await user_manager.create(
            user_create, safe=True, request=request
        )

        await ReferralCodeDAO.insert_referral(referral_code, created_user.id)

    except exceptions.UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
        )
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )

    return schemas.model_validate(UserRead, created_user)
