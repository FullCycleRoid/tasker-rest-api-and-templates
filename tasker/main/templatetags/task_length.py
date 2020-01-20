from django import template

register = template.Library()


def task_length(queryset):
    return list(set(item.t_duration for item in queryset if not item.t_duration == 1000))



register.filter('task_length', task_length)