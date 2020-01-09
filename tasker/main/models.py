import datetime
from django.contrib.auth.models import  AbstractUser
from django.db import models
from django.utils import timezone


# USER SECTION
class AdvancedUser(AbstractUser):
    """User additional information"""
    profile_image = models.ImageField(upload_to='user/profile_image', default='img/default_image.jpg')

    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name='Прошел активацию')
    send_messages = models.BooleanField(default=True,
                                        verbose_name='Слать оповещения о новых комментариях?')

    class Meta(AbstractUser.Meta):
        pass


# TASKBOARD SECTION
class MainTaskBoard(models.Model):
    board_name = models.CharField(max_length=50, verbose_name='Назови доску задач', default='Task board')
    creator = models.OneToOneField(AdvancedUser, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')


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
    author = models.ForeignKey(AdvancedUser, on_delete=models.CASCADE, verbose_name='Автор')
    t_duration = models.CharField(choices=duration, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

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