<script setup>
import { useFacultiesStore } from "@/stores/api.store.js";
import FacultiesDataTable from "@/components/DataTables/FacultiesDataTable.vue";
import { storeToRefs } from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { onMounted } from "vue";
import { useAuthStore } from "@/stores/auth.store.js";
import TheSpinner from "@/components/TheSpinner.vue";
import { useUxStore } from "@/stores/ux.store";

const authStore = useAuthStore()
const facultiesStore = useFacultiesStore();
const { facultiesAdditional } = storeToRefs(facultiesStore);
const { role } = storeToRefs(authStore);
const uxStore = useUxStore();

onMounted(() => {
  uxStore.isLoading = true;
  facultiesStore.getAllAdditional().then(() => {
    uxStore.isLoading = false;
  })
})

const breadcrumbPaths = [
  { path: "/faculties", name: "Fakultetler" },
  { path: "/faculties/add", name: "Goşmak" },
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
      <faculties-data-table :data="facultiesAdditional"
        @update="facultiesStore.getAllAdditional()"></faculties-data-table>
    </div>
  </div>
</template>

<style scoped></style>
