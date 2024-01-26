from typing import Union, List

from fastapi import APIRouter, BackgroundTasks, Depends, Security, status
from sqlalchemy.orm import Session

from authentication.models import Role, User
from authentication.crud import get_current_user
from ecg.crud import create_user_ecg, get_insights
from ecg.schemas import ECGCreate, ECG
from ecg.models import ECG as ECGModel
from database import get_db
from settings import settings


routers = APIRouter(
    prefix=settings.api_prefix,
    tags=['ecgs'],
)


def calculate_under_zeros(db: Session, ecg: ECGModel):
    negative = 0
    if not ecg.processed:
        for lead in ecg.leads:
            negative += len(list(filter(lambda x: (x < 0), lead.signal)))
        db_ecg = db.query(ECGModel).filter(ECGModel.id == ecg.id).first()
        db_ecg.negative_count = negative
        db_ecg.processed = True
        db.commit()


@routers.post(
    '/ecg',
    status_code=status.HTTP_201_CREATED,
    response_model=ECG,
)
def create_ecg(
    ecg: ECGCreate,
    background_tasks: BackgroundTasks,
    user: User = Security(get_current_user, scopes=[Role.USER]),
    db: Session = Depends(get_db),
):
    db_ecg = create_user_ecg(db, ecg, user)
    background_tasks.add_task(calculate_under_zeros, db, db_ecg)
    return db_ecg


@routers.get(
    '/insights',
    status_code=status.HTTP_200_OK,
    response_model=List[ECG],
)
def list_insights(
    user: User = Security(get_current_user, scopes=[Role.USER]),
    db: Session = Depends(get_db),
    q: Union[str, None] = None,
    skip: int = 0,
    limit: int = 20,
):
    return get_insights(db, user.id, skip, limit)
