<script setup>
import { useFacultiesStore } from "@/stores/api.store.js";
import HighSchoolFacultiesDataTable from "@/components/DataTables/HighSchoolFacultiesDataTable.vue";
import { useRoute } from "vue-router";
import { onMounted } from "vue";
import AddHighSchoolFaculty from "@/components/Forms/AddHighSchoolFaculty.vue";
import TheSpinner from "@/components/TheSpinner.vue";
import { useUxStore } from "@/stores/ux.store";

const route = useRoute();
const facultiesStore = useFacultiesStore();
const uxStore = useUxStore();

onMounted(() => {
  uxStore.isLoading = true;
  facultiesStore.getHighSchoolFaculties(route.params.id).then(() => {
    uxStore.isLoading = false;
  });
})

const onUpdate = () => {
  facultiesStore.getHighSchoolFaculties(route.params.id)
  facultiesStore.getHighSchoolExcFaculties(route.params.id)
}

</script>

<template>
  <div class="w-full">
    <add-high-school-faculty @update="onUpdate"></add-high-school-faculty>
  </div>
  <div class="w-full">
    <div v-if="uxStore.isLoading"
      class="flex w-full h-[58vh] items-center justify-center dark:bg-[#171131ef] bg-white rounded-lg border border-gray-200 dark:border-[#36314e]">
      <the-spinner class="w-24"></the-spinner>
    </div>
    <div v-else>
      <high-school-faculties-data-table :data="facultiesStore.highSchoolFaculties"
        @update="onUpdate"></high-school-faculties-data-table>
    </div>
  </div>
</template>

<style scoped></style>
