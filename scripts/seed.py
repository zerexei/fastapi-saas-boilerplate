from core.database import async_session_factory
from core.logger import get_logger

logger = get_logger(__name__)


async def run_seed() -> None:
    """Executes initial database seeding during application startup."""
    async with async_session_factory() as db:
        try:
            logger.info("database_seeding_started")

            # TODO: Add your seed logic here (e.g., creating default roles or admin user)
            # existing_role = await db.scalar(select(Role).where(Role.name == "admin"))
            # if not existing_role:
            #     db.add(Role(name="admin"))

            await db.commit()
            logger.info("database_seeding_completed_successfully")
        except Exception as e:
            await db.rollback()
            logger.error("database_seeding_failed", error=str(e))
            raise
