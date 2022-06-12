<template>
  <v-card>
    <v-card-title>Assignment</v-card-title>
    <v-card-text>
      <v-list class="pt-0" dense>
        <v-list-item class="pa-0">
          <v-list-item-title>Annotator</v-list-item-title>
          <v-list-item-subtitle
            class="text-right"
            v-text="assignment.annotator"
          />
        </v-list-item>
        <v-list-item class="pa-0">
          <v-list-item-title>Approver</v-list-item-title>
          <v-list-item-subtitle
            class="text-right"
            v-text="assignment.approver"
          />
        </v-list-item>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ExampleAssignment } from "@/domain/models/example/example";

export default Vue.extend({
  props: {
    assignment: {
      type: Object as PropType<ExampleAssignment>,
      required: true,
    },
  },
});
</script>
