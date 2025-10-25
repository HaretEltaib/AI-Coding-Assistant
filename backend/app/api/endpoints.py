from fastapi import APIRouter
from app.api.api_v1.users import router as users_router
from app.api.api_v1.llm import router as llm_router

api_router = APIRouter()
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(llm_router, prefix="/llm", tags=["LLM"])

