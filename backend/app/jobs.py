# mypy: disable-error-code="import-untyped"

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from .auth.service import delete_inactive_tokens
from .constants import INVALID_TOKENS_CLEAN_UP_INTERVAL_SECONDS


def configure_auth_jobs(scheduler: AsyncIOScheduler) -> AsyncIOScheduler:
    scheduler.add_job(
        delete_inactive_tokens,
        trigger=IntervalTrigger(seconds=INVALID_TOKENS_CLEAN_UP_INTERVAL_SECONDS),
    )

    return scheduler


def schedule_jobs() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    configure_auth_jobs(scheduler)
    scheduler.start()

    return scheduler
