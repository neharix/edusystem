<script setup>
import router from '@/router';
import { useStatementsStore } from '@/stores/api.store';
import { useRoute } from 'vue-router';

const props = defineProps(['class'])
defineEmits(['submit-click', 'reject-click']);

</script>
<template>
  <div class="mt-4" :class="class">
    <div class="inline-flex rounded-md shadow-xs" role="group">
      <button type="button" @click="$emit('submit-click')"
        class="px-4 py-2 text-[0.8rem] font-medium bg-emerald-400 hover:bg-emerald-500 transition ease-in hover:ease-out duration-200 text-white dark:bg-emerald-700 border border-gray-200 rounded-s-lg focus:z-10 focus:ring-2 focus:ring-emerald-500 dark:border-gray-700 select-none">
        Tassyklamak
      </button>
      <button type="button" @click="$emit('reject-click')"
        class="px-4 py-2 text-[0.8rem] font-medium bg-red-400 hover:bg-red-500 transition ease-in hover:ease-out duration-200 text-white dark:bg-pink-900 dark:hover:bg-pink-600 border border-gray-200 rounded-e-lg focus:z-10 focus:ring-2 focus:ring-red-500 dark:border-gray-700  dark:focus:ring-pink-500 select-none">
        Ret etmek
      </button>
    </div>
  </div>
</template>
