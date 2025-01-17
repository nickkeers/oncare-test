from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .apiviews import ScheduleVisitViewSet

router = DefaultRouter()
router.register(r'schedule', ScheduleVisitViewSet, basename='schedule')

urlpatterns = [
    path('', include(router.urls)),
    # include this separately to handle latest
    path('schedule/latest/', ScheduleVisitViewSet.as_view({'get': 'latest'}), name='schedule-latest'),
    path('schedule/<int:pk>/<str:revision>/', ScheduleVisitViewSet.as_view({'get': 'visit_revision'}), name='schedule-visit-revision'),
    path('schedule/visit/<int:visit_id>/', ScheduleVisitViewSet.as_view({'put': 'update_visit'}), name='schedule-update-visit'),
]