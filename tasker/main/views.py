import datetime
import calendar
from django.contrib import messages
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from .forms import TaskForm, MarkForm, AddUserForm
from .models import TaskInfo, MainTaskBoard, AdvancedUser, Mark


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
    user_bord_pk = AdvancedUser.objects.get(pk=request.user.pk).board.pk
    main_board = MainTaskBoard.objects.get(pk=user_bord_pk)
    board_users = main_board.advanceduser_set.all()

    tasks = TaskInfo.objects.filter(author__in=board_users). \
        extra(select={'t_duration': 'CAST(t_duration AS INTEGER)'}).order_by('t_duration')

    user_count_tasks = TaskInfo.objects.filter(author__in=board_users).aggregate(
        Ежедневные=Count('pk', filter=Q(t_duration='1')),
        Еженедельные=Count('pk', filter=Q(t_duration='7')),
        Долгосрочные=Count('pk', filter=Q(t_duration='30')),
    )
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Новая задача добавлена')
            return redirect('main:main_board')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Какой то косяк. Сделай все как надо')
            return redirect('main:main_board')
    else:
        form = TaskForm(initial={'author': request.user.pk, 'main_board': main_board})
        mark_form = MarkForm()
        adduser_form = AddUserForm()

    context = {'board_users': board_users, 'main_board': main_board, 'month': month_days(),
               'days': current_month_days, 'utasks': tasks, 'form': form, 'user_count_tasks': user_count_tasks,
               'mark_form': mark_form, 'adduser_form': adduser_form}

    return render(request, 'main/main_board.html', context)
