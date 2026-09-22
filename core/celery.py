import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('sar_processing_engine')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Advanced Task Processing & Memory Management
app.conf.update(
    worker_prefetch_multiplier=1,           # Fair task distribution for heavy ML models
    task_acks_late=True,                     # Re-queue task if worker crashes
    worker_max_tasks_per_child=10,           # Restart worker process to free up GPU/RAM memory
    result_expires=86400,                    # Keep analysis results for 24 hours
    task_track_started=True,
)

app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def health_check_task(self):
    return {"status": "Celery Engine Working", "worker": self.request.hostname}