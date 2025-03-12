<script setup>
import { useClassificatorsStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { onMounted } from "vue";
import { useAuthStore } from "@/stores/auth.store.js";
import ClassificatorsDataTable from "@/components/DataTables/ClassificatorsDataTable.vue";
import { useUxStore } from "@/stores/ux.store";
import TheSpinner from "@/components/TheSpinner.vue";


const uxStore = useUxStore();
const authStore = useAuthStore()
const classificatorsStore = useClassificatorsStore()
const { classificatorsAdditional } = storeToRefs(classificatorsStore);
const { user } = storeToRefs(authStore);

onMounted(() => {
  uxStore.isLoading = true;
  classificatorsStore.getAllAdditional().then(() => {
    uxStore.isLoading = false;
  })
})

const breadcrumbPaths = [
  { path: "/classificators", name: "Klassifikatorlar" },
  { path: "/classificators/add", name: "Goşmak" },
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
      <classificators-data-table :data="classificatorsAdditional"
        @update="classificatorsStore.getAllAdditional()"></classificators-data-table>
    </div>
  </div>
</template>

<style scoped></style>
