from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *
from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import check_password
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import uuid

SENDER = 'autom@haprotech.in'
SENDER_TITLE = "Autom Home Assistant"


def generateHTML(name, unique_id):
    _html = f"""
        <div style="font-family: Helvetica,Arial,sans-serif;min-width:700px;overflow:auto;line-height:2">
            <div style="margin:50px auto;width:600px;padding:20px 0">
                <div style="border-bottom:1px solid #eee">
                    <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">{name}</a>
                </div>
                <p style="font-size:1.1em">Hi,</p>
                <p>We received a request to reset your password. <br/>Your Unique code is:</p>
                <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{unique_id}</h2>
                <p style="font-size:0.9em;">
                    Copy and Paste this Unique Code in the App to verify and set new password.<br/>
                    <br/>
                    If you didn't request for password recovery, don't worry your account is absolutely safe. You can ignore this email.<br/>
                    <br/>
                    <br/>
                    Regards,
                    <br/>
                    Team <b>HA PROTECH</b>
                </p>
            </div>
        </div>"""
    return _html


@csrf_exempt
def register(request):

    try:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']

        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()

        ha_user = HAUser.objects.create(user=user, phone=phone)
        return JsonResponse({'200': f'user created {ha_user.user.username}'})

    except BaseException as e:
        return JsonResponse({"400": f'{str(e)}'})


@csrf_exempt
def login(request):
    try:
        user = User.objects.get(username=request.POST['username'])
        if check_password(request.POST['password'], user.password):
            ha_user = HAUser.objects.get(user=user)
            return JsonResponse({'200': ha_user.id, 'username': ha_user.user.username})
        else:
            return JsonResponse({'404': 'provide valid credentials'})
    except:
        return JsonResponse({'404': 'User not found.'})


@csrf_exempt
def forget_password(request):
    try:
        user = User.objects.get(username=request.POST['username'])
        recipient = user.email
        _uuid4 = str(uuid.uuid4())

        ha_user = HAUser.objects.get(user=user)
        ha_user.change_request = True
        ha_user.change_uuid = _uuid4
        ha_user.save()

        msg = MIMEText(generateHTML(user.username, _uuid4), 'html', 'utf-8')
        msg['Subject'] = Header("Password change request", 'utf-8')
        msg['From'] = formataddr((str(Header(SENDER_TITLE, 'utf-8')), SENDER))
        msg['To'] = recipient

        server = smtplib.SMTP_SSL('smtp.zoho.com', 465)
        server.login('autom@haprotech.in', 'fFvUeVBsqUbf')
        server.sendmail(SENDER, [recipient], msg.as_string())
        server.quit()

        return JsonResponse({'200': f'Email sent to {user.username}'})

    except:
        return JsonResponse({'404': 'User not found'})


@csrf_exempt
def set_password(request):
    try:
        user = User.objects.get(username=request.POST['username'])
        password = request.POST['password']
        uid = request.POST['uuid']

        ha_user = HAUser.objects.get(user=user)

        if ha_user.change_request and ha_user.change_uuid == uid:
            ha_user.change_request = False
            ha_user.change_uuid = ""
            ha_user.save()
            user.set_password(password)
            user.save()
            return JsonResponse({'201': 'Password set successfully'})
        
        else:
            return JsonResponse({'400': 'Password set failed'})

    except:
        return JsonResponse({'404': 'User not found.'})


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = HAUser.objects.all()
    serializer_class = HAUserSerializers


class MCU8ViewSet(viewsets.ModelViewSet):
    queryset = MCU8.objects.all()
    serializer_class = MCU8Serializer


class RoomDeviceViewSet(viewsets.ModelViewSet):
    queryset = RoomDevice.objects.all()
    serializer_class = RoomDeviceSerializer
