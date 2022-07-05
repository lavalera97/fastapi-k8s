from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def check_status():
    return {"status": "OK"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, access_log=False, reload=True)
