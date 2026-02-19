from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from app.models.refresh_token import RefreshToken


def create_refresh_token_row(db: Session, user_id: UUID, token_hash: str, jti: str, expires_at: datetime):
    row = RefreshToken(user_id=user_id, token_hash=token_hash, jti=jti, expires_at=expires_at)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_by_jti(db: Session, jti: str):
    return db.query(RefreshToken).filter(RefreshToken.jti == jti).first()


def revoke_by_jti(db: Session, jti: str, revoked_at: datetime):
    row = get_by_jti(db, jti=jti)
    if not row:
        return None
    row.revoked_at = revoked_at
    db.commit()
    db.refresh(row)
    return row