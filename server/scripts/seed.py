import asyncio
import sys

import structlog
from sqlalchemy import text

from core.database import async_session_factory

logger = structlog.get_logger(__name__)


async def run_seed() -> None:
    """Standalone database seeding script guarded by a Postgres advisory lock."""
    # 0x53454544 translates to ASCII 'SEED' in hex
    advisory_lock_id = 1397048644

    logger.info("database_seed_script_initiated")

    async with async_session_factory() as db:
        try:
            # Try to acquire a non-blocking advisory lock
            lock_acquired = await db.scalar(
                text("SELECT pg_try_advisory_lock(:lock_id)"), 
                {"lock_id": advisory_lock_id}
            )

            if not lock_acquired:
                logger.info("seeding_skipped_lock_held_by_another_process")
                return

            logger.info("seeding_lock_acquired_running_seeds")

            # --- Your actual database seeding logic goes here ---
            # Example:
            # await db.execute(
            #     text("INSERT INTO roles (name) VALUES ('admin'), ('user') ON CONFLICT DO NOTHING")
            # )
            # -------------------------------------------------------

            await db.commit()
            logger.info("database_seed_completed_successfully")

        except Exception as e:
            await db.rollback()
            logger.error("database_seed_failed", error=str(e), exc_info=True)
            sys.exit(1)
            
        finally:
            # Release the advisory lock if it was acquired
            try:
                await db.execute(
                    text("SELECT pg_advisory_unlock(:lock_id)"), 
                    {"lock_id": advisory_lock_id}
                )
                await db.commit()
            except Exception:
                pass


if __name__ == "__main__":
    # Run the async seeding function via asyncio
    asyncio.run(run_seed())