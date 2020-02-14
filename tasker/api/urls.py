from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TaskAPIView, TaskDetailAPIView, UserViewSet, main_board_representation_view


api_router = DefaultRouter()
api_router.register(r'users', UserViewSet, 'users')

urlpatterns = [
    path('', include(api_router.urls)),
    path('main_board/', main_board_representation_view),
    path('tasks/<int:pk>', TaskDetailAPIView.as_view(), name='task_detail'),
    path('tasks/', TaskAPIView.as_view(), name='tasks_api'),
]