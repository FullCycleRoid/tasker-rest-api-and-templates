import datetime
from django.shortcuts import render
from .calendar import days_in_month
from .models import TaskInfo, MainTaskBoard


def main_board(request):
    month = datetime.datetime.now().strftime('%B')
    number_of_days = days_in_month(month)

    all_user_task = TaskInfo.objects.filter(author=request.user.pk)
    first_user_task = all_user_task.first()

    user_main_board_pk = first_user_task.main_board.pk
    main_board_obj = MainTaskBoard.objects.get(pk=user_main_board_pk)

    main_board_authors_pk = list(set(main_board_obj.taskinfo_set.all().
                                  values_list('author', flat=True)))

    all_board_tasks = TaskInfo.objects.filter(author__in=main_board_authors_pk)

    main_board = MainTaskBoard.objects.all()
    for item in main_board:
        if item
            my_main_board = item.taskinfo_set.filter(author=request.user.pk)

    print('my_board',my_main_board)

    duration = {
        'day': 'day',
        'week': 'week'
    }


    context = {'days': range(number_of_days), 'all_user_task': all_user_task, 'month': month,
               'first_user_task': first_user_task, 'all_board_tasks': all_board_tasks, 'duration': duration}
    return render(request, 'main/main_board.html', context)