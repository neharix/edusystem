<script setup>
import {useNationalizationsStore} from "@/stores/api.store.js";
import {storeToRefs} from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import {onMounted} from "vue";
import {useAuthStore} from "@/stores/auth.store.js";
import NationalizationsDataTable from "@/components/DataTables/NationalizationsDataTable.vue";

const authStore = useAuthStore()
const nationalizationsStore = useNationalizationsStore()
const {nationalizationsAdditional} = storeToRefs(nationalizationsStore);
const {user} = storeToRefs(authStore);

onMounted(() => {
  nationalizationsStore.getAllAdditional()
})

const breadcrumbPaths = [
  {path: "/nationalizations", name: "Milletler"},
  {path: "/nationalizations/add", name: "Goşmak"},
]

</script>

<template>
  <div class="w-full">
    <the-breadcrumb :paths="breadcrumbPaths" v-if="user.is_superuser"></the-breadcrumb>
    <nationalizations-data-table :data="nationalizationsAdditional" @update="nationalizationsStore.getAllAdditional()"></nationalizations-data-table>
  </div>
</template>

<style scoped>

</style>
