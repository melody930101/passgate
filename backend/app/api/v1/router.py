from fastapi import APIRouter
from app.api.v1 import auth, movies, tickets, stats

api_router = APIRouter()

api_router.include_router(auth.router, prefix='/auth', tags=['认证'])
api_router.include_router(movies.router, prefix='/movies', tags=['电影'])
api_router.include_router(tickets.router, prefix='/tickets', tags=['票务'])
api_router.include_router(stats.router, prefix='/stats', tags=['统计'])
