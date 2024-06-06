from django.db.models import Max
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action

from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import ScheduleVisit
from .serializers import ScheduleVisitSerializer


class ScheduleVisitViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleVisitSerializer
    queryset = ScheduleVisit.objects.all()

    @action(detail=False, methods=['get'])
    def latest(self, request, *args, **kwargs):
        latest_revision = self.queryset.aggregate(Max('revision'))['revision__max']
        latest_visit = self.queryset.filter(revision=latest_revision).first()
        if latest_visit:
            serializer = self.get_serializer(latest_visit)
            return Response(serializer.data)
        else:
            return Response([], status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='(?P<revision>[^/.]+)')
    def visit_revision(self, request, revision=None):
        try:
            visit = self.queryset.get(revision=revision)
            serializer = self.get_serializer(visit)
            return Response(serializer.data)
        except ScheduleVisit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        max_revision = self.queryset.aggregate(Max('revision'))['revision__max'] or 0
        serializer.save(revision=max_revision + 1)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, methods=['put'], url_path='visit/(?P<visit_id>[^/.]+)')
    def update_visit(self, request, *args, **kwargs):
        visit_id = self.kwargs['visit_id']
        try:
            instance = self.queryset.get(pk=visit_id)
        except ScheduleVisit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        max_revision = self.queryset.aggregate(Max('revision'))['revision__max'] or 0

        new_instance = ScheduleVisit(
            start_date_time=serializer.validated_data['start_date_time'],
            end_date_time=serializer.validated_data['end_date_time'],
            client=serializer.validated_data['client'],
            carer=serializer.validated_data['carer'],
            revision=max_revision + 1
        )

        new_instance.save()

        return Response(self.get_serializer(new_instance).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        max_revision = self.queryset.aggregate(Max('revision'))['revision__max'] or 0
        new_instance = ScheduleVisit(
            start_date_time=instance.start_date_time,
            end_date_time=instance.end_date_time,
            client=instance.client,
            carer=instance.carer,
            revision=max_revision + 1
        )
        new_instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
