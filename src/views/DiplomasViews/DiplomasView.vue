<script setup>
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { useAuthStore } from "@/stores/auth.store";
import DiplomasViewForAdmin from "./DiplomasViewForAdmin.vue";
import DiplomasViewForStuff from "./DiplomasViewForStuff.vue";
import { storeToRefs } from "pinia";
import { ref, watch } from "vue";
import { useDiplomasStore } from "@/stores/api.store";

const authStore = useAuthStore();
const { user, role } = storeToRefs(authStore);
const diplomasStore = useDiplomasStore();
const { diplomaRequestAdvanced } = storeToRefs(diplomasStore);


const breadcrumbPaths = ref([
  { path: "/diplomas", name: "Diplomlar" },
])

let allowedUntil = 0;
let now = 0;

watch(diplomaRequestAdvanced, (newVal) => {
  if (user.value.is_superuser) {
  }
  else {
    if (!newVal.null) {
      allowedUntil = new Date(diplomaRequestAdvanced.value.allowed_until).getTime();
      now = new Date().getTime()

      if (newVal.verdict === "C" && (allowedUntil > now)) {
        breadcrumbPaths.value = [
          { path: "/diplomas", name: "Diplomlar" },
          { path: "/diplomas/new-request/", name: "Hasabaty täzelemek" }
        ];
      } else {
        breadcrumbPaths.value = [
          { path: "/diplomas", name: "Diplomlar" },
        ];
      }
    } else {
      breadcrumbPaths.value = [
        { path: "/diplomas", name: "Diplomlar" },
      ];
    }
  }
})

</script>

<template>
  <div class="w-full">
    <the-breadcrumb :paths="breadcrumbPaths"></the-breadcrumb>
    <diplomas-view-for-admin v-if="role === 'root'"></diplomas-view-for-admin>
    <diplomas-view-for-stuff v-else></diplomas-view-for-stuff>
  </div>
</template>

<style scoped></style>
