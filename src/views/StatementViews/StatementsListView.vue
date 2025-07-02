<script setup>
import { useStatementsStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { onMounted } from "vue";
import { useAuthStore } from "@/stores/auth.store.js";
import StatementsDataTable from "@/components/DataTables/StatementsDataTable.vue";
import TheSpinner from "@/components/TheSpinner.vue";
import { useUxStore } from "@/stores/ux.store";


const authStore = useAuthStore()
const statementsStore = useStatementsStore();
const { statements, confirmStatus, rejectStatus } = storeToRefs(statementsStore);
const uxStore = useUxStore();
const { addToast } = storeToRefs(uxStore)

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
</template>

<style scoped></style>
