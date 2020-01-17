import datetime
import calendar
from django.shortcuts import render
from .models import TaskInfo, MainTaskBoard, AdvancedUser, Mark


start_date = datetime.datetime.now().year
end_date = datetime.datetime.now().year + 1


def month_days():
    m = datetime.datetime.now().strftime('%m')
    y = datetime.datetime.now().strftime('%Y')
    return calendar.monthrange(int(y), int(m[1]))[1]


def main_board(request):

    user_bord_pk = AdvancedUser.objects.get(pk=request.user.pk).board.pk
    main_board = MainTaskBoard.objects.get(pk=user_bord_pk)
    board_users = main_board.advanceduser_set.all()

    users_pk = [pk.pk for pk in board_users]

    tasks_by_user = {}
    for pk in users_pk:
        tasks_by_user[str(pk)] = TaskInfo.objects.filter(author=pk).\
            extra(select={'t_duration': 'CAST(t_duration AS INTEGER)'}).order_by('t_duration')

    exact_user_task_marks = Mark.objects.filter(task_info__in)



    context = {'board_users': board_users, 'main_board': main_board,
               'days': month_days(), 'tasks_by_user': tasks_by_user}

    return render(request, 'main/main_board.html', context)