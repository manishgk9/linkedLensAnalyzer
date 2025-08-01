from celery import Celery

celery_app = Celery(
    "LinkedLensAnalyzer",
    broker="redis://localhost:6379/0", 
    backend="redis://localhost:6379/0",
    include=['app.tasks']
)

# celery_app.autodiscover_tasks()
# Timezone (example)
celery_app.conf.update(
    enable_utc=True,
    timezone='UTC'
)