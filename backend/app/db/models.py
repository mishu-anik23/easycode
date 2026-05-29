from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class SessionHistory(Base):
    __tablename__ = "session_history"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String, index=True)
    action = Column(String, nullable=False)
    payload = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
