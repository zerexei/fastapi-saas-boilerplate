from fastapi import APIRouter, HTTPException, status

from core.database import SessionDep, TxSessionDep
from domains.users.deps import CurrentUserEmailDep
from domains.users.schemas import UserCreate, UserRead
from domains.users.service import UserServiceDep

router = APIRouter(prefix="/users")


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    service: UserServiceDep,
    db: TxSessionDep,
):
    """Create a new user account within an atomic transaction boundary."""
    existing_user = await service.get_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered.",
        )
    return await service.create(db, user_in)


@router.get("/me", response_model=UserRead)
async def read_user_me(
    service: UserServiceDep,
    db: SessionDep,
    current_email: CurrentUserEmailDep,
):
    """Retrieve the currently authenticated user's profile."""
    user = await service.get_by_email(db, current_email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found.",
        )
    return user
