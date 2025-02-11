<script setup>
import {useDepartmentsStore, useFacultiesStore} from "@/stores/api.store.js";
import HighSchoolFacultiesDataTable from "@/components/DataTables/HighSchoolFacultiesDataTable.vue";
import {useRoute} from "vue-router";
import {onMounted} from "vue";
import AddHighSchoolFaculty from "@/components/Forms/AddHighSchoolFaculty.vue";
import AddFacultyDepartment from "@/components/Forms/AddFacultyDepartment.vue";
import HighSchoolDepartmentsDataTable from "@/components/DataTables/HighSchoolDepartmentsDataTable.vue";

const route = useRoute();
const facultiesStore = useFacultiesStore();
const departmentsStore = useDepartmentsStore();

onMounted(() => {
  facultiesStore.getHighSchoolFaculties(route.params.id);
  departmentsStore.getHighSchoolDepartments(route.params.id)
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
  <!-- Доработай систему удаления кафедры из ВУЗа -->
  <div class="w-full">
    <high-school-departments-data-table :data="departmentsStore.highSchoolDepartments" @update="onUpdate"></high-school-departments-data-table>
  </div>
</template>

<style scoped>

</style>
