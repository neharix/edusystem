<script setup>
import { useStudentsStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { onMounted } from "vue";
import { useAuthStore } from "@/stores/auth.store.js";
import StudentsDataTable from "@/components/DataTables/StudentsDataTable.vue";
import { useUxStore } from "@/stores/ux.store";
import TheSpinner from "@/components/TheSpinner.vue";


const uxStore = useUxStore();

const authStore = useAuthStore()
const studentsStore = useStudentsStore()
const { studentsAdditional, createStatus, dataTablePageCount } = storeToRefs(studentsStore);
const { role } = storeToRefs(authStore);

function updateData() {
  uxStore.isLoading = true;
  studentsStore.getAllAdditional().then(() => {
    uxStore.isLoading = false;
  })
}


onMounted(() => {
  studentsStore.resetMistakeVariables();
  uxStore.isLoading = true;
  // if (Object.keys(route.query) > 0) {
  //   studentsStore.getAllAdditionalWithQuery(Object.keys(route.query)[0], route.query[Object.keys(route.query)[0]]).then(() => {
  //     uxStore.isLoading = false;
  //   })
  // } else {
  studentsStore.getAllAdditional().then(() => {
    uxStore.isLoading = false;
  })
  // }

  if (createStatus.value) {
    if (createStatus.value === 'success') {
      studentsStore.getAllAdditional();
    }
  }
  createStatus.value = null;
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
      <students-data-table v-if="role === 'root'" :data="studentsAdditional" :total-pages="dataTablePageCount"
        @update="updateData"></students-data-table>
        <students-data-table v-else :data="studentsAdditional" :total-pages="dataTablePageCount"
        @update="updateData"></students-data-table>
    </div>
  </div>
</template>

<style scoped></style>
