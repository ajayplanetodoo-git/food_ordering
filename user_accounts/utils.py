from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage ,send_mail
from django.conf import settings

'''
This is helper function to detectec user role
'''


def detectuser(user):
    if user.role == 1:
        redirectUrl = 'vendashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = "custdashboard"
        return redirectUrl
    elif user.role == None:
        redirectUrl = "/admin"
        return redirectUrl


#     This function send vefication email
def send_varification_link(request, user):
    current_site = get_current_site(request)
    mail_subject = "Please active you account"
    messege = render_to_string("user_accounts/emails/account_verfy_email.html", {
        'user': user,
        'domain': current_site.domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })

    to_email = user.email
    from_email = settings.EMAIL_HOST_USER

    mail = EmailMessage(mail_subject, messege, from_email, to=[to_email])
    mail.send()
    # Send email
    # send_mail(
    #     subject=mail_subject,
    #     message='',  # Empty because we use html_message
    #     from_email=settings.EMAIL_HOST_USER,
    #     recipient_list=[user.email],
    #     fail_silently=False,
    #     html_message=messege
    # )


