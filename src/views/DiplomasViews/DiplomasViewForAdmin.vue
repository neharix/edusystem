<script setup>
import { useDiplomasStore } from '@/stores/api.store';
import { onBeforeMount } from 'vue';
import DiplomaRequestsDataTable from '@/components/DataTables/DiplomaRequestsDataTable.vue';
import DiplomaActionsDataTable from '@/components/DataTables/DiplomaActionsDataTable.vue';
import { storeToRefs } from 'pinia';

const diplomasStore = useDiplomasStore();
const { diplomaRequests, diplomaActions } = storeToRefs(diplomasStore)

onBeforeMount(() => {
  diplomasStore.getAllForTable();
  diplomasStore.getActions();
})

</script>
<template>
  <div class="grid grid-cols-2 lg:grid-cols-3 lg:gap-x-8 lg:gap-y-0 gap-x-0 gap-y-8">
    <div class="col-span-2">
      <diploma-requests-data-table :data="diplomaRequests"
        @update="diplomasStore.getAllForTable()"></diploma-requests-data-table>
    </div>
    <div class="col-span-2 lg:col-span-1">
      <diploma-actions-data-table :data="diplomaActions"
        @update="diplomasStore.getActions()"></diploma-actions-data-table>
    </div>
  </div>
</template>
