<script setup>
import { useHighSchoolsStore } from "@/stores/api.store.js";
import HighSchoolsDataTable from "@/components/DataTables/HighSchoolsDataTable.vue";
import { storeToRefs } from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { onMounted } from "vue";
import { useUxStore } from "@/stores/ux.store";
import TheSpinner from "@/components/TheSpinner.vue";

const highSchoolsStore = useHighSchoolsStore();
const { highSchools } = storeToRefs(highSchoolsStore);
const uxStore = useUxStore();


onMounted(() => {
  uxStore.isLoading = true;
  highSchoolsStore.getAllAdditional().then(() => {
    uxStore.isLoading = false;
  });
})

const breadcrumbPaths = [
  { path: "/high-schools", name: "Ýokary okuw mekdepleri" },
  { path: "/high-schools/add", name: "Goşmak" },
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
      <high-schools-data-table :data="highSchools"
        @update="highSchoolsStore.getAllAdditional()"></high-schools-data-table>
    </div>
  </div>
</template>

<style scoped></style>
