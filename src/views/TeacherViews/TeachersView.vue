<script setup>
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { useAuthStore } from "@/stores/auth.store";
import TeachersViewForAdmin from "./TeachersViewForAdmin.vue";
import TeachersViewForStuff from "./TeachersViewForStuff.vue";
import { storeToRefs } from "pinia";

const authStore = useAuthStore();
const { user } = storeToRefs(authStore);

const breadcrumbPaths = [
  { path: "/teachers", name: 'Mugallymlar' }
]

</script>

<template>
  <div class="w-full">
    <the-breadcrumb :paths="breadcrumbPaths"></the-breadcrumb>
    <teachers-view-for-admin v-if="user.is_superuser"></teachers-view-for-admin>
    <teachers-view-for-stuff v-else></teachers-view-for-stuff>
  </div>
</template>

<style scoped></style>
