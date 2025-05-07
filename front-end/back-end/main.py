from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.games import router as games_router
from api.ranking import router as ranking_router
# from api.players import router as players_router
# from api.stadiums import router as stadiums_router

#from scheduler.scheduler import start_scheduler

app = FastAPI(
    title="야구 정보 사이트",
    description="KBO 일정, 기록, 예매 정보를 제공하는 API",
    version="1.0.0"
)

# CORS 설정 (React 앱이 사용하는 도메인 허용)
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],  # React 앱의 URL
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

app.include_router(games_router, prefix="/games", tags=["경기 일정/결과"])
app.include_router(ranking_router, prefix="/ranking", tags=["랭킹킹"])
# app.include_router(players_router, prefix="/players", tags=["선수 정보"])
# app.include_router(stadiums_router, prefix="/stadiums", tags=["구장 정보"])

#start_scheduler()

