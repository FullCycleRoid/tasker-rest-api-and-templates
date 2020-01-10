from django.contrib import admin
from django.contrib.auth.models import User

from .models import MainTaskBoard, TaskInfo, Mark, AdvancedUser

admin.site.register(MainTaskBoard)
admin.site.register(TaskInfo)
admin.site.register(Mark)
admin.site.register(AdvancedUser)

