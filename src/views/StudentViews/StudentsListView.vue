<script setup>
import { useStudentsStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { onMounted } from "vue";
import { useAuthStore } from "@/stores/auth.store.js";
import StudentsDataTable from "@/components/DataTables/StudentsDataTable.vue";
import { useRoute } from "vue-router";
import { useUxStore } from "@/stores/ux.store";
import TheSpinner from "@/components/TheSpinner.vue";
import TheToolbar from "@/components/TheToolbar.vue";
import ToolbarButton from "@/components/ToolbarButton.vue";
import ConfirmModal from "@/components/Modals/ConfirmModal.vue";
import useConfirmModal from "@/use/useModalWindow";

const uxStore = useUxStore();

const { isModalOpen, openModal, header, context } = useConfirmModal();

const route = useRoute()
const authStore = useAuthStore()
const studentsStore = useStudentsStore()
const { studentsAdditional } = storeToRefs(studentsStore);
const { role } = storeToRefs(authStore);

onMounted(() => {
  studentsStore.resetMistakeVariables();
  uxStore.isLoading = true;
  if (Object.keys(route.query).length > 0) {
    studentsStore.getAllAdditionalWithQuery(Object.keys(route.query)[0], route.query[Object.keys(route.query)[0]]).then(() => {
      uxStore.isLoading = false;
    })
  } else {
    studentsStore.getAllAdditional().then(() => {
      uxStore.isLoading = false;
    })
  }
})

const breadcrumbPathsForAdmin = [
  { path: "/students", name: "Talyplar" },
  { path: "/students/add", name: "Goşmak" },
]
const breadcrumbPaths = [
  { path: "/students", name: "Talyplar" },
]


function submitModal() {
  studentsStore.updateStudyYears().then(() => {
    studentsStore.getAllAdditional();
  });
  isModalOpen.value = false;
}


</script>

<template>
  <confirm-modal :is-open="isModalOpen" @close="isModalOpen = false;" @submit="submitModal" :header="header"
    :context='context'></confirm-modal>
  <div class="w-full">
    <the-breadcrumb :paths="breadcrumbPathsForAdmin" v-if="role === 'root'"></the-breadcrumb>
    <the-breadcrumb :paths="breadcrumbPaths" v-else></the-breadcrumb>
    <div v-if="uxStore.isLoading"
      class="flex w-full h-[58vh] items-center justify-center dark:bg-[#171131ef] bg-white rounded-lg border border-gray-200 dark:border-[#36314e]">
      <the-spinner class="w-24"></the-spinner>
    </div>
    <div v-else>
      <students-data-table :data="studentsAdditional" @update="studentsStore.getAllAdditional()"></students-data-table>
    </div>
  </div>
  <the-toolbar v-slot="{ isActive }">
    <toolbar-button
      :on-click="() => { openModal('Kursy üýtgetme', 'Ähli talyplaryň kursunyň üýtgetdilmegini tassyklaýarsyňyzmy?') }"
      :is-active="isActive">
      <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="w-6" viewBox="0 0 32 32" id="icon">
        <defs>
        </defs>
        <path d="M21,24H11a2,2,0,0,0-2,2v2a2,2,0,0,0,2,2H21a2,2,0,0,0,2-2V26A2,2,0,0,0,21,24Zm0,4H11V26H21Z" />
        <path
          d="M28.707,14.293l-12-12a.9994.9994,0,0,0-1.414,0l-12,12A1,1,0,0,0,4,16H9v4a2.0023,2.0023,0,0,0,2,2H21a2.0027,2.0027,0,0,0,2-2V16h5a1,1,0,0,0,.707-1.707ZM21,14v6H11V14H6.4141L16,4.4141,25.5859,14Z" />
        <rect id="_Transparent_Rectangle_" width="32" height="32" fill="none" />
      </svg>
    </toolbar-button>
  </the-toolbar>
</template>

<style scoped></style>
