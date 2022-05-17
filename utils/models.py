from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import declarative_base

from connect_database import get_engine

Base = declarative_base()

class Track(Base):
    __tablename__ = "tracks"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    def __repr__(self):
        return f"Track(id={self.id!r}, name={self.name!r})"

Base.metadata.create_all(get_engine())