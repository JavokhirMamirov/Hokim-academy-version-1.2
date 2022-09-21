from rest_framework.decorators import api_view
from rest_framework.response import Response

from account.models import Region, City
from api.website.serializers import SchoolArizaSerializer, TeacherArizaSerializer, RegionSerializer, CitySerializer


@api_view(['POST'])
def postSchoolAriza(request):
    try:
        payload = request.data
        ser = SchoolArizaSerializer(data=payload)
        if ser.is_valid():
            ser.save()
            data = {
                "success": True
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


@api_view(['POST'])
def postTeacherAriza(request):
    try:
        payload = request.data
        ser = TeacherArizaSerializer(data=payload)
        if ser.is_valid():
            ser.save()
            data = {
                "success": True
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
def regionView(request):
    try:
        query = Region.objects.all()
        ser = RegionSerializer(query, many=True)
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
def cityView(request):
    try:
        region = request.GET.get('region')
        query = City.objects.filter(region_id=region)
        ser = CitySerializer(query, many=True)
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
