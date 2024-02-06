from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.auth.router import router as auth_router
from src.referral_codes.router import router as auth_referral_codes
from src.users.router import router as user_router


app = FastAPI()

router = APIRouter(prefix="/api")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://localhost:3000",
    "https://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router.include_router(user_router)
router.include_router(auth_router)
router.include_router(auth_referral_codes)

app.include_router(router)
