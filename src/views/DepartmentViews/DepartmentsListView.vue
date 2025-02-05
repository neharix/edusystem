<script setup>
import {useDepartmentsStore} from "@/stores/api.store.js";
import {storeToRefs} from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import {onMounted} from "vue";
import {useAuthStore} from "@/stores/auth.store.js";
import DepartmentsDataTable from "@/components/DataTables/DepartmentsDataTable.vue";

const authStore = useAuthStore()
const departmentsStore = useDepartmentsStore()
const {departmentsAdditional} = storeToRefs(departmentsStore);
const {user} = storeToRefs(authStore);

onMounted(() => {
  departmentsStore.getAllAdditional()
})

const breadcrumbPaths = [
  {path: "/departments", name: "Kafedralar"},
  {path: "/departments/add", name: "Goşmak"},
]

</script>

<template>
  <div class="w-full">
    <the-breadcrumb :paths="breadcrumbPaths" v-if="user.is_superuser"></the-breadcrumb>
    <departments-data-table :data="departmentsAdditional" @update="departmentsStore.getAllAdditional()"></departments-data-table>
  </div>
</template>

<style scoped>

</style>
