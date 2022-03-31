from datetime import timedelta, datetime
from typing import List

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from . import exc
from .helpers import tr
from ..configs import JWT_SECRET
from ..models.users import User
from ..schemas import user_schema as us

_crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@tr
async def find_by_refs(ui: List[int] = None, ue: List[str] = None, db: Session = None):
    """Find user by refs: list ids or emails
    :param ui: User Ids it is optional value List[int]
    :param ue: User Emails it is optional value List[str]
    :param db: Database session
    :type ui: List[int]
    :type ue: List[str]
    :type db: Session
    :return: List of users
    :rtype: List[User]
    """

    return (
        db.execute(
            select(User).where(or_(User.id.in_(ui or []), User.email.in_(ue or [])))
        )
        .scalars()
        .all()
    )


@tr
async def create_user(user_data: us.UserReg, db: Session = None) -> us.User:
    """User registration
    :param user_data: New user data
    :type user_data: UserReg
    :param db: Database session
    :type db: Session
    :return: New User data
    :rtype: User
    :raises EmailAlreadyExists: if email already exists
    """
    if await find_by_refs(ue=[user_data.email], db=db):
        raise exc.EmailAlreadyExists("Email already exists")
    user = User(
        **user_data.dict(exclude={"password"}),
        hashed_password=_crypt_context.hash(user_data.password)
    )
    db.add(user)
    db.flush()
    return us.User.from_orm(user)


@tr
async def user_token(email: str, password: str, db: Session = None) -> us.AccessRef:
    """OAuth2 user by email and password
    :param email: User email
    :type email: str
    :param password: User password
    :type password: str
    :param db: Database session
    :type db: Session
    :return access_ref: Reference for authorization user by token
    :rtype: AccessRef
    :raise AuthError
    """
    assert isinstance(email, str), "email must be str"
    assert isinstance(password, str), "password must be str"

    u: User = db.execute(select(User).where(User.email == email)).scalar_one_or_none()

    if not u or not _crypt_context.verify(password, u.hashed_password):
        raise exc.AuthError("Auth error")

    return us.AccessRef(
        type="bearer",
        token=jwt.encode(
            {"exp": datetime.utcnow() + timedelta(days=60), "sub": str(u.id)},
            JWT_SECRET,
            algorithm="HS256",
        ),
    )


@tr
async def user_by_token(access_ref: us.AccessRef, db: Session = None):
    """Get user by token
    :param access_ref: Token for authorization
    :type: AccessToken
    :param db: Database session
    :type db: Session
    :return: User model
    :rtype: User
    :raises AuthError: If token error or user not found
    """
    assert access_ref.type.lower() == "bearer"

    try:
        user_id = int(
            jwt.decode(access_ref.token, JWT_SECRET, algorithms=["HS256"])["sub"]
        )
    except (jwt.JWTError, KeyError) as e:
        raise exc.AuthError(e)

    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if not user:
        raise exc.AuthError("User not found")
    return user


__all__ = ["find_by_refs", "user_token", "user_by_token"]
