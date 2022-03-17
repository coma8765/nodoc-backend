# from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey, Boolean
# from sqlalchemy.orm import relationship
#
# from .base import Base
#
#
# org_member_association = Table(
#     "org_member_association",
#     Base.metadata,
#     Column("org_id", ForeignKey("org.id"), primary_key=True),
#     Column("member_id", ForeignKey("org_member.id"), primary_key=True),
# )
#
#
# class Org(Base):
#     __tablename__ = "org"
#
#     id = Column(Integer, primory_key=True)
#     title = Column(String, nullable=False)
#     description = Column(Text, default="")
#
#     members = relationship("OrgMember", secondary=org_member_association, backref="org")
#
#
# class OrgMember(Base):
#     __tablename__ = "org_member"
#
#     id = Column(Integer, primory_key=True)
#     email = Column(String, unique=True)
#     hashed_password = Column(String(40), nullable=False)
#     is_confirmed = Column(Boolean, default=False)
#
#
# class OrgRequestType(Base):
#     __tablename__ = "org_request_type"
#
#     id = Column(Integer, primory_key=True)
#     title = Column(String(200), nullable=False)
#     structure = Column(Text, nullable=False)
#     example_data = Column(Text, nullable=False)
