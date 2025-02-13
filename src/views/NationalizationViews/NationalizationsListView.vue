<script setup>
import {useDepartmentsStore, useSpecializationsStore} from "@/stores/api.store.js";
import {storeToRefs} from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import {onMounted} from "vue";
import {useAuthStore} from "@/stores/auth.store.js";
import SpecializationsDataTable from "@/components/DataTables/SpecializationsDataTable.vue";

const authStore = useAuthStore()
const specializationsStore = useSpecializationsStore();
const {specializationsAdditional} = storeToRefs(specializationsStore);
const {user} = storeToRefs(authStore);

onMounted(() => {
  specializationsStore.getAllAdditional()
})

const breadcrumbPaths = [
  {path: "/specializations", name: "Hünärler"},
  {path: "/specializations/add", name: "Goşmak"},
]
</script>

<template>
  <div class="w-full">
    <the-breadcrumb :paths="breadcrumbPaths" v-if="user.is_superuser"></the-breadcrumb>
    <specializations-data-table :data="specializationsAdditional" @update="specializationsStore.getAllAdditional()"></specializations-data-table>
  </div>
</template>

<style scoped>

</style>
