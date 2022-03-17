from sqlalchemy import Integer, String, Boolean, ForeignKey, Column, Text, Date, Table
from sqlalchemy.orm import relationship

from .base import Base

# org_user_association = Table(
#     "org_user_association",
#     Base.metadata,
#     Column("org_id", ForeignKey("org.id"), primary_key=True),
#     Column("user_id", ForeignKey("user.id"), primary_key=True),
# )


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

    # orgs = relationship("Org", secondary=org_user_association, backref="users")


class UserDoc(Base):
    """It's model for user's doc"""

    __tablename__ = "user_doc"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("user.id"))
    type_id = Column(ForeignKey("doc_type.id"))
    data = Column(Text)  # JSON data with structure
    file_id = Column(String(50))
    user = relationship("User", backref="docs")


class UserDocType(Base):
    """It's model for doc. Their may create organization"""

    __tablename__ = "doc_type"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    structure = Column(String(50), default="")
    file_type = Column(String(20), default="png")

    docs = relationship("UserDoc", backref="type")


__all__ = ["User"]
