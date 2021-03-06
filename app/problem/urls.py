from django.urls import path, include
from rest_framework.routers import DefaultRouter

from problem import views


router = DefaultRouter()
router.register('responses', views.ResponseViewSet)
router.register('problems', views.ProblemViewSet)

app_name = 'problem'

urlpatterns = [
    path('', include(router.urls))
]
