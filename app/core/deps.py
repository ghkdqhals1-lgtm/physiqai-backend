from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.core.auth import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        return decode_access_token(token)
    except (JWTError, ValueError):
        raise exc
