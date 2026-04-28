from db_models.base import Base
from sqlalchemy import Column, String, Boolean, DateTime, Float, Integer
from db_models.mixin import ToDictMixin


class MovieDBModel(ToDictMixin, Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    description = Column(String)
    image_url = Column(String)
    location = Column(String)
    published = Column(Boolean)
    rating = Column(Float)
    genre_id = Column(Integer)
    created_at = Column(DateTime)

    def __repr__(self) -> str:
        return f"<Movie(id='{self.id}', name='{self.name}')>"
