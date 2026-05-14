import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import tasks

logging.basicConfig(level=logging.INFO)

# 앱 시작 시 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow Pro API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)
