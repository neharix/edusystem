<script setup>
import {useFacultiesStore} from "@/stores/api.store.js";
import HighSchoolFacultiesDataTable from "@/components/DataTables/HighSchoolFacultiesDataTable.vue";
import {useRoute} from "vue-router";
import {onMounted} from "vue";
import AddHighSchoolFaculty from "@/components/Forms/AddHighSchoolFaculty.vue";

const route = useRoute();
const facultiesStore = useFacultiesStore();

onMounted(() => {
  facultiesStore.getHighSchoolFaculties(route.params.id);
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
    <high-school-faculties-data-table :data="facultiesStore.highSchoolFaculties" @update="onUpdate"></high-school-faculties-data-table>
  </div>
</template>

<style scoped>

</style>
