from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from django.template.defaultfilters import title
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import Teacher, Student
from api.admin_api.serializers import LanguageSerializer, CourseStatusSerializer, LevelSerializer, CategorySerializer, \
    TagSerializer
from api.auth.TeacherJWT import TeacherJwtAuthentication
from api.paginator import pagination_json
from api.student_api.serializers import DetailCourseSerializer
from api.teacher_api.serializers import CourseGetSerializer, CourseLessonsSerializer, LessonSerializer, \
    QuizGETSerializer, QuizPOSTSerializer, QuestionSerializer, CourseAttachmentSerializer, MyCourseSerializer, \
    MyStudentSerializer, TeacherProfileSerializer, CoursePostSerializer, CourseCommentGetSerializer, \
    CourseCommentPostSerializer
from course.models import Language, CourseStatus, Level, Category, Tag, Course, Section, Lesson, Quiz, Question, \
    CourseAttachment, WatchHistory, CourseComment


@api_view(['GET', 'POST'])
@authentication_classes([TeacherJwtAuthentication])
@permission_classes([IsAuthenticated])
def commentsView(request, pk):
    try:
        if request.method == "GET":
            page = request.GET.get('page')
            query = CourseComment.objects.filter(course_id=pk).order_by('-date_added')
            ser = CourseCommentGetSerializer(query, many=True)
            data = {
                "success": True,
                "data": pagination_json(page, query, CourseCommentGetSerializer, 10)
            }
        else:
            payload = request.data
            payload['teacher'] = request.user.id
            payload['course'] = pk
            ser = CourseCommentPostSerializer(data=payload)
            if ser.is_valid():
                ser.save()
                data = {
                    "success": True,
                    "data": ser.data
                }
            else:
                data = {
                    "success": False,
                    "error": f"{ser.errors}"
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
@authentication_classes([TeacherJwtAuthentication])
@permission_classes([IsAuthenticated])
def checkUsernameView(request):
    try:
        username = request.GET.get('username')
        if username != request.user.username:
            students = Teacher.objects.filter(username=username)
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
@authentication_classes([TeacherJwtAuthentication])
@permission_classes([IsAuthenticated])
def changeTeacherImageView(request):
    try:
        student = request.user

        image = request.data.get('image')
        if image is not None:
            student.image = image
            student.save()

        ser = TeacherProfileSerializer(student)
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
@authentication_classes([TeacherJwtAuthentication])
@permission_classes([IsAuthenticated])
def teacherView(request):
    try:
        student = request.user
        if request.method == 'GET':
            ser = TeacherProfileSerializer(student)
            data = {
                "success": True,
                "data": ser.data
            }
        else:
            username = request.data.get('username')
            email = request.data.get('email')
            telegram = request.data.get('telegram')
            facebook = request.data.get('facebook')
            instagram = request.data.get('instagram')
            website = request.data.get('website')
            biography = request.data.get('biography')
            title = request.data.get('title')
            full_name = request.data.get('full_name')
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
            student.full_name = full_name
            student.title = title
            student.telegram = telegram
            student.facebook = facebook
            student.instagram = instagram
            student.website = website
            student.email = email
            student.biography = biography

            student.save()

            ser = TeacherProfileSerializer(student)
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
def myDashboardView(request):
    try:
        query_s = WatchHistory.objects.filter(course__teacher=request.user)

        query = query_s.values('student_id')
        students = Student.objects.filter(id__in=query)

        course = Course.objects.filter(teacher=request.user)

        data = {
            "success": True,
            "data": {
                'course_count': course.count(),
                'student_count': query_s.count(),
                'students': MyStudentSerializer(students[:25], many=True).data
            }
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
def myStudentsView(request):
    try:
        query = WatchHistory.objects.filter(course__teacher=request.user)
        search = request.GET.get('search')
        course = request.GET.get('course')
        page = request.GET.get('page')

        if page == "":
            page = None

        if search is not None and search != "":
            query = query.filter(
                Q(student__full_name__icontains=search) | Q(student__school__name__icontains=search)
                | Q(course__title__icontains=search)
            )

        if course is not None and course != "":
            query = query.filter(course_id=course)

        query = query.values('student_id')
        students = Student.objects.filter(id__in=query)
        data = {
            "success": True,
            "data": pagination_json(page, students, MyStudentSerializer, 20)
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
def myCourseView(request, pk=None):
    try:
        if pk is None:
            query = Course.objects.filter(teacher=request.user)
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
                "data": pagination_json(page, query, MyCourseSerializer, 20)
            }
        else:
            query = Course.objects.get(id=pk)
            ser = CoursePostSerializer(query)
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


@api_view(['POST'])
@authentication_classes([TeacherJwtAuthentication])
@permission_classes([IsAuthenticated])
def changeCourseStep(request, pk):
    try:
        step = request.data['step']
        queries = Course.objects.get(id=pk)
        queries.step = step
        queries.save()
        ser = CourseGetSerializer(queries)
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


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([TeacherJwtAuthentication])
@permission_classes([IsAuthenticated])
def courseAttachmentView(request, pk=None):
    try:
        if request.method == 'GET':
            course = request.GET.get('course')
            query = CourseAttachment.objects.filter(course_id=course).order_by('order')
            ser = CourseAttachmentSerializer(query, many=True)
            data = {
                "success": True,
                "data": ser.data
            }
        elif request.method == 'POST':
            payload = request.data
            ser = CourseAttachmentSerializer(data=payload)
            if ser.is_valid():
                ser.save()
                data = {
                    "success": True,
                    "data": ser.data
                }
            else:
                data = {
                    "success": False,
                    "error": "Something is wrong!"
                }
        elif request.method == 'PUT':
            payload = request.data
            title = payload.get('title')
            course = payload.get('course')
            order = payload.get('order')
            file = payload.get('file')

            query = CourseAttachment.objects.get(id=pk)
            if file is not None:
                query.file = file

            query.title = title
            query.course_id = course
            query.order = order
            query.save()
            ser = CourseAttachmentSerializer(query)
            data = {
                "success": True,
                "data": ser.data
            }

        else:
            query = CourseAttachment.objects.get(id=pk)
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
def questionView(request, pk=None):
    try:
        if request.method == 'GET':
            quiz = request.GET.get('quiz')
            query = Question.objects.filter(quiz_id=quiz)
            ser = QuestionSerializer(query, many=True)
            data = {
                "success": True,
                "data": ser.data
            }
        elif request.method == 'POST':
            payload = request.data
            ser = QuestionSerializer(data=payload)
            if ser.is_valid():
                ser.save()
                data = {
                    "success": True,
                    "data": ser.data
                }
            else:
                data = {
                    "success": False,
                    "error": "Something is wrong!"
                }
        elif request.method == 'PUT':
            payload = request.data
            question = Question.objects.get(id=pk)
            ser = QuestionSerializer(instance=question, data=payload)
            if ser.is_valid():
                ser.save()
                data = {
                    "success": True,
                    "data": ser.data
                }
            else:
                data = {
                    "success": False,
                    "error": "Something is wrong!"
                }
        else:
            query = Question.objects.get(id=pk)
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
def quizView(request, pk=None):
    try:
        if request.method == 'GET':
            course = request.GET.get('course')
            query = Quiz.objects.filter(course_id=course)
            ser = QuizGETSerializer(query, many=True)
            data = {
                "success": True,
                "data": ser.data
            }
        elif request.method == 'POST':
            payload = request.data
            ser = QuizPOSTSerializer(data=payload)
            if ser.is_valid():
                ser.save()
                data = {
                    "success": True,
                    "data": ser.data
                }
            else:
                data = {
                    "success": False,
                    "error": "Something is wrong"
                }

        elif request.method == 'PUT':
            payload = request.data
            quiz = Quiz.objects.get(id=pk)
            ser = QuizPOSTSerializer(instance=quiz, data=payload)
            if ser.is_valid():
                ser.save()
                data = {
                    "success": True,
                    "data": ser.data
                }
            else:
                data = {
                    "success": False,
                    "error": "Something is wrong"
                }
        else:
            query = Quiz.objects.get(id=pk)
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
                query = Course.objects.get(teacher=request.user, step__lt=5)

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
            level = request.data['level']
            image = request.data['image']
            course_type = request.data['course_type']

            query = Course.objects.create(
                teacher=teacher, title=title, short_description=short_description,
                description=description, language_id=language, category_id=category, level_id=level,
                course_type=course_type,
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
            level = request.data['level']
            image = request.data.get('image')
            course_type = request.data['course_type']
            query.title = title
            query.short_description = short_description
            query.description = description
            query.language_id = language
            query.category_id = category
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
