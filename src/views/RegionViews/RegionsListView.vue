<script setup>
import { useRegionsStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { onMounted } from "vue";
import { useAuthStore } from "@/stores/auth.store.js";
import RegionsDataTable from "@/components/DataTables/RegionsDataTable.vue";
import TheSpinner from "@/components/TheSpinner.vue";
import { useUxStore } from "@/stores/ux.store";

const authStore = useAuthStore()
const regionsStore = useRegionsStore();

const { regionsAdditional } = storeToRefs(regionsStore);
const { user } = storeToRefs(authStore);
const uxStore = useUxStore()

onMounted(() => {
  uxStore.isLoading = true;
  regionsStore.getAllAdditional().then(() => {
    uxStore.isLoading = false;
  })
})

const breadcrumbPaths = [
  { path: "/regions", name: "Welaýatlar" },
  { path: "/regions/add", name: "Goşmak" },
]

</script>

<template>
  <div class="w-full">
    <the-breadcrumb :paths="breadcrumbPaths" v-if="user.is_superuser"></the-breadcrumb>
    <div v-if="uxStore.isLoading"
      class="flex w-full h-[58vh] items-center justify-center dark:bg-[#171131ef] bg-white rounded-lg border border-gray-200 dark:border-[#36314e]">
      <the-spinner class="w-24"></the-spinner>
    </div>
    <div v-else>
      <regions-data-table :data="regionsAdditional" @update="regionsStore.getAllAdditional()"></regions-data-table>
    </div>
  </div>
</template>

<style scoped></style>
