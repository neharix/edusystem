<script setup>
import { useTemplateRef } from 'vue';

const drawerToggle = useTemplateRef('drawerToggle');

</script>
<template>
  <button
    class="py-2 select-none text-nowrap px-3 my-2 text-[0.7rem] md:text-sm lg:text-sm rounded-lg shadow-md border-none dark:border-violet-500/50 border-1 bg-blue-500 dark:bg-violet-600 text-white"
    @click="drawerToggle.click()">
    <slot name="btn"></slot>
  </button>
  <div>
    <div class="drawer drawer-end z-40">
      <input id="drawer" type="checkbox" ref="drawerToggle" class="drawer-toggle" />
      <div class="drawer-content">
        <label for="drawer"
          class="hidden drawer-button transition duration-200 ease-in justify-center rounded-md border border-gray-300 dark:border-gray-800 bg-white dark:bg-[#113031] dark:text-gray-200 px-4 py-2 text-[0.75rem] text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 dark:hover:bg-[#113031] focus:outline-none focus:ring-2 focus:ring-emerald-500 dark:focus:ring-[#2e5152] focus:ring-offset-2 focus:ring-offset-gray-100 dark:focus:ring-offset-[#2e5152] select-none"><svg
            class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16m-7 6h7"></path>
          </svg></label>
      </div>
      <div class="drawer-side">
        <label for="drawer" aria-label="close sidebar" class="drawer-overlay"></label>
        <div class="bg-white dark:bg-[#171131] text-base-content min-h-full w-80 p-4">
          <slot name="content"></slot>
        </div>
      </div>
    </div>
  </div>
</template>
