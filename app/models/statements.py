from sqlalchemy import Column, Integer, ForeignKey, String, Text, Enum, DateTime, Boolean, func
from sqlalchemy.orm import relationship

from .base import Base
from ..schemas.statement_schema import StatementStatus


class Statement(Base):
    """Model for statement"""
    __tablename__ = "statement"

    user_id = Column(ForeignKey("user.id"), primary_key=True)
    type_id = Column(ForeignKey("statement_type.id"), primary_key=True)
    org_id = Column(ForeignKey("org.id"), primary_key=True)
    status = Column(Enum(StatementStatus), default=StatementStatus.PENDING)
    send_time = Column(DateTime, server_default=func.now())
    check_time = Column(DateTime)

    user = relationship("User", backref="statements")
    org = relationship("Org", backref="statements")


class StatementType(Base):
    """Model for statement type"""
    __tablename__ = "statement_type"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, default="")
    structure = Column(Text)
    icon_id = Column(String(50))

    statements = relationship("Statement", backref="type", cascade="all, delete")
    org_types = relationship("OrgType", secondary="statement_org", backref="statement_types")


class StatementOrg(Base):
    """Association model for statements from organizations"""
    __tablename__ = "statement_org"

    statement_type_id = Column(ForeignKey("statement_type.id"), primary_key=True)
    org_type_id = Column(ForeignKey("org_type.id"), primary_key=True)


class StatementDoc(Base):
    """Model of the required doc for obtaining statement"""
    __tablename__ = "statement_doc"

    statement_type_id = Column(ForeignKey("statement_type.id"), primary_key=True)
    doc_type_id = Column(ForeignKey("doc_type.id"), primary_key=True)
    obligatory = Column(Boolean, default=True)

    statement_type = relationship("StatementType", backref="docs", cascade="all, delete")
    doc_type = relationship("DocType", backref="statements", cascade="all, delete")

