from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from account.models import Info, Prize
from api.admin_api.serializers import InfoSerializer, PrizeSerializer


@api_view(['POST'])
def admin_login_view(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            data = {
                'success': True,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    "name": user.get_full_name(),
                    "username": user.username,
                    "status": user.status
                }
            }
        else:
            data = {
                "success": False,
                "error": "Username or password error!"
            }

    except Exception as err:
        data = {
            "success": False,
            "error": err
        }
    return Response(data)


@api_view(['GET'])
def infoView(request):
    try:
        query = Info.objects.first()
        ser = InfoSerializer(query)
        data = {
            "success": True,
            "data": ser.data
        }
    except Exception as err:
        data = {
            "success": False,
            "error": f"{err}"
        }
    return Response(data)


@api_view(['GET'])
def prizeView(request):
    try:
        query = Prize.objects.filter(show=True).order_by('order')
        ser = PrizeSerializer(query)
        data = {
            "success": True,
            "data": ser.data
        }
    except Exception as err:
        data = {
            "success": False,
            "error": f"{err}"
        }
    return Response(data)
