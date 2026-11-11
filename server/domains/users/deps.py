from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user_email(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    """Extract and validate the user email claim from the Bearer token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(token)
    if not payload:
        raise credentials_exception
        
    email: str | None = payload.get("sub")
    if not email:
        raise credentials_exception
        
    return email


CurrentUserEmailDep = Annotated[str, Depends(get_current_user_email)]