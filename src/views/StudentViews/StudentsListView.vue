<script setup>
import { useStudentsStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { onMounted } from "vue";
import { useAuthStore } from "@/stores/auth.store.js";
import StudentsDataTable from "@/components/DataTables/StudentsDataTable.vue";
import { useRoute } from "vue-router";
import { useUxStore } from "@/stores/ux.store";
import TheSpinner from "@/components/TheSpinner.vue";


const uxStore = useUxStore();

const route = useRoute()
const authStore = useAuthStore()
const studentsStore = useStudentsStore()
const { studentsAdditional } = storeToRefs(studentsStore);
const { role } = storeToRefs(authStore);

onMounted(() => {
  studentsStore.resetMistakeVariables();
  uxStore.isLoading = true;
  if (Object.keys(route.query).length > 0) {
    studentsStore.getAllAdditionalWithQuery(Object.keys(route.query)[0], route.query[Object.keys(route.query)[0]]).then(() => {
      uxStore.isLoading = false;
    })
  } else {
    studentsStore.getAllAdditional().then(() => {
      uxStore.isLoading = false;
    })
  }
})

const breadcrumbPathsForAdmin = [
  { path: "/students", name: "Talyplar" },
  { path: "/students/add", name: "Goşmak" },
]
const breadcrumbPaths = [
  { path: "/students", name: "Talyplar" },
  { path: "/students/validate", name: "Walidator" }
]




</script>

<template>
  <div class="w-full">
    <the-breadcrumb :paths="breadcrumbPathsForAdmin" v-if="role === 'root'"></the-breadcrumb>
    <the-breadcrumb :paths="breadcrumbPaths" v-else></the-breadcrumb>
    <div v-if="uxStore.isLoading"
      class="flex w-full h-[58vh] items-center justify-center dark:bg-[#171131ef] bg-white rounded-lg border border-gray-200 dark:border-[#36314e]">
      <the-spinner class="w-24"></the-spinner>
    </div>
    <div v-else>
      <students-data-table :data="studentsAdditional" @update="studentsStore.getAllAdditional()"></students-data-table>
    </div>
  </div>
</template>

<style scoped></style>
