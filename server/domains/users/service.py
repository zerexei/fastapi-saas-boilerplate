from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.cache import Cache, CacheDep
from core.security import get_password_hash
from domains.users.models import User
from domains.users.schemas import UserCreate, UserRead


class UserService:
    def __init__(self, cache: Cache):
        self.cache = cache

    async def get_by_email(self, db: AsyncSession, email: str) -> UserRead | None:
        async def _fetch_from_db():
            stmt = select(User).where(User.email == email)
            result = await db.execute(stmt)
            return result.scalars().first()

        user = await self.cache.get_or_set_with_lock(
            f"users:email:{email}",
            _fetch_from_db,
        )

        return UserRead.model_validate(user) if user else None

    async def create(self, db: AsyncSession, user_in: UserCreate) -> UserRead:
        db_user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            role=user_in.role,
        )
        db.add(db_user)
        await db.flush()
        await db.refresh(db_user)
        return UserRead.model_validate(db_user)


def get_user_service(cache: CacheDep) -> UserService:
    return UserService(cache)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
