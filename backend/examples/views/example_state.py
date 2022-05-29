from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from examples.models import Example, ExampleState
from examples.serializers import ExampleStateSerializer
from projects.models import Project, Member
from projects.permissions import IsProjectMember


class ExampleStateList(generics.ListCreateAPIView):
    serializer_class = ExampleStateSerializer
    permission_classes = [IsAuthenticated & IsProjectMember]

    @property
    def can_confirm_per_user(self):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        return not project.collaborative_annotation

    def get_queryset(self):
        queryset = ExampleState.objects.filter(example=self.kwargs["example_id"])
        if self.can_confirm_per_user:
            queryset = queryset.filter(confirmed_by=self.request.user)
        return queryset

    def perform_create(self, serializer):
        queryset = self.get_queryset()
        member = Member.objects.filter(project_id=self.kwargs["project_id"], user=self.request.user).first()
        type_ = self.request.data["type"]  # 0: confirm , 1: approve
        if not member:
            return
        if type_ == 0:
            if queryset.exists():
                queryset.delete()
            else:
                example = get_object_or_404(Example, pk=self.kwargs["example_id"])
                serializer.save(example=example, confirmed_by=self.request.user)
        elif member.role.name in ['annotation_approver', 'project_admin'] and type_ == 1:
            query_res = queryset.first()
            if not query_res:
                example = get_object_or_404(Example, pk=self.kwargs["example_id"])
                query_res = serializer.save(example=example, confirmed_by=self.request.user)
            if not query_res.approved_by:
                query_res.approved_by = self.request.user
            else:
                query_res.approved_by = None
            query_res.save()
