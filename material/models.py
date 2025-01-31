from django.conf import settings

from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name="Название")
    preview = models.ImageField(
        upload_to="materials/course_previews/",
        null=True,
        blank=True,
        verbose_name="Превью",
    )
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="courses",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name="Название")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    preview = models.ImageField(
        upload_to="materials/lesson_previews/",
        null=True,
        blank=True,
        verbose_name="Превью",
    )
    video_url = models.URLField(null=True, blank=True, verbose_name="Ссылка на видео")
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="lessons",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="subscriptions", on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course, related_name="subscriptions", on_delete=models.CASCADE
    )
    class Meta:
        unique_together = ("user", "course")
