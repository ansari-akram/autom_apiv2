from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *
from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import check_password


# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer


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
