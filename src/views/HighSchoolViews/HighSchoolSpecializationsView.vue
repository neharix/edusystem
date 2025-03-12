<script setup>
import { useDepartmentsStore, useSpecializationsStore } from "@/stores/api.store.js";
import { useRoute } from "vue-router";
import { onMounted } from "vue";
import HighSchoolSpecializationsDataTable from "@/components/DataTables/HighSchoolSpecializationsDataTable.vue";
import AddDepartmentSpecialization from "@/components/Forms/AddDepartmentSpecialization.vue";
import { useUxStore } from "@/stores/ux.store";
import TheSpinner from "@/components/TheSpinner.vue";

const route = useRoute();
const departmentsStore = useDepartmentsStore();
const specializationsStore = useSpecializationsStore();
const uxStore = useUxStore();

onMounted(() => {
  uxStore.isLoading = true;
  departmentsStore.getHighSchoolDepartments(route.params.id);
  specializationsStore.getHighSchoolSpecializations(route.params.id).then(() => {
    uxStore.isLoading = false;
  });
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
    <div v-if="uxStore.isLoading"
      class="flex w-full h-[58vh] items-center justify-center dark:bg-[#171131ef] bg-white rounded-lg border border-gray-200 dark:border-[#36314e]">
      <the-spinner class="w-24"></the-spinner>
    </div>
    <div v-else>
      <high-school-specializations-data-table :data="specializationsStore.highSchoolSpecializations"
        @update="onUpdate"></high-school-specializations-data-table>
    </div>
  </div>
</template>

<style scoped></style>
