from django.urls import path

from .views import user_api_view

urlpatterns = [
    path('', user_api_view, name='api_user_list_view')
]