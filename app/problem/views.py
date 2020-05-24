from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from problem.models import Response

from problem.serializers import ResponseSerializer


class ResponseViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage responses in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
