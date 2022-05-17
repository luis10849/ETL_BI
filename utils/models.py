from sqlalchemy import Column,DateTime,Integer,String,Text
from sqlalchemy.orm import declarative_base

from connect_database import get_engine

Base = declarative_base()

class Track(Base):
    __tablename__ = "tracks"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    url =  Column(Text)
    popularity = Column(Integer)
    duration_ms = Column(String(50))
    played_at = Column(DateTime)
    album_id = Column(String(100))
    track_id = Column(String(100))
    id_unique = Column(String(100), unique=True)
    def __repr__(self):
        return f"Track(id={self.id!r}, name={self.name!r})"

Base.metadata.create_all(get_engine())