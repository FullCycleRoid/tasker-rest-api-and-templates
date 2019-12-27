from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# USER SECTION

# class User():
#     """New user model"""
#     pass

class UserProfile(models.Model):
    """User additional information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='user/profile_image', default='img/default_image.jpg')
    name = models.CharField(max_length=50)


# TASKBOARD SECTION


class Goal(models.Model):
    """User goals and preferred accomplishments"""
    title = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=2000)
    created_at = models.DateTimeField(editable=False)
    last_modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.pk:
            self.created_at = timezone.now()
        self.last_modified = timezone.now()
        return super().save(*args, **kwargs)


state = {
    'x': 'red',
    'done': 'green',
    'in_progress': 'purple'
}


class DailyTask(models.Model):
    """Daily task"""
    goals = models.ForeignKey('Goal', on_delete=models.PROTECT)
    condition = models.CharField(max_length=1, choices=state, default=state['x'])

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.pk:
            self.created_at = timezone.now()
        self.last_modified = timezone.now()
        return super().save(*args, **kwargs)


class Note(models.Model):
    """Useful redactor for notes"""
    name = models.CharField(max_length=20)
    body = models.TextField()


# RATING SYSTEM SECTION
class Rating(models.Model):
    """Implementation of rating system model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    month_achievement = models.CharField(max_length=50)


# COMMENTS SECTION
class Comment(models.Model):
    text = models.CharField(max_length=500)
    taskboard = models.ForeignKey('TaskBoard', on_delete=models.CASCADE)


# SCHEDULE SECTION
class Schedule():
    """"""
    pass
