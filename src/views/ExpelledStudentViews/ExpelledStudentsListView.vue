<script setup>
import { useStudentsStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { onMounted } from "vue";
import { useAuthStore } from "@/stores/auth.store.js";
import ExpelledStudentsDataTable from "@/components/DataTables/ExpelledStudentsDataTable.vue";

const authStore = useAuthStore()
const studentsStore = useStudentsStore()
const { expelledStudentsAdditional } = storeToRefs(studentsStore);
const { user } = storeToRefs(authStore);

onMounted(() => {
  studentsStore.getAllExpelledStudents()
})

const breadcrumbPaths = [
  { path: "/expelled-students", name: "Okuwdan boşadylanlar" },
]


</script>

<template>
  <div class="w-full">
    <the-breadcrumb :paths="breadcrumbPaths"></the-breadcrumb>
    <expelled-students-data-table :data="expelledStudentsAdditional"
      @update="studentsStore.getAllExpelledStudents()"></expelled-students-data-table>
  </div>
</template>

<style scoped></style>
