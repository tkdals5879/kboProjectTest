#팀 순위
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.ranking_service import get_current_rankings
from models.schemas import TeamRankingResponse
from utils.db import get_db

router = APIRouter()

@router.get("/", response_model=list[TeamRankingResponse])
def get_rankings(db: Session = Depends(get_db)):
    return get_current_rankings(db)