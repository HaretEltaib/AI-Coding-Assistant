from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import users
from app.db.database import engine
from app.api.endpoints import api_router

# إنشاء الجداول في قاعدة البيانات
users.Base.metadata.create_all(bind=engine)

app = FastAPI()

# إضافة CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تضمين الرواتر مع prefix
app.include_router(api_router, prefix="/api/v1")
