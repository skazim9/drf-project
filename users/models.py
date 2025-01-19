from django.contrib.auth.models import AbstractUser
from django.db import models
from material.models import Course, Lesson


class User(AbstractUser):
    username = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Имя пользователя"
    )
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    phone = models.CharField(
        max_length=15, null=True, blank=True, verbose_name="Телефон"
    )
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name="Город")
    avatar = models.ImageField(
        upload_to="users/avatars/", null=True, blank=True, verbose_name="Аватар"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Payment(models.Model):
    PAYMENT_METHODS = [
        ("cash", "Наличными"),
        ("transfer", "Перевод на счет"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    paid_course = models.ForeignKey(
        Course, null=True, blank=True, on_delete=models.CASCADE
    )
    paid_lesson = models.ForeignKey(
        Lesson, null=True, blank=True, on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)

    def __str__(self):
        return f"Payment of {self.amount} by {self.user.email} on {self.payment_date}"