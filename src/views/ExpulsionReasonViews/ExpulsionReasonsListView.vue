<script setup>
import { useExpulsionReasonsStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { onMounted } from "vue";
import ExpulsionReasonsDataTable from "@/components/DataTables/ExpulsionReasonsDataTable.vue";
import { useUxStore } from "@/stores/ux.store";
import TheSpinner from "@/components/TheSpinner.vue";

const expulsionReasonsStore = useExpulsionReasonsStore();
const { expulsionReasons } = storeToRefs(expulsionReasonsStore);
const uxStore = useUxStore();


onMounted(() => {
  uxStore.isLoading = true;
  expulsionReasonsStore.getAll().then(() => {
    uxStore.isLoading = false;
  })
})

const breadcrumbPaths = [
  { path: "/expulsion-reasons", name: "Okuwdan çykarmak" },
  { path: "/expulsion-reasons/add", name: "Goşmak" },
]
</script>

<template>
  <div class="w-full">
    <the-breadcrumb :paths="breadcrumbPaths"></the-breadcrumb>
    <div v-if="uxStore.isLoading"
      class="flex w-full h-[58vh] items-center justify-center dark:bg-[#171131ef] bg-white rounded-lg border border-gray-200 dark:border-[#36314e]">
      <the-spinner class="w-24"></the-spinner>
    </div>
    <div v-else>
      <expulsion-reasons-data-table :data="expulsionReasons"
        @update="expulsionReasonsStore.getAll()"></expulsion-reasons-data-table>
    </div>
  </div>
</template>

<style scoped></style>
