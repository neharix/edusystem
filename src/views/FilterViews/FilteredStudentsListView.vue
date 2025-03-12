<script setup>
import { useFilterStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { onMounted } from "vue";
import StudentsDataTable from "@/components/DataTables/StudentsDataTable.vue";
import router from "@/router";
import { useRoute } from "vue-router";
import { useUxStore } from "@/stores/ux.store";
import TheSpinner from "@/components/TheSpinner.vue";

const route = useRoute();
const filterStore = useFilterStore()
const { filteredStudents, filterOptions } = storeToRefs(filterStore);
const uxStore = useUxStore();

onMounted(() => {
  filterStore.getFilterOptions().then(() => {
    if (filterStore.isfilterOptionsInSession) {
      uxStore.isLoading = true;
      filterStore.getFilteredStudents(filterOptions.value, Object.keys(route.query)[0], route.query[Object.keys(route.query)[0]]).then(() => {
        uxStore.isLoading = false;
      });
    } else {
      router.push("/filter");
    }
  })
})

const breadcrumbPaths = [
  { path: "/filter", name: "Süzgüç" },
  { path: "/filter/detail", name: "Süzgüçlenen talyplar", current: true },
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
      <students-data-table :data="filteredStudents" @update="filterStore.getFilteredStudents()"></students-data-table>
    </div>
  </div>
</template>

<style scoped></style>
