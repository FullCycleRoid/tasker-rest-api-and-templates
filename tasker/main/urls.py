from django.conf.urls import url

from main.views import main_board

app_name = 'main'

urlpatterns = [
    url('', main_board, name='main_board'),
]