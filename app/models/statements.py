import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, Text, Enum, DateTime
from sqlalchemy.orm import relationship

from .base import Base
from ..schemas.statement_schema import StatementStatus


class Statement(Base):
    """Statements """
    __tablename__ = "statement"

    user_id = Column(ForeignKey("user.id"), primary_key=True)
    type_id = Column(ForeignKey("statement_type.id"), primary_key=True)
    status = Column(Enum(StatementStatus), default=StatementStatus.PENDING)
    send_time = Column(DateTime, default=datetime.datetime.now(tz=None))
    check_time = Column(DateTime)


class StatementType(Base):
    __tablename__ = "statement_type"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, default="")
    structure = Column(Text)
    icon_id = Column(String(50))

    statements = relationship("Statement", backref="type", cascade="all, delete")


class StatementOrg(Base):
    __tablename__ = "statement_org"

    statement_type_id = Column(ForeignKey("statement_type.id"), primary_key=True)
    org_type_id = Column(ForeignKey("org_type.id"), primary_key=True)

    type = relationship("StatementType", backref="orgs", cascade="all, delete")
