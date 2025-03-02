<template>
  <component :is="dashboard"></component>
</template>

<script setup>
import { onMounted, ref, shallowRef, watch } from "vue";
import EmptyDashboard from "@/components/Dashboards/EmptyDashboard.vue";
import RootDashboard from "@/components/Dashboards/RootDashboard.vue";
import UserDashboard from "@/components/Dashboards/UserDashboard.vue";
import { storeToRefs } from "pinia";
import RootSidebar from "@/components/Sidebars/RootSidebar.vue";
import UserSidebar from "@/components/Sidebars/UserSidebar.vue";
import { useAuthStore } from "@/stores/auth.store.js";

const authStore = useAuthStore();

const { role } = storeToRefs(authStore);

const dashboard = shallowRef(EmptyDashboard);


onMounted(() => {
  if (authStore.role === "root") {
    dashboard.value = RootDashboard;
  } else if (authStore.role === "user") {
    dashboard.value = UserDashboard;
  } else if (authStore.role === "empty") {
    dashboard.value = EmptyDashboard;
  }
})

watch(role, (newValue, oldValue) => {
  if (newValue === "root") {
    dashboard.value = RootDashboard;
  } else if (newValue === "user") {
    dashboard.value = UserDashboard;
  } else if (newValue === "empty") {
    dashboard.value = EmptyDashboard;
  }
})

</script>
