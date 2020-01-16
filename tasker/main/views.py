import datetime
from django.shortcuts import render
from .calendar import days_in_month
from .models import TaskInfo, MainTaskBoard, AdvancedUser





def main_board(request):
    days = days_in_month(datetime.datetime.now().strftime('%B'))

    user_bord_pk = AdvancedUser.objects.get(pk=request.user.pk).board.pk
    main_board = MainTaskBoard.objects.get(pk=user_bord_pk)
    board_users = main_board.advanceduser_set.all()

    users_pk = [pk.pk for pk in board_users]
    all_tasks = TaskInfo.objects.filter(author__in=users_pk)

    print(all_tasks)
    context = {'board_users': board_users, 'main_board': main_board,
               'days': range(days), 'all_tasks': all_tasks}
    return render(request, 'main/main_board.html', context)