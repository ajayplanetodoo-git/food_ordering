from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
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

    '''
    blow function used in tow way once user or vendor create send mail for activating user and when any one want to change 
    pasword then it also used
    '''
#     This function send vefication email
def send_varification_link(request,user,mail_subject,mail_template):
    from_email = settings.DEFAULT_FROM_EMAIL  # this will take email from .env metionded email
    current_site = get_current_site(request) # there it will take current site like http/8000  ect
    # mail_subject = "Please active you account"    
    messege = render_to_string(mail_template,{
        'user' :user,
        'domain' : current_site,
        "uid" : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : default_token_generator.make_token(user),
    })
    to_email =user.email
    mail = EmailMessage(mail_subject,messege, from_email,to=[to_email])
    mail.send()

    '''
    this function used for only send notifaication email when admin check is approved flag in vendor app from panal  
    apart from this it hot used in any case
    '''
def send_notification(mail_subject,mail_template,context):
    from_email = settings.DEFAULT_FROM_EMAIL
    messeage = render_to_string(mail_template,context)
    to_email = context['user'].email
    mail = EmailMessage(mail_subject,messeage, from_email,to=[to_email])
    mail.send()
