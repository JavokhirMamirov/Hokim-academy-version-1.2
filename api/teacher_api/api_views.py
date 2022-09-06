from django.contrib.auth.hashers import check_password, make_password
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import Teacher
from api.admin_api.serializers import LanguageSerializer, CourseStatusSerializer, LevelSerializer, CategorySerializer, \
    SubCategorySerialzier, TagSerializer
from api.auth.TeacherJWT import TeacherJwtAuthentication
from api.teacher_api.serializers import CourseGetSerializer, CourseLessonsSerializer, LessonSerializer
from course.models import Language, CourseStatus, Level, Category, SubCategory, Tag, Course, Section, Lesson


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([TeacherJwtAuthentication])
@permission_classes([IsAuthenticated])
def lessonView(request, pk=None):
    try:
        if request.method == 'GET':
            section = request.GET.get('section')
            query = Lesson.objects.filter(section_id=section)
            ser = LessonSerializer(query, many=True)
            data = {
                "success": True,
                "data": ser.data
            }
        elif request.method == 'POST':
            title = request.data['title']
            section = request.data['section']
            video_type = request.data['video_type']
            video = request.data['video']
            summary = request.data['summary']
            time = request.data['time']
            order = request.data['order']

            query = Lesson.objects.create(
                title=title, section_id=section, video_type=video_type,
                video=video, summary=summary, time=time,
                order=order
            )

            ser = LessonSerializer(query)
            data = {
                "success": True,
                "data": ser.data
            }

        elif request.method == 'PUT':
            title = request.data['title']
            section = request.data['section']
            video_type = request.data['video_type']
            video = request.data['video']
            summary = request.data['summary']
            time = request.data['time']
            order = request.data['order']
            query = Lesson.objects.get(id=pk)
            query.title = title
            query.order = order
            query.section_id = section
            query.video_type = video_type
            query.video = video
            query.summary = summary
            query.time = time
            query.save()
            ser = LessonSerializer(query)
            data = {
                "success": True,
                "data": ser.data
            }
        else:
            query = Lesson.objects.get(id=pk)
            query.delete()
            data = {
                "success": True,
                "data": pk
            }
    except Exception as err:
        data = {
            "success": False,
            "error": f"{err}"
        }
    return Response(data)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([TeacherJwtAuthentication])
@permission_classes([IsAuthenticated])
def sectionView(request, pk=None):
    try:
        if request.method == 'GET':
            course = request.GET.get('course')
            query = Section.objects.filter(course_id=course)
            ser = CourseLessonsSerializer(query, many=True)
            data = {
                "success": True,
                "data": ser.data
            }
        elif request.method == 'POST':
            title = request.data['title']
            course = request.data['course']
            order = request.data['order']

            query = Section.objects.create(
                title=title, course_id=course, order=order
            )

            ser = CourseLessonsSerializer(query)
            data = {
                "success": True,
                "data": ser.data
            }

        elif request.method == 'PUT':
            title = request.data['title']
            order = request.data['order']
            query = Section.objects.get(id=pk)
            query.title = title
            query.order = order
            query.save()
            ser = CourseLessonsSerializer(query)
            data = {
                "success": True,
                "data": ser.data
            }
        else:
            query = Section.objects.get(id=pk)
            query.delete()
            data = {
                "success": True,
                "data": pk
            }
    except Exception as err:
        data = {
            "success": False,
            "error": f"{err}"
        }
    return Response(data)


@api_view(['POST', 'GET', 'PUT'])
@authentication_classes([TeacherJwtAuthentication])
@permission_classes([IsAuthenticated])
def courseView(request, pk=None):
    try:
        if request.method == 'GET':
            if pk is not None:
                query = Course.objects.get(id=pk)
            else:
                query = Course.objects.get(teacher=request.user, step__lt=6)

            ser = CourseGetSerializer(query)
            data = {
                "success": True,
                "data": ser.data
            }

        elif request.method == 'POST':
            teacher = request.user
            title = request.data['title']
            short_description = request.data['short_description']
            description = request.data['description']
            language = request.data['language']
            category = request.data['category']
            sub_category = request.data['sub_category']
            level = request.data['level']
            image = request.data['image']
            course_type = request.data['course_type']

            query = Course.objects.create(
                teacher=teacher, title=title, short_description=short_description,
                description=description, language_id=language, category_id=category,
                sub_category_id=sub_category, level_id=level, course_type=course_type,
                image=image
            )
            ser = CourseGetSerializer(query)
            data = {
                "success": True,
                "data": ser.data
            }
        elif request.method == "PUT":
            query = Course.objects.get(id=pk)
            title = request.data['title']
            short_description = request.data['short_description']
            description = request.data['description']
            language = request.data['language']
            category = request.data['category']
            sub_category = request.data['sub_category']
            level = request.data['level']
            image = request.data.get('image')
            course_type = request.data['course_type']
            query.title = title
            query.short_description = short_description
            query.description = description
            query.language_id = language
            query.category_id = category
            query.sub_category_id = sub_category
            query.level_id = level
            query.course_type = course_type
            if image is not None:
                query.image = image
            query.save()
            ser = CourseGetSerializer(query)
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
@authentication_classes([TeacherJwtAuthentication])
@permission_classes([IsAuthenticated])
def languageView(request):
    try:
        queries = Language.objects.all()
        ser = LanguageSerializer(queries, many=True)
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
@authentication_classes([TeacherJwtAuthentication])
@permission_classes([IsAuthenticated])
def courseStatusView(request):
    try:
        queries = CourseStatus.objects.all()
        ser = CourseStatusSerializer(queries, many=True)
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
@authentication_classes([TeacherJwtAuthentication])
@permission_classes([IsAuthenticated])
def levelView(request):
    try:
        queries = Level.objects.all()
        ser = LevelSerializer(queries, many=True)
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
@authentication_classes([TeacherJwtAuthentication])
@permission_classes([IsAuthenticated])
def categoryView(request):
    try:
        queries = Category.objects.all()
        ser = CategorySerializer(queries, many=True)
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
@authentication_classes([TeacherJwtAuthentication])
@permission_classes([IsAuthenticated])
def subCategoryView(request):
    try:
        queries = SubCategory.objects.all()
        ser = SubCategorySerialzier(queries, many=True)
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
@authentication_classes([TeacherJwtAuthentication])
@permission_classes([IsAuthenticated])
def tagView(request):
    try:
        queries = Tag.objects.all()
        ser = TagSerializer(queries, many=True)
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


@api_view(['PUT'])
@authentication_classes([TeacherJwtAuthentication])
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
def teacherLoginView(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(model=Teacher, username=username, password=password)
        try:
            img = user.image.url
        except:
            img = None
        if user is not None:
            refresh = RefreshToken.for_user(user)
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
                    "image": img
                }
            }
            print(data)
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
