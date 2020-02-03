from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializers


@api_view(['GET', 'POST'])
def user_api_view(request):
    if request.method == 'GET':
        users = get_user_model().objects.all()
        serialisation = UserSerializers(users, many=True)
        return Response(serialisation.data, status=status.HTTP_200_OK)