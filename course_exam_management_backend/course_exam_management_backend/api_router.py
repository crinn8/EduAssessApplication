from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from courses.api.views import CourseViewSet, CourseFileViewSet
from users.api.views import UserViewSet
from quizes.api.views import QuizViewSet, DeliveredQuizViewSet, DeliveredQuizCreateApiView
from classes.api.views import ClassViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("courses", CourseViewSet)
router.register("quizes", QuizViewSet)
router.register("delivered_quiz", DeliveredQuizViewSet)
router.register("classes", ClassViewSet)
router.register("delivered-quizes", DeliveredQuizCreateApiView)
router.register("course-files", CourseFileViewSet)

app_name = "api"
urlpatterns = router.urls
