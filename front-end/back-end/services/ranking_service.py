from sqlalchemy.orm import Session
from models.db_model import TeamRanking
from datetime import datetime

def save_rankings(db: Session, data: list):
    for item in data:
        ranking = db.query(TeamRanking).filter_by(team_name=item["team_name"]).first()
        if ranking:
            for key, value in item.items():
                setattr(ranking, key, value)
            ranking.updated_at = datetime.utcnow()
        else:
            db.add(TeamRanking(**item))
    db.commit()

def get_current_rankings(db: Session):
    return db.query(TeamRanking).order_by(TeamRanking.rank).all()