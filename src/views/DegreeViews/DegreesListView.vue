<script setup>
import {useClassificatorsStore, useDegreesStore} from "@/stores/api.store.js";
import {storeToRefs} from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import {onMounted} from "vue";
import {useAuthStore} from "@/stores/auth.store.js";
import ClassificatorsDataTable from "@/components/DataTables/ClassificatorsDataTable.vue";
import DegreesDataTable from "@/components/DataTables/DegreesDataTable.vue";

const authStore = useAuthStore()
const degreesStore = useDegreesStore()
const {degreesAdditional} = storeToRefs(degreesStore);
const {user} = storeToRefs(authStore);

onMounted(() => {
  degreesStore.getAllAdditional()
})

const breadcrumbPaths = [
  {path: "/degrees", name: "Hünär derejeleri"},
  {path: "/degrees/add", name: "Goşmak"},
]

</script>

<template>
  <div class="w-full">
    <the-breadcrumb :paths="breadcrumbPaths" v-if="user.is_superuser"></the-breadcrumb>
    <degrees-data-table :data="degreesAdditional" @update="degreesStore.getAllAdditional()"></degrees-data-table>
  </div>
</template>

<style scoped>

</style>
