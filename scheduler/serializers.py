from rest_framework import serializers
from .models import ScheduleVisit
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class ScheduleVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleVisit
        fields = "__all__"
