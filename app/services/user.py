from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.repositories.user import get_user_by_email, create_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def register_user(db: Session, email: str, password: str):
    existing = get_user_by_email(db, email)
    if existing:
        raise ValueError("EMAIL_TAKEN")

    hashed_password = hash_password(password)
    return create_user(db, email=email, hashed_password=hashed_password)


def login_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        raise ValueError("INVALID_CREDENTIALS")

    if not verify_password(password, user.hashed_password):
        raise ValueError("INVALID_CREDENTIALS")

    return user