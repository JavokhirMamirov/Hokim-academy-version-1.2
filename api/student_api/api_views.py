from django.contrib.auth.hashers import check_password, make_password
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from api.auth.StudentJWT import StudentJwtAuthentication

from account.models import Student


@api_view(['PUT'])
@authentication_classes([StudentJwtAuthentication])
@permission_classes([IsAuthenticated])
def changePasswordAndUsernameFirstView(request):
    try:
        password = request.data.get('password')
        username = request.data.get('username')
        student = request.user
        if student.username != username:
            students = Student.objects.filter(username=username)
            if students.count() > 0:
                return Response({
                    "success": False,
                    "status": 205,
                    "error": "username already exist"
                })
            else:
                student.username = username
        student.password = make_password(password)
        student.is_used_promocode = True
        student.save()
        data = {
            "success": True,
            "status": 200,
            'user': {
                "id": student.id,
                "full_name": student.full_name,
                "username": student.username,
                "status": student.status,
                "is_used_promocode": student.is_used_promocode
            },
            "message": "Username and Password changed"
        }
    except Exception as err:
        data = {
            "success": False,
            "status": 500,
            "error": f"{err}"
        }
    return Response(data)


@api_view(['PUT'])
@authentication_classes([StudentJwtAuthentication])
@permission_classes([IsAuthenticated])
def changePasswordView(request):
    try:

        password = request.data.get('password')
        student = request.user
        student.password = make_password(password)
        student.save()
        data = {
            "success": True,
            "message": "Password changed"
        }
    except Exception as err:
        data = {
            "success": False,
            "error": f"{err}"
        }
    return Response(data)


@api_view(['POST'])
def studentLoginView(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(model=Student, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            data = {
                'success': True,
                'token':{
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'user': {
                    "id": user.id,
                    "full_name": user.full_name,
                    "username": user.username,
                    "status": user.status,
                    "is_used_promocode": user.is_used_promocode
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
    print(data)
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
