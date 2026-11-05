from fastapi import FastAPI
import uvicorn

from database_connection import init_db
from routes.main_router import router as main_router
from contextlib import asynccontextmanager
from fastapi_pagination import add_pagination

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(description="MemSmash API", title="Mem Smash API", lifespan=lifespan)

app.include_router(main_router)
add_pagination(app)



@app.get("/health", tags=["SERVER HEALTH"])
async def health():
    return {"status": "ok"}



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)