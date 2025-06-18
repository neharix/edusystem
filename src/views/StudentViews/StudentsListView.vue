<script setup>
import { useStudentsStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { onMounted } from "vue";
import { useAuthStore } from "@/stores/auth.store.js";
import StudentsDataTable from "@/components/DataTables/StudentsDataTable.vue";
import HighSchoolStudentsDataTable from "@/components/DataTables/HighSchoolStudentsDataTable.vue";
import { useUxStore } from "@/stores/ux.store";
import TheSpinner from "@/components/TheSpinner.vue";
import GridCell from "@/components/GridCell.vue";


const uxStore = useUxStore();

const authStore = useAuthStore()
const studentsStore = useStudentsStore()
const { studentsAdditional, createStatus, dataTablePageCount, objCount } = storeToRefs(studentsStore);
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
      <div class="grid md:grid-cols-1 sm:grid-cols-1 gap-8 my-8">
        <grid-cell label="Talap boýunça tapylan talyplar" :data-value="objCount"
          icon-bg-class="bg-sky-200 dark:bg-sky-500/75">
          <svg class="w-6 h-8 stroke-sky-500 dark:stroke-sky-900" xmlns="http://www.w3.org/2000/svg" width="14"
            height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
            stroke-linejoin="round">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
        </grid-cell>
      </div>
      <students-data-table v-if="role === 'root'" :data="studentsAdditional" :total-pages="dataTablePageCount"
        @update="updateData"></students-data-table>
      <high-school-students-data-table v-else :data="studentsAdditional" :total-pages="dataTablePageCount"
        @update="updateData"></high-school-students-data-table>

    </div>
  </div>
</template>

<style scoped></style>
