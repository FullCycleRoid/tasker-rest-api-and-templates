from django.conf.urls import url
from django.urls import path
from .views import main_board, TaskDetail, RegView, DeleteTaskView, \
    MyLoginView, MyLogoutView, RegistrationView, CreateBoardView, AccountUpdateView, InvitedUserRegistration

app_name = 'main'


urlpatterns = [
    url('^detail/(?P<pk>\d+)/$', TaskDetail.as_view(), name='detail'),
    path('create_board/', CreateBoardView.as_view(), name='create_board'),
    path('delete/<int:pk>', DeleteTaskView.as_view(), name='delete'),
    path('signin/', MyLoginView.as_view(), name='signin'),
    path('signout/', MyLogoutView.as_view(), name='signout'),
    path('account/', AccountUpdateView.as_view(), name='account'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('invite/', RegView.as_view(), name='invite_friend'),
    path('invited_user_registration/', InvitedUserRegistration.as_view(), name='invited_user_registration'),
    url('', main_board, name='main_board'),
]


