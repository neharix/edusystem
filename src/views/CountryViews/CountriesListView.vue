<script setup>
import {useCountriesStore, useNationalizationsStore} from "@/stores/api.store.js";
import {storeToRefs} from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import {onMounted} from "vue";
import {useAuthStore} from "@/stores/auth.store.js";
import NationalizationsDataTable from "@/components/DataTables/NationalizationsDataTable.vue";
import CountriesDataTable from "@/components/DataTables/CountriesDataTable.vue";

const authStore = useAuthStore()
const countriesStore = useCountriesStore()
const {countriesAdditional} = storeToRefs(countriesStore);
const {user} = storeToRefs(authStore);

onMounted(() => {
  countriesStore.getAllAdditional()
})

const breadcrumbPaths = [
  {path: "/countries", name: "Ýurtlar"},
  {path: "/countries/add", name: "Goşmak"},
]

</script>

<template>
  <div class="w-full">
    <the-breadcrumb :paths="breadcrumbPaths" v-if="user.is_superuser"></the-breadcrumb>
    <countries-data-table :data="countriesAdditional" @update="countriesStore.getAllAdditional()"></countries-data-table>
  </div>
</template>

<style scoped>

</style>
