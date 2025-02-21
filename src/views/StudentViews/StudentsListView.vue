<script setup>
import { useStudentsStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { onMounted } from "vue";
import { useAuthStore } from "@/stores/auth.store.js";
import StudentsDataTable from "@/components/DataTables/StudentsDataTable.vue";

const authStore = useAuthStore()
const studentsStore = useStudentsStore()
const { studentsAdditional } = storeToRefs(studentsStore);
const { user } = storeToRefs(authStore);

onMounted(() => {
  studentsStore.getAllAdditional()
})

const breadcrumbPathsForAdmin = [
  { path: "/students", name: "Talyplar" },
  { path: "/students/add", name: "Goşmak" },
]
const breadcrumbPaths = [
  { path: "/students", name: "Talyplar" },
]


</script>

<template>
  <div class="w-full">
    <the-breadcrumb :paths="breadcrumbPathsForAdmin" v-if="user.is_superuser"></the-breadcrumb>
    <the-breadcrumb :paths="breadcrumbPaths" v-else></the-breadcrumb>
    <students-data-table :data="studentsAdditional" @update="studentsStore.getAllAdditional()"></students-data-table>
  </div>
</template>

<style scoped></style>
