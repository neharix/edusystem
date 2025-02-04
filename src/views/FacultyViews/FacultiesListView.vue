<script setup>
import {useFacultiesStore, useHighSchoolsStore} from "@/stores/api.store.js";
import FacultiesDataTable from "@/components/DataTables/FacultiesDataTable.vue";
import {storeToRefs} from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import {onMounted, watch} from "vue";

const facultiesStore = useFacultiesStore();
const {facultiesAdditional} = storeToRefs(facultiesStore);

onMounted(() => {
  facultiesStore.getAllAdditional()
})

const breadcrumbPaths = [
  {path: "/faculties", name: "Fakultetler"},
  {path: "/faculties/add", name: "Goşmak"},
]

</script>

<template>
  <div class="w-full">
    <the-breadcrumb :paths="breadcrumbPaths"></the-breadcrumb>
    <faculties-data-table :data="facultiesAdditional" @update="facultiesStore.getAllAdditional()"></faculties-data-table>
  </div>
</template>

<style scoped>

</style>
