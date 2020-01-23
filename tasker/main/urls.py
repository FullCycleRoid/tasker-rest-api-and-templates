from django.conf.urls import url
from django.urls import path
from main.views import main_board, TaskDetail, RegView, DeleteTaskView

app_name = 'main'

urlpatterns = [
    url('^detail/(?P<pk>\d+)/$', TaskDetail.as_view(), name='detail'),
    url('^registration/$', RegView.as_view(), name='invited_user_registration'),
    path('delete/<int:pk>/', DeleteTaskView.as_view(), name='delete'),
    url('', main_board, name='main_board'),
]

