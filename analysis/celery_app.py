# -*- coding: utf-8 -*-

from celery import Celery

celery_app = Celery('analysis_tasks')
celery_app.config_from_object('webspider.tasks.celery_config')