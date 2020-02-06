from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from .serializers import UserSerializers, TaskSerializers
from main.models import TaskInfo


class UserAPIView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializers

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TaskAPIView(ListAPIView, CreateAPIView, RetrieveAPIView):
    queryset = TaskInfo.objects.all()
    serializer_class = TaskSerializers
    # permission_classes = ['IsAuthenticated',]

    def get_queryset(self):
        super(TaskAPIView, self).get_queryset()
        user = self.request.user.pk
        return TaskInfo.objects.filter(author=user)

