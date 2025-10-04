from rest_framework import serializers, viewsets
from .models import Service

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
