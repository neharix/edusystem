<script setup>
import { useTeacherStatementsStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { onBeforeMount } from "vue";
import { useAuthStore } from "@/stores/auth.store.js";
import TeachersDataTable from "@/components/DataTables/TeachersDataTable.vue";
import useToast from "@/use/useToast";
import TheToast from "@/components/TheToast.vue";
import TotalTeachersDataTable from "@/components/DataTables/TotalTeachersDataTable.vue";

const { toasts, addToast } = useToast();

const authStore = useAuthStore()
const teacherStatementsStore = useTeacherStatementsStore();
const { teacherStatements } = storeToRefs(teacherStatementsStore);

const { user } = storeToRefs(authStore);

onBeforeMount(() => {
  teacherStatementsStore.getAll();
})


</script>

<template>
  <div class="w-full">
    <teachers-data-table :data="teacherStatements" @update="teacherStatementsStore.getAll()"></teachers-data-table>
    <total-teachers-data-table :data="teacherStatements"></total-teachers-data-table>
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
