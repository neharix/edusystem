<template>
  <li :class="{'me-2': sidebarExpanded || sidebarHover}">
    <button
      :class="{
        'p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300': !props.isActive,
        'p-4 text-blue-600 border-b-2 border-blue-600 rounded-t-lg active dark:text-violet-500 dark:border-violet-500': props.isActive,
        'inline-block': sidebarExpanded,
        'hidden': !props.isActive && !sidebarExpanded,
      }" class="transition duration-200 ease-in-out select-none">
      <slot name="default"></slot>
    </button>
  </li>
</template>

<script setup>
import {useUxStore} from "@/stores/ux.store.js";
import {storeToRefs} from "pinia";

const props = defineProps({
  isActive: {
    type: Boolean,
    required: false,
    default: false,
  }
})

const uxStore = useUxStore()
const {sidebarExpanded, sidebarHover} = storeToRefs(uxStore);
</script>


<style scoped>

</style>
