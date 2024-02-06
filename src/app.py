from fastapi import APIRouter, FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from starlette.middleware.cors import CORSMiddleware

from src.auth.router import router as auth_router
from src.config import settings
from src.referral_codes.router import router as auth_referral_codes
from src.referrals.router import router as referrals_router
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


@app.on_event("startup")
def startup():
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")


router.include_router(auth_router)
router.include_router(user_router)
router.include_router(auth_referral_codes)
router.include_router(referrals_router)

app.include_router(router)
