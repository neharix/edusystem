<script setup>
import { useTeacherStatementsStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import { onBeforeMount } from "vue";
import TeachersDataTable from "@/components/DataTables/TeachersDataTable.vue";
import useToast from "@/use/useToast";
import TheToast from "@/components/TheToast.vue";
import TotalTeachersDataTable from "@/components/DataTables/TotalTeachersDataTable.vue";
import { useUxStore } from "@/stores/ux.store";
import TheSpinner from "@/components/TheSpinner.vue";

const { toasts, addToast } = useToast();

const teacherStatementsStore = useTeacherStatementsStore();
const { teacherStatements } = storeToRefs(teacherStatementsStore);
const uxStore = useUxStore();


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
  <teleport to="body">
    <div class="toast-container w-5/6 fixed top-25
       md:top-auto md:bottom-5 right-5 md:w-1/4 flex flex-col-reverse space-y-2">
      <TransitionGroup name="toast">
        <the-toast v-for="toast in toasts" :key="toast.id" :message="toast.message" :type="toast.type"
          :duration="toast.duration" :onClose="() => (toasts = toasts.filter((t) => t.id !== toast.id))"></the-toast>
      </TransitionGroup>
    </div>
  </teleport>
</template>

<style scoped></style>
