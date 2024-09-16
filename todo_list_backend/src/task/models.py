from datetime import datetime

from django.db import models
from django.utils import timezone

from user.models import CustomUser


class Category(models.Model):
    id: str = models.CharField(max_length=160, primary_key=True)
    name: str = models.CharField(
        max_length=100,
        verbose_name='Наименование категории'
    )
    user: CustomUser = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = f'{self.user}_{self.name}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'],
                name='unique_user_category'
            )
        ]


class Task(models.Model):
    id: str = models.CharField(max_length=160, primary_key=True)
    title: str = models.CharField(max_length=250, verbose_name='Заголовок')
    content: str = models.TextField(blank=True, verbose_name='Текст')
    created: datetime = models.DateField(
        default=timezone.now().strftime("%Y-%m-%d")
    )
    due_date: datetime = models.DateField(
        default=timezone.now().strftime("%Y-%m-%d"),
        verbose_name='Дата завершения задачи'
    )
    category: Category = models.ForeignKey(
        Category, default="general",
        on_delete=models.PROTECT,
        verbose_name='Категория'
    )
    user: CustomUser = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = f'{self.user}_{self.title}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created']
