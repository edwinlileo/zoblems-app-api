from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from problem.models import Response, Problem

from problem.serializers import ResponseSerializer, ProblemSerializer


class BaseProblemAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, \
                             mixins.CreateModelMixin):
    """Base viewset for problem attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class ResponseViewSet(BaseProblemAttrViewSet):
    """Manage responses in the database"""
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer


class ProblemViewSet(BaseProblemAttrViewSet):
    """Manage problems in the database"""
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
