from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import include, re_path
from api import views

api_info = openapi.Info(
    title="Sdtest API",
    default_version='v1',
    description="Sdtest API",
)

schema_view = get_schema_view(
    public=False,
    permission_classes=(permissions.AllowAny,),
)
router = routers.SimpleRouter()
router.register(r'participant', views.ParticipantViewSet)

urlpatterns = [
    re_path(r'^rest-auth/', include('rest_auth.urls')),
    re_path(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    re_path(r'^participant/info/', views.ParticipantView.as_view()),
    re_path(r'^', include(router.urls)),
    re_path(r'^', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
