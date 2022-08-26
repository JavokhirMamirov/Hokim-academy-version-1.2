from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.auth.CustomAdminPermission import CustomAdminPermission


class LanguageViewset(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomAdminPermission]
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()


class CourseStatusViewset(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomAdminPermission]
    serializer_class = CourseStatusSerializer
    queryset = CourseStatus.objects.all()


class LevelViewset(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomAdminPermission]
    serializer_class = LevelSerializer
    queryset = Level.objects.all()


class CategoryViewset(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomAdminPermission]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class SubCategoryViewset(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomAdminPermission]
    serializer_class = SubCategorySerialzier
    queryset = SubCategory.objects.all()


class TagViewset(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomAdminPermission]
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
