from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from db.session import Base


class Run(Base):
    __tablename__ = "runs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    total = Column(Integer, default=0)
    success = Column(Integer, default=0)
    failed = Column(Integer, default=0)
    status = Column(String, default="success")
    message = Column(String, nullable=True)

    # run_detailsとのリレーション
    details = relationship("RunDetail", back_populates="run")


class RunDetail(Base):
    __tablename__ = "run_details"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("runs.id"))
    row_number = Column(Integer)
    data = Column(JSON)  # 登録に使った1行分の情報
    result = Column(String)  # "success" or "error"
    error_message = Column(String, nullable=True)

    run = relationship("Run", back_populates="details")
