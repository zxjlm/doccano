"""
@author: harumonia
@license: © Copyright 2022, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@homepage: https://harumonia.moe/
@file: utils.py
@time: 2022/5/11 20:17
@desc:
"""
from examples.models import Example
from projects.models import Member


def re_assign_annotator(project_id: int, is_all_resign=False):
    members = Member.objects.filter(project_id=project_id, role__name="annotator").all()

    if not members:
        return

    if is_all_resign:
        # 全量再分配
        examples = Example.objects.filter(annotations_approved_by=None).all()
        member_id_docs = {member.id: 0 for member in members}
    else:
        # 增量再分配
        examples = Example.objects.filter(annotations_approved_by=None, assigned_to_annotator=None).all()
        member_id_docs = {member.id: member.assigned_annotation_examples.count() for member in members}

    for example in examples:
        # todo: 分配方案优化
        member_id_doc = min(member_id_docs.items(), key=lambda x: x[1])
        example.assigned_to_annotator_id = member_id_doc[0]
        member_id_docs[member_id_doc[0]] += 1
        example.save()


def re_assign_approver(project_id: int, is_all_resign=False):
    members = Member.objects.filter(project_id=project_id, role__name="annotation_approver").all()

    if not members:
        return

    if is_all_resign:
        # 全量再分配
        examples = Example.objects.filter(annotations_approved_by=None).all()
        member_id_docs = {member.id: 0 for member in members}
    else:
        # 增量再分配
        examples = Example.objects.filter(annotations_approved_by=None, assigned_to_approval=None).all()
        member_id_docs = {member.id: member.assigned_annotation_examples.count() for member in members}

    for example in examples:
        # todo: 分配方案优化
        member_id_doc = min(member_id_docs.items(), key=lambda x: x[1])
        example.assigned_to_approval_id = member_id_doc[0]
        member_id_docs[member_id_doc[0]] += 1
        example.save()

