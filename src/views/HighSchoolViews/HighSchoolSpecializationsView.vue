<script setup>
import {useDepartmentsStore, useFacultiesStore, useSpecializationsStore} from "@/stores/api.store.js";
import HighSchoolFacultiesDataTable from "@/components/DataTables/HighSchoolFacultiesDataTable.vue";
import {useRoute} from "vue-router";
import {onMounted} from "vue";
import AddHighSchoolFaculty from "@/components/Forms/AddHighSchoolFaculty.vue";
import AddFacultyDepartment from "@/components/Forms/AddFacultyDepartment.vue";
import HighSchoolDepartmentsDataTable from "@/components/DataTables/HighSchoolDepartmentsDataTable.vue";
import HighSchoolSpecializationsDataTable from "@/components/DataTables/HighSchoolSpecializationsDataTable.vue";
import AddDepartmentSpecialization from "@/components/Forms/AddDepartmentSpecialization.vue";

const route = useRoute();
const facultiesStore = useFacultiesStore();
const departmentsStore = useDepartmentsStore();
const specializationsStore = useSpecializationsStore();

onMounted(() => {
  departmentsStore.getHighSchoolDepartments(route.params.id);
  specializationsStore.getHighSchoolSpecializations(route.params.id);
})

const onUpdate = () => {
  specializationsStore.getHighSchoolSpecializations(route.params.id)
  specializationsStore.getHighSchoolExcSpecializations(route.params.id)
}

</script>

<template>
  <div class="w-full">
    <add-department-specialization @update="onUpdate"></add-department-specialization>
  </div>
  <div class="w-full">
    <high-school-specializations-data-table :data="specializationsStore.highSchoolSpecializations" @update="onUpdate"></high-school-specializations-data-table>
  </div>
</template>

<style scoped>

</style>
