from rest_framework import serializers

from account.models import Region, City
from home.models import SchoolAriza, TeacherAriza


class SchoolArizaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolAriza
        fields = "__all__"


class TeacherArizaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAriza
        fields = "__all__"


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"
