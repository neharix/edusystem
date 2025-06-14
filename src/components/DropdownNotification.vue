<script setup>
import router from '@/router';

const props = defineProps({
  notification: Object,
  redirectTo: String,
  types: Array,
})
</script>
<template>
  <button @click="router.push(redirectTo)" v-if="types.includes(notification.type)"
    class="bg-none w-full flex items-center text-gray-600 dark:text-gray-200 px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-[#261c52ef] transition duration-300 ease-out">
    <span class="select-none text-wrap text-start">{{ notification.sender }}-den arza goýberilen arza</span>
  </button>
</template>
