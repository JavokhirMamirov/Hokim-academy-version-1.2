from rest_framework import routers

from api.admin_api.viewsets import LanguageViewset, CourseStatusViewset, LevelViewset, CategoryViewset, TagViewset

router = routers.SimpleRouter()
router.register('language', LanguageViewset)
router.register('course-status', CourseStatusViewset)
router.register('level', LevelViewset)
router.register('category', CategoryViewset)
router.register('tag', TagViewset)
urlpatterns = router.urls
