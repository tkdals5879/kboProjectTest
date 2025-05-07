#경기 결과
from fastapi import APIRouter, HTTPException, Query
import json
from pathlib import Path

router = APIRouter()
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

@router.get("/")
def get_filtered_game_results(
    date: str = Query(None, title="날짜", description="YYYY-MM-DD 형식의 날짜로 필터링"),
    team: str = Query(None, title="팀명", description="팀명으로 필터링 (예: LG, SSG)")):

    all_games = []

    try:
        game_files = sorted(DATA_DIR.glob("games_*.json"))

        if not game_files:
            raise HTTPException(status_code=404, detail="경기 결과 파일이 없습니다.")

        for file in game_files:
            with open(file, "r", encoding="utf-8") as f:
                month_data = json.load(f)
                all_games.extend(month_data)

        # 필터링: 날짜 또는 팀명으로
        filtered_games = []
        for game in all_games:
            if date and game.get("date") != date:
                continue
            if team and team not in [game.get("home_team"), game.get("away_team")]:
                continue
            filtered_games.append(game)

        if not filtered_games:
            raise HTTPException(status_code=404, detail="검색된 경기가 없습니다.")

        return {"games": filtered_games}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데이터를 읽는 중 오류 발생: {str(e)}")