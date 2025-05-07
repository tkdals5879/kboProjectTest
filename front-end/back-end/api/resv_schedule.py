from fastapi import APIRouter, HTTPException
from pathlib import Path
import json

router = APIRouter()
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

@router.get("/schedule")
def get_schedule():
    try:
        file = DATA_DIR / "schedule.json"
        with open(file, "r", encoding="utf-8") as f:
            schedule_data = json.load(f)

        return {"games": schedule_data}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="일정 데이터 파일이 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")