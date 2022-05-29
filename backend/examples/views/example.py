import random

from django.db.models import F
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from examples.filters import ExampleFilter
from examples.models import Example
from examples.serializers import ExampleSerializer
from projects.models import Project
from projects.permissions import IsProjectAdmin, IsProjectStaffAndReadOnly


class ExampleList(generics.ListCreateAPIView):
    serializer_class = ExampleSerializer
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = ("created_at", "updated_at")
    search_fields = ("text", "filename")
    model = Example
    filter_class = ExampleFilter

    @property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs["project_id"])

    def get_queryset(self):
        queryset = self.model.objects.filter(project=self.project)
        member = self.request.user.role_mappings.filter(project_id=self.project.id).first()
        if member.role.name == "annotator":
            queryset = queryset.filter(assigned_to_annotator=member, states__confirmed_at=None)
        elif member.role.name == "annotation_approver":
            queryset = queryset.filter(assigned_to_approval=member).exclude(states__confirmed_at=None)
        if self.project.random_order:
            # Todo: fix the algorithm.
            random.seed(self.request.user.id)
            value = random.randrange(2, 20)
            queryset = queryset.annotate(sort_id=F("id") % value).order_by("sort_id", "id")
        else:
            queryset = queryset.order_by("created_at")
        return queryset

    def perform_create(self, serializer):
        serializer.save(project=self.project)

    def delete(self, request, *args, **kwargs):
        queryset = self.project.examples
        delete_ids = request.data["ids"]
        if delete_ids:
            queryset.filter(pk__in=delete_ids).delete()
        else:
            queryset.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExampleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Example.objects.all()
    serializer_class = ExampleSerializer
    lookup_url_kwarg = "example_id"
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]
