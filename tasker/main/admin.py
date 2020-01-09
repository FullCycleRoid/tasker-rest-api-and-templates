from django.contrib import admin
from .models import MainTaskBoard, TaskInfo, DailyTask

admin.site.register(MainTaskBoard)
admin.site.register(TaskInfo)
admin.site.register(DailyTask)

