<script setup>
import { useTeacherStatementsStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import { onBeforeMount } from "vue";
import TeachersDataTable from "@/components/DataTables/TeachersDataTable.vue";
import TotalTeachersDataTable from "@/components/DataTables/TotalTeachersDataTable.vue";
import { useUxStore } from "@/stores/ux.store";
import TheSpinner from "@/components/TheSpinner.vue";


const teacherStatementsStore = useTeacherStatementsStore();
const { teacherStatements } = storeToRefs(teacherStatementsStore);
const uxStore = useUxStore();
const { addToast } = storeToRefs();


onBeforeMount(() => {
  uxStore.isLoading = true;
  teacherStatementsStore.getAll().then(() => {
    uxStore.isLoading = false;
  });
})


</script>

<template>
  <div class="w-full">
    <div v-if="uxStore.isLoading"
      class="flex w-full h-[58vh] items-center justify-center dark:bg-[#171131ef] bg-white rounded-lg border border-gray-200 dark:border-[#36314e]">
      <the-spinner class="w-24"></the-spinner>
    </div>
    <div v-else>
      <teachers-data-table :data="teacherStatements" @update="teacherStatementsStore.getAll()"></teachers-data-table>
      <total-teachers-data-table :data="teacherStatements"></total-teachers-data-table>
    </div>
  </div>
</template>

<style scoped></style>
