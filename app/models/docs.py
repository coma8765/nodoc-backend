from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from .base import Base


class Doc(Base):
    """User's docs"""
    __tablename__ = "doc"

    user_id = Column(ForeignKey("user.id"), primary_key=True)
    type_id = Column(ForeignKey("doc_type.id"), primary_key=True)
    _data = Column("data", Text)

    user = relationship("User", backref="docs", cascade="all, delete")

    @hybrid_property
    def data(self):
        """Decoding security data"""
        # TODO: Add data decoding
        return self._data

    @data.setter
    def data(self, raw_data):
        """Encoding security data"""
        # TODO: Add data encoding
        self._data = raw_data


class DocType(Base):
    """Doc's types
    Future: add validator by regular
    """
    __tablename__ = "doc_type"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False, unique=True)
    description = Column(String(200), default="")

    docs = relationship("Doc", backref="type", cascade="all, delete")
