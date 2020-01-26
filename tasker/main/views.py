import datetime
import calendar
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, DetailView, UpdateView, DeleteView

from .forms import TaskForm, MarkForm, AddUserForm, TaskDetailForm
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


def main_board(request):


    if not request.user.is_authenticated:
        main_board = get_object_or_404(MainTaskBoard, pk=1)
    else:
        user_bord_pk = AdvancedUser.objects.get(pk=request.user.pk).board.pk
        main_board = MainTaskBoard.objects.get(pk=user_bord_pk)
        invited_by = request.user.username

    board_users = main_board.advanceduser_set.all()


    tasks = TaskInfo.objects.filter(author__in=board_users)

    user_count_tasks = TaskInfo.objects.filter(author__in=board_users).aggregate(
        Ежедневные=Count('pk', filter=Q(t_duration='1')),
        Еженедельные=Count('pk', filter=Q(t_duration='7')),
        Долгосрочные=Count('pk', filter=Q(t_duration='30')),
    )

    for item in request.POST:
        print(item)

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

            send_invite_notification(adduser_form.cleaned_data['email'], main_board.pk, invited_by)
            return redirect('main:main_board')

        else:
            messages.add_message(request, messages.ERROR,
                                 f'Invite didn\'t send to your friend  {adduser_form.cleaned_data["email"]} email')

            return redirect('main:main_board')

    else:

        form = TaskForm(initial={'author': request.user.pk, 'main_board': main_board})
        mark_form = MarkForm()
        adduser_form = AddUserForm()

    context = {'board_users': board_users, 'main_board': main_board, 'month': month_days(),
               'days': current_month_days, 'utasks': tasks, 'form': form, 'user_count_tasks': user_count_tasks,
               'mark_form': mark_form, 'adduser_form': adduser_form}

    return render(request, 'main/main_board.html', context)


class RegView(TemplateView):
    template_name = 'main/invited_user_registration.html'


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
