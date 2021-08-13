from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views


app_name = 'dogger'

router = DefaultRouter()
router.register(r'dogs', views.DogsViewSet, basename='dogs')
router.register(r'schedule', views.ScheduleViewSet, basename='schedule')

urlpatterns = [
    path('api/v1/protected', views.protected, name='protected'),
    path('api/v1/', include(router.urls)),
]
