"""
URL configuration for course_exam_management_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static
from quizes.api.views import CompilePythonCodeAPIView, DeliveredQuizCreateApiView
from users.api.views import PasswordChangeView
from courses.api.views import CourseListAPIView

schema_view = get_schema_view(
    openapi.Info(
        title="Live Streaming API",
        default_version='v1',
        description="Live Streaming Api description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="dpnrawthapa@mail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    path("api/auth-token/", obtain_auth_token),
    path("api/", include("course_exam_management_backend.api_router")),
    path('api/compile_python/', CompilePythonCodeAPIView.as_view()),
    path('api/change-password/', PasswordChangeView.as_view(), name='change_password'),
    path('api/get-all-courses/', CourseListAPIView.as_view(), name='get_all_courses'),
    # path('api/delivered-quizes/', DeliveredQuizCreateApiView.as_view(), name='delivered-quizes'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        # urls for swagger
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
