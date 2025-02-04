<script setup>
import {useHighSchoolsStore} from "@/stores/api.store.js";
import HighSchoolsDataTable from "@/components/DataTables/HighSchoolsDataTable.vue";
import {storeToRefs} from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import {onMounted, watch} from "vue";

const highSchoolsStore = useHighSchoolsStore();
const {highSchools} = storeToRefs(highSchoolsStore);

onMounted(() => {
  highSchoolsStore.getAllAdditional()
})

const breadcrumbPaths = [
  {path: "/high-schools", name: "Ýokary okuw mekdepleri"},
  {path: "/high-schools/add", name: "Goşmak"},
]

</script>

<template>
  <div class="w-full">
    <the-breadcrumb :paths="breadcrumbPaths"></the-breadcrumb>
    <high-schools-data-table :data="highSchools" @update="highSchoolsStore.getAllAdditional()"></high-schools-data-table>
  </div>
</template>

<style scoped>

</style>
