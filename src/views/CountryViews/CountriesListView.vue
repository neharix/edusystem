<script setup>
import { useCountriesStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { onMounted } from "vue";
import { useAuthStore } from "@/stores/auth.store.js";
import CountriesDataTable from "@/components/DataTables/CountriesDataTable.vue";
import TheSpinner from "@/components/TheSpinner.vue";
import { useUxStore } from "@/stores/ux.store";

const uxStore = useUxStore();
const authStore = useAuthStore()
const countriesStore = useCountriesStore()
const { countriesAdditional } = storeToRefs(countriesStore);
const { role } = storeToRefs(authStore);

onMounted(() => {
  uxStore.isLoading = true;
  countriesStore.getAllAdditional().then(() => {
    uxStore.isLoading = false;
  })
})

const breadcrumbPaths = [
  { path: "/countries", name: "Ýurtlar" },
  { path: "/countries/add", name: "Goşmak" },
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
      <countries-data-table :data="countriesAdditional"
        @update="countriesStore.getAllAdditional()"></countries-data-table>
    </div>
  </div>
</template>

<style scoped></style>
