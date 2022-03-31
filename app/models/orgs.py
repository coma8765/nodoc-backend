from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from .base import Base
from ..schemas.org_schema import MemberStatus


class Org(Base):
    """Org's model"""
    __tablename__ = "org"

    id = Column(Integer, primary_key=True)
    type_id = Column(ForeignKey("org_type.id"))
    title = Column(String(50), nullable=False)


class OrgType(Base):
    """Model with Types of orgs"""
    __tablename__ = "org_type"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False, unique=True)

    orgs = relationship("Org", backref="type", cascade="all, delete")


class OrgMember(Base):
    """Org's members"""
    __tablename__ = "org_member"

    org_id = Column(ForeignKey("org.id"), primary_key=True)
    user_id = Column(ForeignKey("user.id"), primary_key=True)
    status = Column(Enum(MemberStatus), default=MemberStatus.PENDING)

    org = relationship("Org", backref="members", cascade="all, delete")
    user = relationship("User", backref="orgs", cascade="all, delete")


__all__ = ["Org", "OrgType", "OrgMember"]
