from sqlalchemy.orm import Session
from models.db_model import MatchResult

def get_results_by_date(db: Session, target_date):
    return db.query(MatchResult).filter(MatchResult.date == target_date).all()

def save_results(db: Session, results: list):
    for res in results:
        match = MatchResult(**res)
        db.add(match)
    db.commit()