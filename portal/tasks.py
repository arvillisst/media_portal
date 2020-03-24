# Create your tasks here
# from __future__ import absolute_import, unicode_literals

from celery import shared_task
# from demoapp.models import Widget

# from celery import Celery
# from celery import task  

# celery = Celery('tasks', broker='redis://localhost:6379') #!

# import os

# os.environ['DJANGO_SETTINGS_MODULE'] = "config.settings"

# @task()
# def add_photos_task():
#     print('hello world')



@shared_task
def add(x, y):
    return x + y


# @shared_task
# def mul(x, y):
#     return x * y


# @shared_task
# def xsum(numbers):
#     return sum(numbers)


# @shared_task
# def count_widgets():
#     return Widget.objects.count()


# @shared_task
# def rename_widget(widget_id, name):
#     w = Widget.objects.get(id=widget_id)
#     w.name = name
#     w.save()