<script setup>

import SidebarLink from "@/components/SidebarLink.vue";
</script>

<template>
  <nav class="flex-1 p-4 space-y-2 overflow-y-auto">
    <h4 class="uppercase text-gray-400 dark:text-gray-500 p-4">Dolandyryş</h4>
    <sidebar-link link="/faculties">
      <svg class="w-6"
           xmlns="http://www.w3.org/2000/svg"
           fill="none"
           viewBox="0 0 24 24"
           strokeWidth="4"
           stroke="currentColor"
      >
        <path
          strokeLinecap="round"
          strokeLineJoin="round"
          d="M16.5 3.75V16.5L12 14.25 7.5 16.5V3.75m9 0H18A2.25 2.25 0 0 1 20.25 6v12A2.25 2.25 0 0 1 18 20.25H6A2.25 2.25 0 0 1 3.75 18V6A2.25 2.25 0 0 1 6 3.75h1.5m9 0h-9"
        />
      </svg>
      <span>Fakultetler</span></sidebar-link>
  </nav>
</template>

<style scoped>

</style>
