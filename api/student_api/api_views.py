from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.admin_api.serializers import CategorySerializer, LevelSerializer, CourseStatusSerializer
from api.auth.StudentJWT import StudentJwtAuthentication

from account.models import Student
from api.paginator import pagination_json
from api.student_api.serializers import CourseHomeWithCategorySerializer
from api.teacher_api.serializers import CourseGetSerializer
from course.models import Course, Category, Level, CourseStatus


@api_view(['GET'])
@authentication_classes([StudentJwtAuthentication])
@permission_classes([IsAuthenticated])
def allCourseView(request):
    try:
        student = request.user
        query = Course.objects.filter(course_type=student.status, step=7)

        search = request.GET.get('search')
        level = request.GET.get('level')
        category = request.GET.get('category')
        status = request.GET.get('status')
        page = request.GET.get('page')

        if search is not None:
            query = query.filter(
                Q(title__icontains=search) | Q(short_description__icontains=search)
                | Q(teacher__full_name__icontains=search)
            )

        if level is not None and level != "":
            query = query.filter(level_id=level)

        if category is not None and category != "":
            query = query.filter(category_id=category)

        if status is not None and status != "":
            query = query.filter(status_id=status)

        if page == "":
            page = None

        data = {
            "success": True,
            "data": pagination_json(page, query, CourseGetSerializer, 9)
        }
    except Exception as err:
        data = {
            "success": False,
            "error": f"{err}"
        }

    return Response(data)


@api_view(['GET'])
@authentication_classes([StudentJwtAuthentication])
@permission_classes([IsAuthenticated])
def levelView(request):
    try:
        cats = Level.objects.all()
        ser = LevelSerializer(cats, many=True)
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
@authentication_classes([StudentJwtAuthentication])
@permission_classes([IsAuthenticated])
def courseStatusView(request):
    try:
        cats = CourseStatus.objects.all()
        ser = CourseStatusSerializer(cats, many=True)
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
@authentication_classes([StudentJwtAuthentication])
@permission_classes([IsAuthenticated])
def categoryView(request):
    try:
        cats = Category.objects.filter(type=request.user.status)
        ser = CategorySerializer(cats, many=True)
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
@authentication_classes([StudentJwtAuthentication])
@permission_classes([IsAuthenticated])
def bestThreeAndRecomCourseView(request):
    try:
        user = request.user
        bestThree = Course.objects.filter(best_three=True, course_type=user.status, step=7)
        recommends = Course.objects.filter(is_recommended=True, course_type=user.status, step=7)
        category = Category.objects.filter(type=user.status)[:8]
        data = {
            "success": True,
            "data": {
                "three_course": CourseGetSerializer(bestThree[:3], many=True).data,
                "recommends": CourseGetSerializer(recommends[:12], many=True).data,
                "category": CourseHomeWithCategorySerializer(category, many=True).data
            }
        }
    except Exception as err:
        data = {
            "success": False,
            "error": f"{err}"
        }

    return Response(data)


@api_view(['PUT'])
@authentication_classes([StudentJwtAuthentication])
@permission_classes([IsAuthenticated])
def changePasswordAndUsernameFirstView(request):
    try:
        password = request.data.get('password')
        username = request.data.get('username')
        student = request.user
        try:
            img = student.image.url
        except:
            img = None
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
                "image": img,
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
            try:
                img = user.image.url
            except:
                img = None
            data = {
                'success': True,
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'user': {
                    "id": user.id,
                    "full_name": user.full_name,
                    "username": user.username,
                    "status": user.status,
                    "image": img,
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
