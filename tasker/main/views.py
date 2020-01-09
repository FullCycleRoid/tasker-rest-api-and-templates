import datetime
from django.shortcuts import render
from .calendar import days_in_month
from .models import TaskInfo, DailyTask, MainTaskBoard


def main_board(request):
    month = datetime.datetime.now().strftime('%B')
    number_of_days = days_in_month(month)
    taskinfo = TaskInfo.objects.all()
    main = MainTaskBoard.objects.get(members=request.user.pk)
    context = {'days': range(number_of_days), 'task': taskinfo, 'month': month,
               'main': main}
    return render(request, 'main/main_board.html', context)