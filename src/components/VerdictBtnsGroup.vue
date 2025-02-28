<script setup>
import router from '@/router';
import { useStatementsStore } from '@/stores/api.store';
import { useRoute } from 'vue-router';

const route = useRoute();

const props = defineProps({
  statementType: {
    type: String,
    required: true,
  }
})

const statementsStore = useStatementsStore();

function submitStatement() {
  statementsStore.confirmStatement(route.params.id, props.statementType)
  router.push("/statements");
}


function rejectStatement() {
  statementsStore.rejectStatement(route.params.id, props.statementType)
  router.push("/statements");
}

</script>
<template>
  <div class="mt-4">
    <div class="inline-flex rounded-md shadow-xs" role="group">
      <button type="button" @click="submitStatement()"
        class="px-4 py-2 text-[0.8rem] font-medium bg-emerald-400 hover:bg-emerald-500 transition ease-in hover:ease-out duration-200 text-white dark:bg-emerald-700 border border-gray-200 rounded-s-lg focus:z-10 focus:ring-2 focus:ring-emerald-500 dark:border-gray-700 select-none">
        Tassyklamak
      </button>
      <button type="button" @click="rejectStatement()"
        class="px-4 py-2 text-[0.8rem] font-medium bg-red-400 hover:bg-red-500 transition ease-in hover:ease-out duration-200 text-white dark:bg-pink-900 dark:hover:bg-pink-600 border border-gray-200 rounded-e-lg focus:z-10 focus:ring-2 focus:ring-red-500 dark:border-gray-700  dark:focus:ring-pink-500 select-none">
        Ret etmek
      </button>
    </div>
  </div>
</template>
