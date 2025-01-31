<script setup>
import {useHighSchoolsStore} from "@/stores/api.store.js";
import HighSchoolsDataTable from "@/components/DataTables/HighSchoolsDataTable.vue";
import {storeToRefs} from "pinia";

const highSchoolsStore = useHighSchoolsStore();
const {highSchools} = storeToRefs(highSchoolsStore);

highSchoolsStore.getAdditional()



</script>

<template>
  <div class="w-full">
    <div
      class="px-3 py-4 w-full rounded-xl shadow-md dark:shadow-lg flex justify-between mb-8 bg-white dark:bg-[#171131ef]">
      <div class="flex items-center">
        <h3 class="lg:block md:block hidden">Ýokary okuw mekdepleri</h3>
        <h3 class="mx-2 lg:block md:block hidden">/</h3>
        <!-- TODO add some functionality -->
        <button
          class="py-2 px-3 my-2 text-sm rounded-lg shadow-md border-none dark:border-violet-500/50 border-1 bg-blue-500 dark:bg-violet-600 text-white">
          Goşmak
        </button>
      </div>
    </div>
    <high-schools-data-table :data="highSchools"></high-schools-data-table>
  </div>
  <!--  <search-table></search-table>-->
</template>

<style scoped>

</style>
