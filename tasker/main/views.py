import datetime
import calendar
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView, DetailView, TemplateView, DeleteView, CreateView

from .forms import TaskForm, MarkForm, AddUserForm, TaskDetailForm, RegistrationForm, CustomUserChangeForm, \
    InvitedUserCreationForm
from .models import TaskInfo, MainTaskBoard, AdvancedUser
from .utilities import send_invite_notification


def month_days():
    m = datetime.datetime.now().strftime('%m')
    y = datetime.datetime.now().strftime('%Y')
    return calendar.monthrange(int(y), int(m[1]))[1]


def current_month_days():
    start_month = datetime.datetime.today().replace(day=1)
    date_list = []
    days = 0
    m = datetime.datetime.now().strftime('%m')
    y = datetime.datetime.now().strftime('%Y')
    for item in range(calendar.monthrange(int(y), int(m[1]))[1]):
        date_list.append(start_month + datetime.timedelta(days=days))
        days += 1
    return date_list


class UnregistredBoardVew():
    pass


@login_required()
def main_board(request):
    try:
        main_board = MainTaskBoard.objects.get(creator=request.user)

        board_users = [user for user in main_board.member.all()]
        board_users.insert(0, main_board.creator)

        board_users_id = [user.id for user in board_users]
        tasks = TaskInfo.objects.filter(author__in=board_users_id)
    except ObjectDoesNotExist:
        return redirect('main:create_board')

    if request.method == 'POST' and 'main_board' in request.POST:
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'New task successfully added')
            return redirect('main:main_board')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Ops, new task not added.'
                                 'Something goes wrong. Please do all right.')
            return redirect('main:main_board')

    if request.method == 'POST' and 'email' in request.POST:
        adduser_form = AddUserForm(request.POST)

        if adduser_form.is_valid():
            messages.add_message(request, messages.SUCCESS,
                                 f'Invite sent to your friend {adduser_form.cleaned_data["email"]} email')

            send_invite_notification(adduser_form.cleaned_data['email'], main_board.pk)
            return redirect('main:invite_friend')

        else:
            messages.add_message(request, messages.ERROR,
                                 f'Invite didn\'t send to your friend  {adduser_form.cleaned_data["email"]} email')

            return redirect('main:main_board')

    else:

        form = TaskForm(initial={'author': request.user.pk, 'main_board': main_board})
        mark_form = MarkForm()
        adduser_form = AddUserForm()

    context = {'board_users': board_users, 'main_board': main_board, 'month': month_days(), 'days': current_month_days,
               'utasks': tasks, 'form': form, 'mark_form': mark_form, 'adduser_form': adduser_form}

    return render(request, 'main/main_board.html', context)


class RegView(TemplateView):
    template_name = 'main/send_invite_notification.html'


class TaskDetail(DetailView, UpdateView):
    model = TaskInfo
    template_name = 'main/detail_task.html'
    form_class = TaskDetailForm


class DeleteTaskView(DeleteView):
    model = TaskInfo
    template_name = 'main/delete_task.html'
    success_url = '/'


class MyLoginView(LoginView):
    template_name = 'main/login.html'


class MyLogoutView(LogoutView):
    template_name = 'main/logout.html'


class RegistrationView(CreateView):
    model = AdvancedUser
    form_class = RegistrationForm
    template_name = 'main/registration.html'
    success_url = '/'


class CreateBoardView(LoginRequiredMixin, CreateView):
    model = MainTaskBoard
    template_name = 'main/create_board.html'
    fields = ('board_name',)
    success_url = '/'

    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            self.object.creator = self.request.user
            return super(CreateBoardView, self).form_valid(form)
        except IntegrityError:
            return redirect('main:main_board')


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = AdvancedUser
    form_class = CustomUserChangeForm
    template_name = 'main/account.html'

    def get_object(self, queryset=None):
        obj = AdvancedUser.objects.filter(pk=self.request.user.pk).first()
        return obj


class InvitedUserRegistration(CreateView):
    model = AdvancedUser
    form_class = InvitedUserCreationForm
    template_name = 'main/invite_registration.html'
    success_url = '/'

    def get_query_params(self):
        url = self.request.build_absolute_uri()
        split_url = url.split('?')[1]
        return split_url

    def get_email(self):
        params = self.get_query_params()
        email = params.split('email=')[1]
        return email

    def get_board(self):
        params = self.get_query_params()
        board = params.split('board_pk=')[1].split('&')[0]
        obj = MainTaskBoard.objects.get(pk=board)
        return obj

    def get_initial(self):
        self.initial['email'] = self.get_email()
        self.initial['board'] = self.get_board()
        print(self.initial)
        return self.initial


class RegistrationDone(TemplateView):
    template_name = 'main/registration_done.html'
