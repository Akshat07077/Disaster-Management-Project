from rest_framework import serializers
from . models import DisasterEvent, Report, Resource

class DisasterEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisasterEvent
        fields = "__all__"

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields= "__all__"

class ResourceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields="__all__"