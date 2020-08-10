from __future__ import absolute_import, unicode_literals

from celery import shared_task

from django.conf import settings
from apps.blog_home_work.models import Posts

@shared_task
def delete_post_task():
    Posts.objects.filter(show_rubric=False).delete()


