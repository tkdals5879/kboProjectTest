from pydantic import BaseModel
from datetime import datetime, date, time

#팀랭킹
class TeamRankingResponse(BaseModel):
    team_name: str
    rank: int
    games_played: int
    wins: int
    losses: int
    draws: int
    win_rate: str
    recent_form: str
    

    class Config:
        orm_mode = True


class MatchResultResponse(BaseModel):
    date: date
    time: time
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    stadium: str

    class Config:
        orm_mode = True