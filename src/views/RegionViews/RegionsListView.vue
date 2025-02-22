<script setup>
import { useClassificatorsStore, useRegionsStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { onMounted } from "vue";
import { useAuthStore } from "@/stores/auth.store.js";
import RegionsDataTable from "@/components/DataTables/RegionsDataTable.vue";

const authStore = useAuthStore()
const regionsStore = useRegionsStore();

const { regionsAdditional } = storeToRefs(regionsStore);
const { user } = storeToRefs(authStore);

onMounted(() => {
  regionsStore.getAllAdditional()
})

const breadcrumbPaths = [
  { path: "/regions", name: "Welaýatlar" },
  { path: "/regions/add", name: "Goşmak" },
]

</script>

<template>
  <div class="w-full">
    <the-breadcrumb :paths="breadcrumbPaths" v-if="user.is_superuser"></the-breadcrumb>
    <regions-data-table :data="regionsAdditional" @update="regionsStore.getAllAdditional()"></regions-data-table>
  </div>
</template>

<style scoped></style>
