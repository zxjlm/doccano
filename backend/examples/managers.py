from django.db.models import Count, Manager


class ExampleManager(Manager):
    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        super().bulk_create(objs, batch_size=batch_size, ignore_conflicts=ignore_conflicts)
        uuids = [data.uuid for data in objs]
        examples = self.in_bulk(uuids, field_name="uuid")
        return [examples[uid] for uid in uuids]


class ExampleStateManager(Manager):
    def count_done(self, examples, user=None):
        if user:
            queryset = self.filter(example_id__in=examples, confirmed_by=user)
        else:
            queryset = self.filter(example_id__in=examples)
        return queryset.distinct().values("example").count()

    def measure_member_progress(self, examples, members):
        # done_count = (
        #     self.filter(example_id__in=examples).values("confirmed_by__username").annotate(total=Count("confirmed_by"))
        # )
        # response = {
        #     "progress": [{"user": obj["confirmed_by__username"], "done": obj["total"]} for obj in done_count],
        # }
        # members_with_progress = {o["confirmed_by__username"] for o in done_count}
        # for member in members:
        #     if member.username not in members_with_progress:
        #         response["progress"].append({"user": member.username, "done": 0})
        # return response
        done_count = (
            self.filter(example_id__in=examples).values("confirmed_by", "confirmed_by__username").annotate(
                total=Count("confirmed_by"))
        )
        approval_count = self.filter(example__in=examples).values("approved_by", "approved_by__username").annotate(
            total=Count("approved_by")
        )

        tmp_dic = {**{
            obj["confirmed_by"]: {"done": obj["total"]}
            for obj in done_count},
                   **{obj["approved_by"]: {"done": obj["total"]}
                      for obj in approval_count}}

        annotate_task_count = examples.values("assigned_to_annotator__user",
                                              "assigned_to_annotator__user__username").annotate(
            total=Count("assigned_to_annotator")
        )
        approval_task_count = examples.values("assigned_to_approval__user",
                                              "assigned_to_approval__user__username").annotate(
            total=Count("assigned_to_approval")
        )
        tmp_dic_1 = {**{
            obj["assigned_to_annotator__user"]: {"user": obj["assigned_to_annotator__user__username"], "total": obj["total"]}
            for obj in annotate_task_count},
                     **{obj["assigned_to_approval__user"]: {"user": obj["assigned_to_approval__user__username"],
                                                            "total": obj["total"]}
                        for obj in approval_task_count}}

        response = []
        for name, total_dic in tmp_dic_1.items():
            if name in tmp_dic:
                response.append({**tmp_dic[name], **total_dic})
            else:
                response.append({**{"done": 0}, **total_dic})
        return {"progress": response}
