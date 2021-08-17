from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views


app_name = 'dogger'

router = DefaultRouter()
router.register(r'dogs', views.DogsViewSet, basename='dogs')
router.register(r'schedule', views.ScheduleViewSet, basename='schedule')
router.register(r'reservation', views.ReservationViewSet, basename='reservation')

urlpatterns = [
    path('api/v1/walker/schedule/', views.walker_schedules, name='walker_schedules'),
    path('api/v1/', include(router.urls)),
]
