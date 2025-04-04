"""Auth endpoints."""

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext  # type: ignore
from sqlalchemy.orm import Session

from backend_fastapi import data, endpoint_functions

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


auth_router = APIRouter()


@auth_router.post("/token")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: Annotated[Session, Depends(data.get_db_session)],
) -> dict[str, str]:
    """Get authentication bearer token."""
    user = endpoint_functions.get_user_by_name(db_session=db_session, username=form_data.username)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not _verify_password(plain_password=form_data.password, hashed_password=user.password):  # type: ignore
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    access_token = endpoint_functions.create_token(
        username=user.username,  # type: ignore
        user_id=user.user_id,  # type: ignore
        color=user.color,  # type: ignore
        expiration_time=timedelta(minutes=30),
    )

    return {"access_token": access_token, "token_type": "bearer"}


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain text password matches hashed password."""
    return PWD_CONTEXT.verify(plain_password, hashed_password)  # type: ignore
