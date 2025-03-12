<script setup>
import { useDepartmentsStore, useFacultiesStore } from "@/stores/api.store.js";
import { useRoute } from "vue-router";
import { onMounted } from "vue";
import AddFacultyDepartment from "@/components/Forms/AddFacultyDepartment.vue";
import HighSchoolDepartmentsDataTable from "@/components/DataTables/HighSchoolDepartmentsDataTable.vue";
import { useUxStore } from "@/stores/ux.store";
import TheSpinner from "@/components/TheSpinner.vue";

const route = useRoute();
const facultiesStore = useFacultiesStore();
const departmentsStore = useDepartmentsStore();
const uxStore = useUxStore();

onMounted(() => {
  uxStore.isLoading = true;
  facultiesStore.getHighSchoolFaculties(route.params.id);
  departmentsStore.getHighSchoolDepartments(route.params.id).then(() => {
    uxStore.isLoading = false;
  })
})

const onUpdate = () => {
  departmentsStore.getHighSchoolDepartments(route.params.id)
  departmentsStore.getHighSchoolExcDepartments(route.params.id)
}

</script>

<template>
  <div class="w-full">
    <add-faculty-department @update="onUpdate"></add-faculty-department>
  </div>
  <div class="w-full">
    <div v-if="uxStore.isLoading"
      class="flex w-full h-[58vh] items-center justify-center dark:bg-[#171131ef] bg-white rounded-lg border border-gray-200 dark:border-[#36314e]">
      <the-spinner class="w-24"></the-spinner>
    </div>
    <div v-else>
      <high-school-departments-data-table :data="departmentsStore.highSchoolDepartments"
        @update="onUpdate"></high-school-departments-data-table>
    </div>
  </div>
</template>

<style scoped></style>
