import asyncio
import os
import sys

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import async_session_factory
from core.logger import get_logger
from core.security import get_password_hash
from domains.users.enums import UserRole
from domains.users.models import User

logger = get_logger(__name__)

FIRST_USER_EMAIL = os.getenv("SEED_ADMIN_EMAIL", "test@example.com")
FIRST_USER_PASSWORD = os.getenv("SEED_ADMIN_PASSWORD", "password")


async def seed_first_user(db: AsyncSession) -> None:
    existing_user = await db.scalar(select(User).where(User.email == FIRST_USER_EMAIL))
    if existing_user is None:
        db.add(
            User(
                email=FIRST_USER_EMAIL,
                hashed_password=get_password_hash(FIRST_USER_PASSWORD),
                is_active=True,
                role=UserRole.admin,
            )
        )


async def run_seed() -> None:
    """Standalone database seeding script."""
    logger.info("database_seed_script_initiated")

    async with async_session_factory() as db:
        try:
            await seed_first_user(db)
            await db.commit()
            logger.info("database_seed_completed_successfully")
        except Exception as e:
            await db.rollback()
            logger.error("database_seed_failed", error=str(e), exc_info=True)
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(run_seed())
