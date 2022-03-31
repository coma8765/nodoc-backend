from sqlalchemy import Integer, String, Boolean, ForeignKey, Column, Text, Date, Table
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    """It's model for user"""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True)
    hashed_password = Column(String(60), nullable=False)

    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    patronymic = Column(String(50))
    birthday = Column(Date, nullable=False)

    is_confirmed = Column(Boolean, default=False)


__all__ = ["User"]
