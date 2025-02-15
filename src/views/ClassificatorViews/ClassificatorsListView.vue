<script setup>
import {useClassificatorsStore} from "@/stores/api.store.js";
import {storeToRefs} from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import {onMounted} from "vue";
import {useAuthStore} from "@/stores/auth.store.js";
import ClassificatorsDataTable from "@/components/DataTables/ClassificatorsDataTable.vue";

const authStore = useAuthStore()
const classificatorsStore = useClassificatorsStore()
const {classificatorsAdditional} = storeToRefs(classificatorsStore);
const {user} = storeToRefs(authStore);

onMounted(() => {
  classificatorsStore.getAllAdditional()
})

const breadcrumbPaths = [
  {path: "/classificators", name: "Klassifikatorlar"},
  {path: "/classificators/add", name: "Goşmak"},
]

</script>

<template>
  <div class="w-full">
    <the-breadcrumb :paths="breadcrumbPaths" v-if="user.is_superuser"></the-breadcrumb>
    <classificators-data-table :data="classificatorsAdditional" @update="classificatorsStore.getAllAdditional()"></classificators-data-table>
  </div>
</template>

<style scoped>

</style>
