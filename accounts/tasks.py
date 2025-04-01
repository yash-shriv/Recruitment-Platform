# 1 sending emails asynchronously using celery (async, scalable)

# https://www.reddit.com/r/django/comments/v45t65/do_i_need_celery_for_sending_emails/?rdt=62113
# https://docs.celeryq.dev/en/latest/django/first-steps-with-django.html
# https://github.com/celery/celery

# 11:10 pm 30 mar
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings

EMAIL_FROM = "noreply@yash-shriv-app.com"

@shared_task(bind=True)
def send_email(self, subject, email_to, html_template, context):
    """Asynchronous email sending task using Celery."""
    
    # Debugging logs to verify received parameters
    print(f"📩 Received subject: {subject}")
    print(f"📩 Received email_to: {email_to}")
    print(f"📩 Received html_template: {html_template}")
    print(f"📩 Received context: {context}")

    # Ensure email_to is always a list
    if isinstance(email_to, str):
        email_list = [email_to]  # Convert single string to list
    elif isinstance(email_to, list):
        email_list = email_to  # Keep as list
    else:
        print("❌ Error: Invalid email_to format!")
        raise TypeError("email_to should be a string or a list of emails.")

    try:
        # Load and render the email template
        html_template = get_template(html_template)
        html_alternative = html_template.render(context)

        # Prepare and send the email
        msg = EmailMultiAlternatives(
            subject=subject,
            from_email=EMAIL_FROM,
            to=email_list
        )
        msg.attach_alternative(html_alternative, "text/html")
        msg.send(fail_silently=False)

        print("✅ Email sent successfully!")

    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        raise e


# @shared_task(bind=True)
# def send_email(self, **kwargs):
#     """Asynchronous email sending task using Celery."""
    
#     # Extract required parameters
#     subject = kwargs.get('subject')
#     email_to = kwargs.get('email_to')
#     html_template = kwargs.get('html_template')
#     context = kwargs.get('context')

#     # Debugging logs to verify received parameters
#     print(f"📩 Received subject: {subject}")
#     print(f"📩 Received email_to: {email_to}")
#     print(f"📩 Received html_template: {html_template}")
#     print(f"📩 Received context: {context}")

#     # Validate required parameters
#     if not subject or not email_to or not html_template or not context:
#         print("❌ Error: Missing required parameters!")
#         raise ValueError("Missing required parameters!")

#     # Ensure email_to is always a list
#     if isinstance(email_to, str):
#         email_list = [email_to]  # Convert single string to list
#     elif isinstance(email_to, list):
#         email_list = email_to  # Keep as list
#     else:
#         print("❌ Error: Invalid email_to format!")
#         raise TypeError("email_to should be a string or a list of emails.")

#     try:
#         # Load and render the email template
#         html_template = get_template(html_template)
#         html_alternative = html_template.render(context)

#         # Prepare and send the email
#         msg = EmailMultiAlternatives(
#             subject=subject,
#             from_email=EMAIL_FROM,
#             to=email_list
#         )
#         msg.attach_alternative(html_alternative, "text/html")
#         msg.send(fail_silently=False)

#         print("✅ Email sent successfully!")

#     except Exception as e:
#         print(f"❌ Email sending failed: {e}")
#         raise e


"""
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_email(subject, recipient_list, template, context):
    # Sends an email using Django's send_mail function.
    message = f"Subject: {subject}\n\n{context}"  # Modify as per actual template rendering
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )
"""

# 11:08 pm 30mar
"""
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

EMAIL_FROM = "noreply@yash-shriv-app.com"

@shared_task(bind=True)
def send_email(self, subject=None, email_to=None, html_template=None, context=None):
    print(f"📩 Received subject: {subject}")
    print(f"📩 Received email_to: {email_to}")
    print(f"📩 Received html_template: {html_template}")
    print(f"📩 Received context: {context}")

    if not subject or not email_to or not html_template or not context:
        raise ValueError("Missing required parameters!")

    # Convert email_to from string back to list
    email_list = email_to.split(",") if isinstance(email_to, str) else email_to

    msg = EmailMultiAlternatives(
        subject=subject, from_email=EMAIL_FROM, to=email_list
    )
    html_template = get_template(html_template)
    html_alternative = html_template.render(context)
    msg.attach_alternative(html_alternative, "text/html")
    msg.send(fail_silently=False)

    print("✅ Email sent successfully!")
"""

# temp with debuub logs
"""
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

EMAIL_FROM = "noreply@yash-shriv-app.com"

@shared_task(bind=True)
def send_email(self, subject=None, email_to=None, html_template=None, context=None):
    print(f"Received subject: {subject}")
    print(f"Received email_to: {email_to}")
    print(f"Received html_template: {html_template}")
    print(f"Received context: {context}")

    if not all([subject, email_to, html_template, context]):
        raise ValueError("Missing required parameters!")

    msg = EmailMultiAlternatives(
        subject=subject, from_email=EMAIL_FROM, to=email_to
    )
    html_template = get_template(html_template)
    html_alternative = html_template.render(context)
    msg.attach_alternative(html_alternative, "text/html")
    msg.send(fail_silently=False)

    print("✅ Email sent successfully!")
"""


# current: Update celery task to use Gmail SMTP for async email sending

# from celery import shared_task
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.conf import settings

# @shared_task
# def send_email(subject, recipient_list, template, context):
#     """Send an email using Django EmailMultiAlternatives."""
#     html_content = render_to_string(template, context)  # Render HTML template
#     msg = EmailMultiAlternatives(
#         subject=subject,
#         body="This is an HTML email. Please enable HTML view.",  # Fallback text
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=recipient_list,
#     )
#     msg.attach_alternative(html_content, "text/html")  # Attach HTML version
#     msg.send(fail_silently=False)


"""
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

EMAIL_FROM ="noreply@yash-shriv-app.com"

@shared_task
def send_email(subject, email_to, html_template, context):
    msg = EmailMultiAlternatives(
        subject=subject, from_email=EMAIL_FROM, to=email_to
    )
    html_template = get_template(html_template)
    html_alternative = html_template.render(context)
    msg.attach_alternative(html_alternative, "text/html")
    msg.send(fail_silently=False)
"""

"""
Celery May Not Support Type Annotations (str, list[str])
Celery may be misinterpreting type hints like list[str], causing the unpacking error.

@shared_task
def send_email(subject: str, email_to: list[str], html_template, context):
    msg = EmailMultiAlternatives(
        subject=subject, from_email=EMAIL_FROM, to=email_to
    )
    html_template = get_template(html_template)
    html_alternative = html_template.render(context)
    msg.attach_alternative(html_alternative, "text/html")
    msg.send(fail_silently=False)
"""

# 2 synchronously using django send_mail()

# from django.core.mail import send_mail
# from django.conf import settings

# def send_email(subject, recipient_list, template, context):
#     """
#     Sends an email using Django's send_mail function (without Celery).
#     """
#     message = f"Subject: {subject}\n\n{context}"  # Modify as per actual template rendering
#     send_mail(
#         subject=subject,
#         message=message,
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         recipient_list=recipient_list,
#         fail_silently=False,
#     )

# 3 asynchronously using threading (basic async)

# https://stackoverflow.com/questions/17601698/can-you-perform-multi-threaded-tasks-within-django

# import threading
# from django.core.mail import send_mail
# from django.conf import settings

# def send_email_async(subject, recipient_list, template, context):
#     # Sends an email asynchronously using threading (without Celery).
#     def email_task():
#         message = f"Subject: {subject}\n\n{context}"  # Modify as per template rendering
#         send_mail(
#             subject=subject,
#             message=message,
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=recipient_list,
#             fail_silently=False,
#         )

#     email_thread = threading.Thread(target=email_task)
#     email_thread.start()
