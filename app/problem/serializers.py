from rest_framework import serializers

from problem.models import Response, Problem


class ResponseSerializer(serializers.ModelSerializer):
    """Serializer for a response object"""

    class Meta:
        model = Response
        fields = ('id', 'description', 'problem')
        read_only_fields = ('id',)


class ProblemSerializer(serializers.ModelSerializer):
    """Serializer for a problem object"""

    class Meta:
        model = Problem
        fields = ('id', 'title', 'accessUsers', 'responses')
        read_only_fields = ('id',)
