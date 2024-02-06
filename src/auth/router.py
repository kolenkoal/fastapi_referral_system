from fastapi import APIRouter

from src.auth.auth import auth_backend, fastapi_users
from src.users.schemas import UserCreate, UserRead


router = APIRouter(prefix="/auth", tags=["Auth"])

router.include_router(fastapi_users.get_auth_router(auth_backend))
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
