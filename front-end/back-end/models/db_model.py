from sqlalchemy import Column, Integer, String, Date, Time, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

#팀랭킹킹
class TeamRanking(Base):
    __tablename__ = 'team_rankings'

    id = Column(Integer, primary_key=True, index=True)
    rank = Column(Integer)                  # 순위
    team_name = Column(String, unique=True) # 팀명
    games = Column(Integer)                 # 총 경기 수
    wins = Column(Integer)                  # 승
    losses = Column(Integer)                # 패
    draws = Column(Integer)                 # 무
    win_rate = Column(Float)                # 승률 (예: 0.714)
    game_diff = Column(String)              # 게임차 (문자열로 저장)
    last_10_games = Column(String)          # 최근 10경기 성적 (예: 7-3)
    streak = Column(String)                 # 연속 승/패 (예: 3연승)
    home = Column(String)                   # 홈 성적 (예: 10-5)
    away = Column(String)                   # 원정 성적 (예: 8-6)
    updated_at = Column(DateTime, default=datetime.utcnow)  # 데이터 저장 시간

#경기 결과
class MatchResult(Base):
    __tablename__ = 'match_results'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)                 # 경기 날짜
    time = Column(Time)                             # 경기 시간
    home_team = Column(String)                      # 홈팀 이름
    away_team = Column(String)                      # 어웨이팀 이름
    home_score = Column(Integer)                    # 홈팀 점수
    away_score = Column(Integer)                    # 어웨이팀 점수
    stadium = Column(String)                        # 경기장 이름
    created_at = Column(DateTime, default=datetime.utcnow)  # 레코드 생성 시각
