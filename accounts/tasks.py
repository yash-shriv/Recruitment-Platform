from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings

EMAIL_FROM = "noreply@yash-shriv-app.com"

@shared_task(bind=True)
def send_email(self, subject, email_to, html_template, context):
    # Ensure email_to is always a list
    if isinstance(email_to, str):
        email_list = [email_to]  # Convert single string to list
    elif isinstance(email_to, list):
        email_list = email_to  # Keep as list
    else:
        print("Error: Invalid email_to format!")
        raise TypeError("email_to should be a string or a list of emails.")
    try:
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

        print("Email sent successfully!")
    except Exception as e:
        print(f"Email sending failed: {e}")
        raise e
