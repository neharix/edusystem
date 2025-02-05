<script setup>
import {useFacultiesStore} from "@/stores/api.store.js";
import FacultiesDataTable from "@/components/DataTables/FacultiesDataTable.vue";
import {storeToRefs} from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import {onMounted} from "vue";
import {useAuthStore} from "@/stores/auth.store.js";

const authStore = useAuthStore()
const facultiesStore = useFacultiesStore();
const {facultiesAdditional} = storeToRefs(facultiesStore);
const {user} = storeToRefs(authStore);

onMounted(() => {
  facultiesStore.getAllAdditional()
})

const breadcrumbPaths = [
  {path: "/faculties", name: "Fakultetler"},
  {path: "/faculties/add", name: "Goşmak"},
]

</script>

<template>
  <div class="w-full">
    <the-breadcrumb :paths="breadcrumbPaths" v-if="user.is_superuser"></the-breadcrumb>
    <faculties-data-table :data="facultiesAdditional" @update="facultiesStore.getAllAdditional()"></faculties-data-table>
  </div>
</template>

<style scoped>

</style>
