<script setup>
import { useFilterStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { onMounted } from "vue";
import StudentsDataTable from "@/components/DataTables/StudentsDataTable.vue";
import router from "@/router";
import { useRoute } from "vue-router";

const route = useRoute();
const filterStore = useFilterStore()
const { filteredStudents, filterOptions } = storeToRefs(filterStore);


onMounted(() => {
  filterStore.getFilterOptions().then(() => {
    if (filterStore.isfilterOptionsInSession) {
      filterStore.getFilteredStudents(filterOptions.value, Object.keys(route.query)[0], route.query[Object.keys(route.query)[0]]);
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
    <students-data-table :data="filteredStudents" @update="filterStore.getFilteredStudents()"></students-data-table>
  </div>
</template>

<style scoped></style>
