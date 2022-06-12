<template>
  <v-tooltip bottom>
    <template #activator="{ on }">
      <v-btn
        v-shortkey.once="['enter']"
        icon
        v-on="on"
        @shortkey="$emit('click:approval')"
        @click="$emit('click:approval')"
      >
        <v-icon v-if="isApproved">
          {{ mdiArchiveLock }}
        </v-icon>
        <v-icon v-else>
          {{ mdiArchiveLockOpen }}
        </v-icon>
      </v-btn>
    </template>
    <span v-if="isApproved">{{ $t("annotation.approvedTooltip") }}</span>
    <span v-else>{{ $t("annotation.notApprovedTooltip") }}</span>
  </v-tooltip>
</template>

<script lang="ts">
import Vue from "vue";
import { mdiArchiveLock, mdiArchiveLockOpen } from "@mdi/js";

export default Vue.extend({
  props: {
    isApproved: {
      type: Boolean,
      default: false,
      required: true,
    },
  },

  data() {
    return {
      mdiArchiveLockOpen,
      mdiArchiveLock,
    };
  },
});
</script>
