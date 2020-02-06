from django.urls import path
from .views import UserAPIView, TaskAPIView

urlpatterns = [
    path('users/', UserAPIView.as_view(), name='users_api'),
    path('tasks/', TaskAPIView.as_view(), name='tasks_api'),
    path('task/<int:pk>', TaskAPIView.as_view(), name='task_detail')
]