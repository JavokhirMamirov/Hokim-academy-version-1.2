from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view
from rest_framework.response import Response

from account.models import Student


@api_view(['POST'])
def studentLoginView(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        chat_id = request.data.get('chat_id')
        user = authenticate(model=Student, username=username, password=password)
        if user is not None:
            if user.active == True:
                user.chat_id = chat_id
                data = {
                    "success": True,
                    "data": {
                        "id": user.id,
                        "full_name": user.full_name,
                        "username": user.username,
                        "status": user.status,
                    }
                }
            else:
                data = {
                    "success": False,
                    "error": "Username or password error!"
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
def studentLogOut(request):
    try:
        user = request.user
        user.chat_id = None
        user.save()
        data = {
            "success": True
        }
    except:
        data = {
            "success": False
        }
    return Response(data)


def authenticate(model, username, password):
    try:
        user = model.objects.get(username=username)
        if check_password(password, user.password):
            return user
        else:
            return None
    except:
        return None
