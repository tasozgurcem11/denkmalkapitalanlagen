from django.core import mail

from django_project.settings import EMAIL_HOST_USER


def send_pdf(receiver, attachment=None):
    sender = EMAIL_HOST_USER
    subject = "Kaiser & Dicke PDF"
    message = "Die von Ihnen angeforderte Datei angehängt ist."
    email = mail.EmailMessage(
        subject, message, sender, [receiver])

    if attachment:
        email.attach_file(attachment)

    email.send()
