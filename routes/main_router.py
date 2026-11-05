from fastapi import APIRouter
from routes.auth.router import router as auth_router

router = APIRouter(prefix="/api")


router.include_router(router=auth_router, tags=["AUTH"])




