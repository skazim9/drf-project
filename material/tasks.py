from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone


@shared_task
def send_email_task(to_email, subject, message):
    """Отправка письма пользователю, оформившего подписку"""
    send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email])


@shared_task
def deactivate_inactive_users():
    """Блокировка пользователей, не входивших в систему более месяца."""
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
    inactive_users.update(is_active=False)
