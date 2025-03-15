<script setup>
defineProps({
  onClick: {
    type: Function,
    required: true,
  },
  isActive: {
    type: Boolean,
    required: true,
  }
})
</script>
<template>

  <button @click="onClick"
    class="px-4 py-2 rounded-full select-none text-gray-700 dark:text-white transition-all duration-1000 ease-out"
    :class="{
      'mt-2 mb-2': isActive,
      'mt-2 mb-0': !isActive,
    }">
    <slot name="default"></slot>
  </button>
</template>
