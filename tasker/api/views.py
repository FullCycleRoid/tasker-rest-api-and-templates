from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView, UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .serializers import TaskSerializer, TaskDetailSerializer, MainBoardSerializer, UserSerializer
from main.models import TaskInfo, MainTaskBoard, AdvancedUser


class ListCreateUserAPIView(ListCreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserViewSet(ListModelMixin,
                 CreateModelMixin,
                 RetrieveModelMixin,
                 UpdateModelMixin,
                 GenericViewSet):

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]

class TaskAPIView(ListAPIView, CreateAPIView, RetrieveAPIView):
    queryset = TaskInfo.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        super(TaskAPIView, self).get_queryset()
        user = self.request.user.pk
        return TaskInfo.objects.filter(author=user)


class TaskDetailAPIView(RetrieveAPIView):
    queryset = TaskInfo.objects.all()
    serializer_class = TaskDetailSerializer


@login_required()
def main_board_representation_view(request):
    board_data = {
        'user': 'goo',
        "boo": "noo"
    }
    return JsonResponse(board_data)
