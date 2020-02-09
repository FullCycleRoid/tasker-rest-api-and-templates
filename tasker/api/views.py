from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializers, TaskSerializer, TaskDetailSerializer, MainBoardSerializer
from main.models import TaskInfo, MainTaskBoard


class UserAPIView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializers

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


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


class MainBoardAPIView(GenericAPIView):
    queryset = MainTaskBoard.objects.all()
    serializer_class = MainBoardSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        print(self.queryset[0])
        if self.request.user.is_authenticated:
            queryset = self.queryset.get(creator=user)
            serializer = MainBoardSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            queryset = self.queryset[0]
            serializer = MainBoardSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)


