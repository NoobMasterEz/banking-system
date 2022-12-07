from __future__ import absolute_import, unicode_literals

from django.core.mail import EmailMultiAlternatives
from django.template import loader

from banking.schedule_task.celery import app, logger
from banking.module.users.models import User


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Setup and call send_reminders() every 60 seconds.
    pass


@app.task(serializer='json')
def send_email_reply(
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None):
    """
    ex. https://stackoverflow.com/questions/65004128/send-email-to-user-after-password-reset-in-django
    """
    user = User.objects.filter(email=to_email).first()
    if user:
        email = EmailMultiAlternatives(
            subject=subject_template_name,
            body=email_template_name,
            from_email=from_email,
            to=[user.email],
        )
        if html_email_template_name:
            html_email = loader.render_to_string(html_email_template_name, context)
            email.attach_alternative(html_email, "text/html")

        email.send()
        logger.info("sending Email...")
    else:
        logger.error('{0!r} failed: {1!r}'.format("Email Error", "can't sending email"))