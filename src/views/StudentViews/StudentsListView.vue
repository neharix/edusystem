<script setup>
import { useStudentsStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { onMounted } from "vue";
import { useAuthStore } from "@/stores/auth.store.js";
import StudentsDataTable from "@/components/DataTables/StudentsDataTable.vue";
import { useRoute } from "vue-router";

const route = useRoute()
const authStore = useAuthStore()
const studentsStore = useStudentsStore()
const { studentsAdditional } = storeToRefs(studentsStore);
const { user } = storeToRefs(authStore);

onMounted(() => {
  if (Object.keys(route.query).length > 0) {
    studentsStore.getAllAdditionalWithQuery(Object.keys(route.query)[0], route.query[Object.keys(route.query)[0]])
  } else {
    studentsStore.getAllAdditional()
  }
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
