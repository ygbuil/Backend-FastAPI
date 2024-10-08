"""Users endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status

from app import data, endpoint_functions
from app.data import NewUser, UserResponse, UserUpdateInfo

users_router = APIRouter(prefix="/users")


@users_router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_to_create: NewUser,
    db_session: Depends = Depends(data.get_db_session),  # noqa: B008
) -> dict:
    """Create user endpoint."""
    user = endpoint_functions.get_user_by_name(
        db_session=db_session,
        username=user_to_create.username,
    )

    if user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    return endpoint_functions.create_user(db_session=db_session, user_to_create=user_to_create)


@users_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, db_session: Depends = Depends(data.get_db_session)) -> dict:  # noqa: B008
    """Get user endpoint."""
    user = endpoint_functions.get_user_by_id(db_session=db_session, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


@users_router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: str,
    user_update_info: UserUpdateInfo,
    verified_user: Depends = Depends(endpoint_functions.get_verified_user),  # noqa: B008
    db_session: Depends = Depends(data.get_db_session),  # noqa: B008
) -> dict:
    """Update user endpoint."""
    try:
        user_to_update = endpoint_functions.get_user_by_id(db_session=db_session, user_id=user_id)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request") from exc

    if user_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if str(verified_user.user_id) != str(user_to_update.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    return endpoint_functions.update_user(db_session=db_session, user_update_info=user_update_info)


@users_router.delete("/{user_id}", response_model=UserResponse)
def delete_user(
    user_id: str,
    verified_user: Depends = Depends(endpoint_functions.get_verified_user),  # noqa: B008
    db_session: Depends = Depends(data.get_db_session),  # noqa: B008
) -> dict:
    """Delete user endpoint."""
    user_to_delete = endpoint_functions.get_user_by_id(db_session=db_session, user_id=user_id)

    if user_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if str(verified_user.user_id) != str(user_to_delete.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    return endpoint_functions.delete_user(db_session=db_session, user_id=user_to_delete.user_id)
