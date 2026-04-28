from db_models.base import Base
from sqlalchemy import Column, String, Boolean, DateTime
from db_models.mixin import ToDictMixin


class UserDBModel(ToDictMixin, Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    email = Column(String)
    full_name = Column(String)
    password = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    verified = Column(Boolean)
    banned = Column(Boolean)
    roles = Column(String)

    def __repr__(self) -> str:
        return f"<User(id='{self.id}', email='{self.email}')>"
