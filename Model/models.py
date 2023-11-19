from sqlalchemy import Integer, Column, String
from .database import Base

class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(16))
    body = Column(String(100))