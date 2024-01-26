from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    func,
    JSON,
)
from sqlalchemy.orm import relationship

from database import Base


class Lead(Base):
    __tablename__ = 'leads'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    samples = Column(Integer, nullable=True, default=0)
    signal = Column(JSON)

    ecg_id = Column(Integer, ForeignKey('ecgs.id', ondelete='CASCADE'))
    ecg = relationship('ECG', back_populates='leads')


class ECG(Base):
    __tablename__ = 'ecgs'

    id = Column(Integer, primary_key=True)
    owner = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime, index=True, server_default=func.now())
    leads = Column()
    negative_count = Column(Integer, default=0)
    processed = Column(Boolean, default=False)

    leads = relationship('Lead', back_populates='ecg')
