import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# USER SECTION
class UserProfile(models.Model):
    """User additional information"""
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    profile_image = models.ImageField(upload_to='user/profile_image', default='img/default_image.jpg')


# TASKBOARD SECTION
class MainTaskBoard(models.Model):
    board_name = models.CharField(max_length=50, verbose_name='Назови доску задач', default='Task board')
    creator = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    members = models.ManyToManyField(User, related_name='friends')

    class Meta:
        verbose_name = 'Доска задач'
        verbose_name_plural = 'Доски задач'


class TaskInfo(models.Model):
    duration = (
        ('day', 'day'),
        ('week', 'week'),
        ('long', 'long')
    )

    main_board = models.ForeignKey(MainTaskBoard, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='Задача')
    description = models.TextField(max_length=2000, verbose_name='Дополнительное описание задачи')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    t_duration = models.CharField(choices=duration, max_length=10)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class DailyTask(models.Model):
    status = (
         ('done', 'done'),
         ('undone', 'undone'),
         ('in_progress', 'in_progress')
    )

    task_info = models.ForeignKey(TaskInfo, on_delete=models.CASCADE)
    t_status = models.CharField(choices=status, default=status[1], max_length=50)
    created_at = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = 'Отметка'
        verbose_name_plural = 'Отметка'