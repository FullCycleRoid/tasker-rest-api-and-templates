from django.conf.urls import url
from main.views import main_board, TaskDetail, RegView

app_name = 'main'

urlpatterns = [
    url('^detail/(?P<pk>\d+)/$', TaskDetail.as_view(), name='detail'),
    url('^registration/$', RegView.as_view(), name='invited_user_registration'),
    url('', main_board, name='main_board'),
]

