from django.urls import reverse
from django.conf import settings
from .models import EmailVerificationToken, User
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMessage
from accounts.translations import translations, allSettings

def sendEmail(user_email, subject, template, email_context):
    subject = subject
    html_content = render_to_string(template, email_context)
    text_content = strip_tags(html_content)

    email = EmailMessage(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [user_email]
    )
    email.content_subtype = 'html'
    if email.send(fail_silently=False) == 1:
        return True
    else:
        return False

def sendVerificationEmail(user):
    token, _ = EmailVerificationToken.objects.get_or_create(user_id=user)
    user = User.objects.get(id=user)
    verification_link = settings.SITE_URL + reverse('accounts:verifyRegistrationEmail', args=[token.token])
    email_context = {
        'verification_link': verification_link
    }
    emailSend = sendEmail(user.email, translations[allSettings.language]["subject_verification_email"], f"accounts/email/{allSettings.language}/verify_account.html", email_context)