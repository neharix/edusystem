<script setup>
import {useFacultiesStore} from "@/stores/api.store.js";
import HighSchoolFacultiesDataTable from "@/components/DataTables/HighSchoolFacultiesDataTable.vue";
import {useRoute} from "vue-router";
import {onMounted} from "vue";

const route = useRoute();
const facultiesStore = useFacultiesStore();

onMounted(() => {
  facultiesStore.getHighSchoolFaculties(route.params.id);
})
</script>

<template>
  <div class="w-full">
    <high-school-faculties-data-table :data="facultiesStore.highSchoolFaculties" @update="facultiesStore.getHighSchoolFaculties(route.params.id)"></high-school-faculties-data-table>
  </div>
</template>

<style scoped>

</style>
