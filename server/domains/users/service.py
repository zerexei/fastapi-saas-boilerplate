from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.cache import Cache, CacheDep
from core.security import get_password_hash
from domains.users.models import User
from domains.users.schemas import UserCreate


class UserService:
    def __init__(self, cache: Cache):
        self.cache = cache

    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        async def _fetch_from_db():
            result = await db.execute(select(User).where(User.email == email))
            return result.scalars().first()

        return await self.cache.get_or_set_with_lock(
            f"users:email:{email}",
            _fetch_from_db,
        )

    async def create(self, db: AsyncSession, user_in: UserCreate) -> User:
        db_user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            role=user_in.role,
        )
        db.add(db_user)
        await db.flush()
        await db.refresh(db_user)
        return db_user


def get_user_service(cache: CacheDep) -> UserService:
    return UserService(cache)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
