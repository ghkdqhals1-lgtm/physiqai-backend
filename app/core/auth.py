from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.core.config import settings


def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    return jwt.encode(
        {"sub": str(user_id), "exp": expire},
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> int:
    payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    sub = payload.get("sub")
    if sub is None:
        raise ValueError("Missing subject in token")
    return int(sub)
