from django.shortcuts import render
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.filters import ApplicationFilterSet
from core.models import Application
from core.notifications import notify_user
from core.serializers import CoreApplicationSerializer
from push_notifications.models import GCMDevice


class ApplicationViewSet(viewsets.ModelViewSet):
    pagination_class = None
    permission_classes = [IsAuthenticated]
    queryset = Application.objects.all()
    serializer_class = CoreApplicationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ApplicationFilterSet

    def get_queryset(self):
        if self.request.user.airline_id:
            return super().get_queryset().filter(user__airline_id=self.request.user.airline_id)
        else:
            return super().get_queryset()

    def perform_update(self, serializer):
        return serializer.save(status=Application.ApplicationStatuses.EDITED_BY_AIRLINE)

    @swagger_auto_schema(method='get',
                         operation_description="GET /api/airline/applications/{id}/approve/")
    @action(methods=["get"], detail=True)
    def approve(self, *args, **kwargs):
        application = self.get_object()
        application.approve_by_airline()
        notify_user(application.user, "Ваша заявка одобрена авиакомпанией")
        return Response(status=204)

    @swagger_auto_schema(method='get', uto_schema=None,
                         operation_description="GET /api/airline/applications/{id}/refuse/")
    @action(methods=["get"], detail=True)
    def refuse(self, *args, **kwargs):
        application = self.get_object()
        application.refuse_by_airline()
        notify_user(application.user, "Ваша заявка отклонена авиакомпанией")
        return Response(status=204)
