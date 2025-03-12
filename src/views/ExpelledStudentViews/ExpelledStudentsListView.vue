<script setup>
import { useStudentsStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { onMounted } from "vue";
import ExpelledStudentsDataTable from "@/components/DataTables/ExpelledStudentsDataTable.vue";
import { useUxStore } from "@/stores/ux.store";
import TheSpinner from "@/components/TheSpinner.vue";

const uxStore = useUxStore();
const studentsStore = useStudentsStore()
const { expelledStudentsAdditional } = storeToRefs(studentsStore);

onMounted(() => {
  uxStore.isLoading = true;
  studentsStore.getAllExpelledStudents().then(() => {
    uxStore.isLoading = false;
  })
})

const breadcrumbPaths = [
  { path: "/expelled-students", name: "Okuwdan boşadylanlar" },
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
      <expelled-students-data-table :data="expelledStudentsAdditional"
        @update="studentsStore.getAllExpelledStudents()"></expelled-students-data-table>
    </div>
  </div>
</template>

<style scoped></style>
