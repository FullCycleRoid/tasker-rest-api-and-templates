from django.core.mail import send_mail
from tasker.settings import ALLOWED_HOSTS, DEFAULT_TO_EMAIL
from django.template.loader import render_to_string


def send_invite_notification(recipient_email, board_pk):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'

    context = {'user': recipient_email, 'host': host, 'board_pk': board_pk,
               'recipient_email': recipient_email}

    subject = render_to_string('email/add_new_user_letter_subject.txt',
                               context)
    body_text = render_to_string('email/add_new_user_letter_body.txt',
                                 context)

    send_mail(subject, body_text, DEFAULT_TO_EMAIL, [recipient_email,])

