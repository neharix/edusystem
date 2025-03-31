<script setup>
import { useDiplomasStore } from '@/stores/api.store';
import { onBeforeMount, ref } from 'vue';
import DiplomaRequestsDataTable from '@/components/DataTables/DiplomaRequestsDataTable.vue';
import DiplomaActionsDataTable from '@/components/DataTables/DiplomaActionsDataTable.vue';
import { storeToRefs } from 'pinia';
import TheSpinner from '@/components/TheSpinner.vue';

const diplomasStore = useDiplomasStore();
const { diplomaRequests, diplomaActions } = storeToRefs(diplomasStore);
const isRequestsLoading = ref(false);
const isActionsLoading = ref(false);

onBeforeMount(() => {
  isRequestsLoading.value = true;
  isActionsLoading.value = true;
  diplomasStore.getAllForTable().then(() => {
    isRequestsLoading.value = false;
  });
  diplomasStore.getActions().then(() => {
    isActionsLoading.value = false;
  });
})

</script>
<template>
  <div class="grid grid-cols-2 lg:grid-cols-3 lg:gap-x-8 lg:gap-y-0 gap-x-0 gap-y-8">
    <div class="col-span-2">
      <diploma-requests-data-table v-if="!isRequestsLoading" :data="diplomaRequests"
        @update="diplomasStore.getAllForTable()"></diploma-requests-data-table>
      <div v-else
        class="flex w-full h-[58vh] items-center justify-center dark:bg-[#171131ef] bg-white rounded-lg border border-gray-200 dark:border-[#36314e]">
        <the-spinner class="w-24"></the-spinner>
      </div>
    </div>
    <div class="col-span-2 lg:col-span-1">
      <diploma-actions-data-table v-if="!isActionsLoading" :data="diplomaActions"
        @update="diplomasStore.getActions()"></diploma-actions-data-table>
      <div v-else
        class="flex w-full h-[58vh] items-center justify-center dark:bg-[#171131ef] bg-white rounded-lg border border-gray-200 dark:border-[#36314e]">
        <the-spinner class="w-24"></the-spinner>
      </div>
    </div>
  </div>
</template>
