from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, index=True) # ID from Celery
    query = Column(String)
    status = Column(String, default="PENDING") # PENDING, SUCCESS, FAILED
    result_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)