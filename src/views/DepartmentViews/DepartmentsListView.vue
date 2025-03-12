<script setup>
import { useDepartmentsStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { onMounted } from "vue";
import { useAuthStore } from "@/stores/auth.store.js";
import DepartmentsDataTable from "@/components/DataTables/DepartmentsDataTable.vue";
import { useUxStore } from "@/stores/ux.store";
import TheSpinner from "@/components/TheSpinner.vue";

const authStore = useAuthStore()
const departmentsStore = useDepartmentsStore()
const { departmentsAdditional } = storeToRefs(departmentsStore);
const { role } = storeToRefs(authStore);
const uxStore = useUxStore();

onMounted(() => {
  uxStore.isLoading = true;
  departmentsStore.getAllAdditional().then(() => {
    uxStore.isLoading = false;
  })
})

const breadcrumbPaths = [
  { path: "/departments", name: "Kafedralar" },
  { path: "/departments/add", name: "Goşmak" },
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
      <departments-data-table :data="departmentsAdditional"
        @update="departmentsStore.getAllAdditional()"></departments-data-table>
    </div>
  </div>
</template>

<style scoped></style>
