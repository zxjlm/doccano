<template>
  <v-data-table
    :value="value"
    :headers="headers"
    :items="items"
    :options.sync="options"
    :server-items-length="total"
    :search="search"
    :loading="isLoading"
    :loading-text="$t('generic.loading')"
    :no-data-text="$t('vuetify.noDataAvailable')"
    :footer-props="{
      showFirstLastPage: true,
      'items-per-page-options': [10, 50, 100],
      'items-per-page-text': $t('vuetify.itemsPerPageText'),
      'page-text': $t('dataset.pageText'),
    }"
    item-key="id"
    show-select
    @input="$emit('input', $event)"
  >
    <template #top>
      <v-container>
        <v-row>
          <v-col cols="12" md="4">
            <v-select
              v-model="confirmSelected"
              :items="confirmSelectedItems"
              label="是否已确认"
              item-text="hint"
              item-value="value"
            >
            </v-select>
          </v-col>

          <v-col cols="12" md="4">
            <v-select
              v-model="approveSelected"
              :items="approveSelectedItems"
              label="是否已审核"
              item-text="hint"
              item-value="value"
            >
            </v-select>
          </v-col>
        </v-row>
      </v-container>
      <v-text-field
        v-model="search"
        :prepend-inner-icon="mdiMagnify"
        :label="$t('generic.search')"
        single-line
        hide-details
        filled
      />
    </template>
    <template #[`item.text`]="{ item }">
      <span class="d-flex d-sm-none">{{ item.text | truncate(50) }}</span>
      <span class="d-none d-sm-flex">{{ item.text | truncate(200) }}</span>
    </template>
    //
    <template #[`item.meta`]="{ item }">
      // {{ JSON.stringify(item.meta, null, 4) }} //
    </template>
    <template #[`item.isConfirmed`]="{ item }">
      <span> {{ 1 ? item.isConfirmed : 0 }} </span>
    </template>
    <template #[`item.isApproved`]="{ item }">
      <span> {{ 1 ? item.isApproved : 0 }} </span>
    </template>
    //
    <template #[`item.commentCount`]="{ item }">
      // <span> {{ item.commentCount }} </span> //
    </template>
    <template #[`item.action`]="{ item }">
      <v-btn small color="primary text-capitalize" @click="toLabeling(item)">
        {{ $t("dataset.annotate") }}
      </v-btn>
    </template>
  </v-data-table>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { mdiMagnify } from "@mdi/js";
import { DataOptions } from "vuetify/types";
import { ExampleDTO } from "~/services/application/example/exampleData";

export default Vue.extend({
  props: {
    isLoading: {
      type: Boolean,
      default: false,
      required: true,
    },
    items: {
      type: Array as PropType<ExampleDTO[]>,
      default: () => [],
      required: true,
    },
    value: {
      type: Array as PropType<ExampleDTO[]>,
      default: () => [],
      required: true,
    },
    total: {
      type: Number,
      default: 0,
      required: true,
    },
  },

  data() {
    return {
      search: this.$route.query.q,
      confirmSelectedItems: [
        {
          hint: "已确认",
          value: 1,
        },
        {
          hint: "未确认",
          value: -1,
        },
        {
          hint: "不选择",
          value: 0,
        },
      ],
      confirmSelected: "",
      approveSelectedItems: [
        {
          hint: "已审核",
          value: 1,
        },
        {
          hint: "未审核",
          value: -1,
        },
        {
          hint: "不选择",
          value: 0,
        },
      ],
      approveSelected: "",
      options: {} as DataOptions,
      mdiMagnify,
    };
  },

  computed: {
    headers() {
      return [
        {
          text: this.$t("dataset.text"),
          value: "text",
          sortable: false,
        },
        // {
        //   text: this.$t("dataset.metadata"),
        //   value: "meta",
        //   sortable: false,
        // },
        {
          text: this.$t("annotation.isConfirmed"),
          value: "isConfirmed",
          sortable: false,
          filterable: true,
        },
        {
          text: this.$t("annotation.isApproved"),
          value: "isApproved",
          sortable: false,
          filterable: true,
        },
        // {
        //   text: this.$t("comments.comments"),
        //   value: "commentCount",
        //   sortable: false,
        // },
        {
          text: this.$t("dataset.action"),
          value: "action",
          sortable: false,
        },
      ];
    },
  },

  watch: {
    options: {
      handler() {
        this.$emit("update:query", {
          query: {
            limit: this.options.itemsPerPage.toString(),
            offset: (
              (this.options.page - 1) *
              this.options.itemsPerPage
            ).toString(),
            q: this.search,
            isConfirmed: this.confirmSelected,
            isApproved: this.approveSelected,
          },
        });
      },
      deep: true,
    },
    search() {
      this.$emit("update:query", {
        query: {
          limit: this.options.itemsPerPage.toString(),
          offset: "0",
          q: this.search,
          isConfirmed: this.confirmSelected,
          isApproved: this.approveSelected,
        },
      });
      this.options.page = 1;
    },
  },

  methods: {
    toLabeling(item: ExampleDTO) {
      const index = this.items.indexOf(item);
      const offset = (this.options.page - 1) * this.options.itemsPerPage;
      const page = (offset + index + 1).toString();
      this.$emit("click:labeling", {
        page,
        q: this.search,
        isConfirmed: this.confirmSelected,
        isApproved: this.approveSelected,
      });
    },
  },
});
</script>
