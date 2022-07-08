from fastapi import APIRouter, status


health_check_router = APIRouter(tags=["health"])


@health_check_router.get("/health", status_code=status.HTTP_200_OK)
async def check_status():
    return {"status": "OK"}
