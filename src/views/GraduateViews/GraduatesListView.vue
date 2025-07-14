<script setup>
import { useGraduatesStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { onMounted } from "vue";
import GraduatesDataTable from "@/components/DataTables/GraduatesDataTable.vue";
import { useUxStore } from "@/stores/ux.store";
import TheSpinner from "@/components/TheSpinner.vue";

const uxStore = useUxStore();

const graduatesStore = useGraduatesStore()
const { graduatesAdditional, dataTablePageCount } = storeToRefs(graduatesStore);


function updateData() {
  uxStore.isLoading = true;
  graduatesStore.getAllAdditional().then(() => {
    uxStore.isLoading = false;
  })
}

onMounted(() => {
  updateData();
})


const breadcrumbPaths = [
  { path: "/graduates", name: "Uçurymlar" },
]

</script>

<template>
  <div class="w-full">
    <the-breadcrumb :paths="breadcrumbPaths"></the-breadcrumb>
    <div v-if="uxStore.isLoading"
      class="flex w-full h-[58vh] items-center justify-center dark:bg-[#171131ef] bg-white rounded-lg border border-gray-200 dark:border-[#36314e]">
      <the-spinner class="w-24"></the-spinner>
    </div>
    <div v-else>
      <graduates-data-table :data="graduatesAdditional" :total-pages="dataTablePageCount"
        @update="updateData"></graduates-data-table>
    </div>
  </div>
</template>

<style scoped></style>
