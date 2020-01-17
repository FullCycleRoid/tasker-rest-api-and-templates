from django import template

register = template.Library()


def task_duration(queryset, arg):
    length = 0
    for q in queryset:
        if q.t_duration == arg:
            length += 1
    return length


register.filter('task_duration', task_duration)