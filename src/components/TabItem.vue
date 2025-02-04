<template>
  <li class="me-2">
    <button
      :class="{
        'inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300': !isActive,
        'inline-block p-4 text-blue-600 border-b-2 border-blue-600 rounded-t-lg active dark:text-violet-500 dark:border-violet-500': isActive,
      }" class="transition duration-200 ease-in-out select-none">
      <slot name="default"></slot>
    </button>
  </li>
</template>

<script>
export default {
  props: {
    isActive: {
      type: Boolean,
      required: false,
      default: false,
    },
  }
}
</script>


<style scoped>

</style>
