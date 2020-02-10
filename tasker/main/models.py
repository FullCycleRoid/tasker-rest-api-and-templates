import datetime
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# USER SECTION
from django.utils import timezone


class AdvancedUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class AdvancedUser(AbstractBaseUser, PermissionsMixin):
    """User additional information"""

    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=50, blank=True, null=True)

    profile_image = models.ImageField(upload_to='user/profile_image', default='img/default_image.jpg')
    # is_activated = models.BooleanField(default=True, db_index=True,
    #                                    verbose_name='Прошел активацию')
    # send_messages = models.BooleanField(default=True,
    #                                     verbose_name='Слать оповещения о новых комментариях?')

    board = models.ForeignKey('MainTaskBoard', on_delete=models.CASCADE, blank=True, null=True, related_name='member')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AdvancedUserManager()

    def __str__(self):
        return self.email


# TASK BOARD SECTION
class MainTaskBoard(models.Model):
    board_name = models.CharField(max_length=50, verbose_name='Board Name')
    creator = models.OneToOneField(AdvancedUser, on_delete=models.CASCADE)
    created_at = models.DateField(editable=False, verbose_name='Creates')

    class Meta:
        verbose_name = 'Доска задач'
        verbose_name_plural = 'Доски задач'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = datetime.date.today()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.board_name


class TaskInfo(models.Model):
    duration = {
        ('9000', 'Бессрочные'),
        ('1', 'Ежедневные'),
        ('7', 'Еженедельные'),
        ('80', 'Долгосрочные')
    }

    main_board = models.ForeignKey(MainTaskBoard, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(max_length=2000, verbose_name='Дополнительное описание задачи', blank=True)
    author = models.ForeignKey(AdvancedUser, on_delete=models.CASCADE, verbose_name='Автор')
    t_duration = models.CharField(choices=duration, max_length=10, verbose_name='Длительность')
    created_at = models.DateField(editable=False, verbose_name='Создано')
    visible = models.BooleanField(default=True, verbose_name='Кто видит задачу? Только я/Все')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['author', 't_duration']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = datetime.date.today()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:detail', kwargs={'pk': self.pk})


class Mark(models.Model):
    status = (
        ('done', 'done'),
        ('undone', 'undone'),
        ('in_progress', 'in_progress')
    )

    task_info = models.ForeignKey(TaskInfo, on_delete=models.CASCADE)
    t_status = models.CharField(choices=status, default=status[1], max_length=50)
    created_at = models.DateField(editable=False)

    class Meta:
        verbose_name = 'Отметка'
        verbose_name_plural = 'Отметки'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = datetime.date.today()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.task_info.name}-{self.created_at}'


class Comment(models.Model):
    author = models.ForeignKey(AdvancedUser, on_delete=models.CASCADE)
    task = models.ForeignKey(TaskInfo, on_delete=models.CASCADE)
    name = models.TextField(max_length=500, verbose_name='Имя')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.name
