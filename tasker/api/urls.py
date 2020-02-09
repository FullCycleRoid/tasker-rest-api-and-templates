from django.urls import path

from .views import UserAPIView, TaskAPIView, TaskDetailAPIView, MainBoardAPIView

urlpatterns = [
    path('users/', UserAPIView.as_view(), name='users_api'),
    path('tasks/<int:pk>', TaskDetailAPIView.as_view(), name='task_detail'),
    path('main_board/', MainBoardAPIView.as_view(), name='main_board'),
    path('tasks/', TaskAPIView.as_view(), name='tasks_api'),
]