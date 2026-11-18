from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True)
    country = Column(String(10), default="NG")
    created_at = Column(DateTime, default=datetime.utcnow)
    api_key = Column(String(100), unique=True)

class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    iso = Column(String(10))
    action = Column(String(20))
    amount = Column(Float)
    price = Column(Float)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    machine = Column(String(50))
    status = Column(String(20), default="queued") # queued, running, done, failed
    stdout = Column(Text, default="")
    stderr = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)

class AppBuild(Base):
    __tablename__ = "app_builds"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    name = Column(String(100))
    spec = Column(Text)
    status = Column(String(20), default="building")
    url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
