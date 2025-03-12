<script setup>
import { useStatementsStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { onMounted } from "vue";
import { useAuthStore } from "@/stores/auth.store.js";
import StatementsDataTable from "@/components/DataTables/StatementsDataTable.vue";
import useToast from "@/use/useToast";
import TheToast from "@/components/TheToast.vue";
import TheSpinner from "@/components/TheSpinner.vue";
import { useUxStore } from "@/stores/ux.store";

const { toasts, addToast } = useToast();

const authStore = useAuthStore()
const statementsStore = useStatementsStore();
const { statements, confirmStatus, rejectStatus } = storeToRefs(statementsStore);
const uxStore = useUxStore();

const { role } = storeToRefs(authStore);

onMounted(() => {

  if (rejectStatus.value) {
    if (rejectStatus.value === 'success') {
      addToast('Arza üstünlikli ret edildi', 'success');
    } else if (rejectStatus.value === 'error') {
      addToast('Ret etme prosesinde ýalňyşlyk ýüze çykdy', 'error');
    }
  }
  rejectStatus.value = null;

  if (confirmStatus.value) {
    if (confirmStatus.value === 'success') {
      addToast('Arza üstünlikli tassyklanyldy', 'success');
    } else if (confirmStatus.value === 'error') {
      addToast('Tassyklama prosesinde ýalňyşlyk ýüze çykdy', 'error');
    }
  }
  confirmStatus.value = null;

  uxStore.isLoading = true;
  statementsStore.getAll().then(() => {
    uxStore.isLoading = false;
  });
})


const breadcrumbPaths = [
  { path: "/statements", name: "Arzalar" },
]

</script>

<template>
  <div class="w-full">
    <the-breadcrumb :paths="breadcrumbPaths" v-if="role === 'root'"></the-breadcrumb>
    <div v-if="uxStore.isLoading"
      class="flex w-full h-[58vh] items-center justify-center dark:bg-[#171131ef] bg-white rounded-lg border border-gray-200 dark:border-[#36314e]">
      <the-spinner class="w-24"></the-spinner>
    </div>
    <div v-else>
      <statements-data-table :data="statements" @update="statementsStore.getAll()"></statements-data-table>
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
