from uuid import uuid4

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from jose import jwt, JWTError

from api.routes import router as api_router
from config import settings
from db.database import database

app = FastAPI()
app.include_router(api_router)


@app.middleware("http")
async def add_request_id(request: Request, call_next) -> Response:
    request.scope['request_id'] = str(uuid4())
    response = await call_next(request)
    response.headers['X-Request-ID'] = request.scope['request_id']
    return response


@app.middleware("http")
async def add_token_exception_decription(request: Request, call_next) -> Response:
    if request.method != 'OPTIONS' and request.headers.get("Authorization"):
        auth_header: str = request.headers.get("Authorization")
        if not auth_header or ' ' not in auth_header:
            return JSONResponse(
                {"detail": "Invalid header"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        auth_type, token = auth_header.split(" ", 1)
        if auth_type.lower() != "bearer":
            return JSONResponse(
                {"detail": "Invalid header."},
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        try:
            jwt.decode(token, settings.SECRET_KEY, [settings.ALGORITHM])
        except JWTError:
            return JSONResponse(
                {"detail": "Invalid token."},
                status_code=status.HTTP_401_UNAUTHORIZED
            )
    response = await call_next(request)
    return response


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, access_log=False, reload=True)
