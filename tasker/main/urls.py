from django.conf.urls import url
from main.views import main_board
from main.views import RegView


app_name = 'main'


urlpatterns = [
    url('^registration/$', RegView.as_view(), name='invited_user_registration'),
    url('', main_board, name='main_board'),
]
