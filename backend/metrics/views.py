import abc

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from examples.models import Example, ExampleState
from label_types.models import CategoryType, LabelType, RelationType, SpanType
from labels.models import Category, Label, Relation, Span
from projects.models import Member
from projects.permissions import IsProjectAdmin, IsProjectStaffAndReadOnly


class ProgressAPI(APIView):
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]

    def get(self, request, *args, **kwargs):
        member = Member.objects.filter(user=self.request.user, project_id=self.kwargs["project_id"]).first()
        if member.role.name == "annotator":
            examples = Example.objects.filter(project=self.kwargs["project_id"], assigned_to_annotator=member).values(
                "id")
        elif member.role.name == 'annotation_approver':
            examples = Example.objects.filter(project=self.kwargs["project_id"], assigned_to_approval=member).values(
                "id")
        else:
            examples = Example.objects.filter(project=self.kwargs["project_id"]).values("id")
        total = examples.count()
        complete = ExampleState.objects.count_done(examples, user=self.request.user)
        data = {"total": total, "remaining": total - complete, "complete": complete}
        return Response(data=data, status=status.HTTP_200_OK)


class MemberProgressAPI(APIView):
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]

    def get(self, request, *args, **kwargs):
        examples = Example.objects.filter(project=self.kwargs["project_id"]).values("id")
        members = Member.objects.filter(project=self.kwargs["project_id"])
        data = ExampleState.objects.measure_member_progress(examples, members)
        return Response(data=data, status=status.HTTP_200_OK)


class LabelDistribution(abc.ABC, APIView):
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]
    model = Label
    label_type = LabelType

    def get(self, request, *args, **kwargs):
        labels = self.label_type.objects.filter(project=self.kwargs["project_id"])
        examples = Example.objects.filter(project=self.kwargs["project_id"]).values("id")
        members = Member.objects.filter(project=self.kwargs["project_id"])
        data = self.model.objects.calc_label_distribution(examples, members, labels)
        return Response(data=data, status=status.HTTP_200_OK)


class CategoryTypeDistribution(LabelDistribution):
    model = Category
    label_type = CategoryType


class SpanTypeDistribution(LabelDistribution):
    model = Span
    label_type = SpanType


class RelationTypeDistribution(LabelDistribution):
    model = Relation
    label_type = RelationType
