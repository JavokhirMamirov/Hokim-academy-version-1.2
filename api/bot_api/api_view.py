from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view
from rest_framework.response import Response

from account.models import Student
from api.bot_api.serializers import MyCourseSerializer, QuizSerializer, QuizDetailSerializer
from course.models import WatchHistory, Quiz, QuizResult


@api_view(['GET'])
def get_quiz_result_view(request):
    try:
        quiz_id = request.GET('quiz_id')
        chat_id = request.GET.get('chat_id')
        student = Student.objects.get(chat_id=chat_id)
        query = QuizResult.objects.filter(quiz_id=quiz_id, is_passed=True).order_by('-mark')
        my_res = QuizResult.objects.filter(quiz_id=quiz_id, student=student, is_passed=True).last()
        order = list(query).index(my_res)
        data = {
            "order": order
        }
    except Exception as err:
        data = {
            "success": False,
            "error": f"{err}"
        }


@api_view(['GET'])
def quizView(request, pk=None):
    try:
        if pk is not None:
            chat_id = request.GET.get('chat_id')
            student = Student.objects.get(chat_id=chat_id)
            quiz = Quiz.objects.get(id=pk)
            ser = QuizDetailSerializer(quiz, context={"student": student})
            data = {
                "success": True,
                "data": ser.data
            }
        else:
            course_id = request.GET.get('course_id')
            # chat_id = request.GET.get('chat_id')
            # student = Student.objects.get(chat_id=chat_id)
            query = Quiz.objects.filter(course_id=course_id, is_active=True)
            ser = QuizSerializer(query, many=True)
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
def myCoursesView(request):
    try:
        chat_id = request.GET.get('chat_id')
        student = Student.objects.get(chat_id=chat_id)
        courses = WatchHistory.objects.filter(student=student)
        ser = MyCourseSerializer(courses, many=True)
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
def studentLoginView(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        chat_id = request.data.get('chat_id')
        try:
            student = Student.objects.get(chat_id=chat_id)
            student.chat_id = None
            student.save()
        except Student.DoesNotExist:
            pass
        user = authenticate(model=Student, username=username, password=password)
        if user is not None:
            if user.active == True:
                user.chat_id = chat_id
                user.save()
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
        chat_id = request.GET.get('chat_id')
        student = Student.objects.get(chat_id=chat_id)
        student.chat_id = None

        student.save()
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
