# django_celery/celery.py
from django.db import transaction

from celery import Celery, Task
from celery.utils.log import get_task_logger


class AtomicTask(Task):
    def __call__(self, *args, **kwargs):
        with transaction.atomic():
            return super().__call__(*args, **kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error('{0!r} failed: {1!r}'.format(task_id, exc))


logger = get_task_logger(__name__)


app = Celery("django_celery")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
atomic_task = app.task(base=AtomicTask, serializer='json')
