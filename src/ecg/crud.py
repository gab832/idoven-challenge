from sqlalchemy.orm import Session

from authentication.models import User
from ecg.models import ECG, Lead
from ecg.schemas import ECGCreate


def create_user_ecg(db: Session, ecg: ECGCreate, user: User) -> ECG:
    data = ecg.dict()
    leads = data.pop('leads')
    db_ecg = ECG(date=ecg.date, owner=user.id)
    db.add(db_ecg)
    db.commit()
    db.refresh(db_ecg)
    leads_to_insert = []
    for lead_data in leads:
        lead = Lead(**lead_data, ecg_id=db_ecg.id)
        leads_to_insert.append(lead)
    db.add_all(leads_to_insert)
    db.commit()
    return db_ecg


def get_insights(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(ECG).filter(ECG.owner == user_id).offset(skip).limit(limit).all()
