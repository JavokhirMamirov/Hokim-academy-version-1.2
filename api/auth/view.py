from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from account.models import Student


@api_view(['POST'])

def get_tokens_for_user(request):
    username = request.data['username']
    password = request.data['password']
    student = Student.objects.get(username=username, promo_code=password)
    refresh = RefreshToken.for_user(student)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_view(request):
    return Response({'success':True})