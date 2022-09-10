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
from api.student_api.serializers import CourseHomeWithCategorySerializer, StudentSerializer, SearchCourseSerializer, \
    DetailCourseSerializer, MyCourseSerializer
from api.teacher_api.serializers import CourseGetSerializer
from course.models import Course, Category, Level, CourseStatus, WatchHistory


@api_view(['GET'])
@authentication_classes([StudentJwtAuthentication])
@permission_classes([IsAuthenticated])
def mycourseView(request):
    try:
        student = request.user
        query = WatchHistory.objects.filter(
            student=student
        )

        search = request.GET.get('search')
        category = request.GET.get('category')
        page = request.GET.get('page')

        if search is not None and search != "":
            query = query.filter(
                Q(title__icontains=search) | Q(short_description__icontains=search)
                | Q(teacher__full_name__icontains=search)
            )

        if category is not None and category != "":
            query = query.filter(category_id=category)

        if page == "":
            page = None

        data = {
            "success": True,
            "data": pagination_json(page, query, MyCourseSerializer, 9)
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
def detailCourseView(request, pk):
    try:
        course = Course.objects.get(id=pk)
        ser = DetailCourseSerializer(course)
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
def searchCourseView(request):
    try:
        student = request.user
        query = Course.objects.filter(Q(course_type=student.status) | Q(course_type=5), Q(step=7))

        search = request.GET.get('search')

        if search is not None and search != "":
            query = query.filter(
                Q(title__icontains=search)
            )

        data = {
            "success": True,
            "data": SearchCourseSerializer(query[:25], many=True).data
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
def checkUsernameView(request):
    try:
        username = request.GET.get('username')
        if username != request.user.username:
            students = Student.objects.filter(username=username)
            if students.count() > 0:
                data = {
                    "success": False,
                    "error": "Username already exist"
                }
            else:
                data = {
                    "success": True,
                    "error": ""
                }
        else:
            data = {
                "success": True,
                "error": ""
            }
    except Exception as err:
        data = {
            "success": False,
            "error": f"{err}"
        }

    return Response(data)


@api_view(['POST'])
@authentication_classes([StudentJwtAuthentication])
@permission_classes([IsAuthenticated])
def changeStudentImageView(request):
    try:
        student = request.user

        image = request.data.get('image')
        if image is not None:
            student.image = image
            student.save()

        ser = StudentSerializer(student)
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


@api_view(['GET', 'POST'])
@authentication_classes([StudentJwtAuthentication])
@permission_classes([IsAuthenticated])
def studentView(request):
    try:
        student = request.user
        st = Student.objects.get(id=student.id)
        if request.method == 'GET':
            ser = StudentSerializer(st)
            data = {
                "success": True,
                "data": ser.data
            }
        else:
            username = request.data.get('username')
            phone = request.data.get('phone')
            address = request.data.get('address')
            telegram = request.data.get('telegram')
            facebook = request.data.get('facebook')
            instagram = request.data.get('instagram')
            website = request.data.get('website')
            if username != student.username:
                students = Student.objects.filter(username=username)
                if students.count() > 0:
                    data = {
                        "success": False,
                        "status": 203,
                        "error": "Username already exist"
                    }
                    return Response(data)
                else:
                    student.username = username
            student.phone = phone
            student.phone = phone
            student.address = address
            student.telegram = telegram
            student.facebook = facebook
            student.instagram = instagram
            student.website = website

            student.save()

            ser = StudentSerializer(student)
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
def allCourseView(request):
    try:
        student = request.user
        query = Course.objects.filter(Q(course_type=student.status) | Q(course_type=5), Q(step=7))

        search = request.GET.get('search')
        level = request.GET.get('level')
        category = request.GET.get('category')
        status = request.GET.get('status')
        page = request.GET.get('page')

        if search is not None and search != "":
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
