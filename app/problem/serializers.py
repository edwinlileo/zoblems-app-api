from rest_framework import serializers

from problem.models import Response


class ResponseSerializer(serializers.ModelSerializer):
    """Serializer for a response object"""

    class Meta:
        model = Response
        fields = ('id', 'description')
        read_only_fields = ('id',)
