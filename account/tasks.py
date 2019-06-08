from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger

from account.views import calculate_parent_bonus

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_calculate_bonus",
    ignore_result=True
)
def task_calculate_bonus():
    """
    Saves latest image from Flickr
    """
    # calculate_parent_bonus()
    logger.info("Saved image from Flickr")

