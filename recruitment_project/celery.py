import os
from celery import Celery
from django.conf import settings

# Set default Django settings module for Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recruitment_project.settings")

app = Celery("recruitment_project")

# Load task modules from all registered Django app configs.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in Django apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, force=True)

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
