from api.v1.user import user_router
from api.v1.healthcheck import health_check_router
from fastapi import APIRouter


router = APIRouter()
router.include_router(user_router)
router.include_router(health_check_router)
