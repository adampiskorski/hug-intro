from datetime import datetime
from sqlalchemy import Column, DateTime, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class ToDo(Base):
    """Simple ToDo recording scheme"""
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True)
    todo = Column(String(140), nullable=False)
    assignee = Column(String(60))
    category = Column(String(60))
    completed = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime)

engine = create_engine('sqlite:///hug_intro.db')

Base.metadata.create_all(engine)
