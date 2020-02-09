from django.contrib.auth import get_user_model
from rest_framework import serializers
from main.models import TaskInfo, MainTaskBoard, AdvancedUser


class UserSerializers(serializers.ModelSerializer):
    """Serializer for the user objects"""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

        def create(self, validated_data):
            """Create a new user with encrypted password and return it"""
            return get_user_model().objects.create_user(**validated_data)

        def update(self, instance, validated_data):
            """Update a user, setting the password correctly and return it"""
            password = validated_data.pop('password', None)
            instance.model_method()
            user = super().update(instance, validated_data)

            if password:
                user.set_password(password)
                user.save()

            return user


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskInfo
        fields = ['name', 'author']


class TaskDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskInfo
        fields = ['main_board', 'name', 'author', 'description',
                  't_duration', 'created_at', 'author']


class MainBoardSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(queryset=AdvancedUser.objects.all())


    class Meta:
        model = MainTaskBoard
        fields = ['board_name', 'creator', 'created_at']