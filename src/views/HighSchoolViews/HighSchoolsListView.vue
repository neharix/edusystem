<script setup>
import {useHighSchoolsStore} from "@/stores/api.store.js";
import HighSchoolsDataTable from "@/components/DataTables/HighSchoolsDataTable.vue";
import {storeToRefs} from "pinia";

const highSchoolsStore = useHighSchoolsStore();
const {highSchools} = storeToRefs(highSchoolsStore);

highSchoolsStore.getAdditional()

console.log(highSchools)


</script>

<template>
  <high-schools-data-table :data="highSchools"></high-schools-data-table>
  <!--  <search-table></search-table>-->
</template>

<style scoped>

</style>
