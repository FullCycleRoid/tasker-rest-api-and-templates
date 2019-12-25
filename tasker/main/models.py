from django.db import models
from django.utils import timezone

"User section"
class User():
    """New user model"""
    pass

class UserProfile(models.Model):
    """User additional information"""
    pass



"TASKBOARD SECTION"
state = {
    'x':'red',
    'done':'green',
    'in_progress': 'purple'
}

class TaskBoard(models.Model):
    """Main task board info"""
    name = models.CharField(max_length=40)
    # user = models.ForeignKey()
    description = models.TextField(max_length=2000)
    condition = models.CharField(max_length=1, choices=state, default=state['x'])
    created_at = models.DateTimeField()
    last_modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.pk:
            self.created_at = timezone.now()
        self.last_modified = timezone.now()
        return super().save(*args, **kwargs)


"""Rating system section"""
class Rating(models.Model):
    """Implementation of rating system model"""
    pass


"""Schedule section"""
class Schedule():
    """"""
    pass