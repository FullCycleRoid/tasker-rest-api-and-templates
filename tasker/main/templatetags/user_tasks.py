from django import template

register = template.Library()


def user_tasks(queryset, user):


    return length


register.filter('user_tasks', user_tasks)