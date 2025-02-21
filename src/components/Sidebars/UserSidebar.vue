<script setup>

import SidebarLink from "@/components/SidebarLink.vue";
import {useUxStore} from "@/stores/ux.store.js";
import {storeToRefs} from "pinia";

const uxStore = useUxStore();
const {sidebarExpanded, sidebarHover} = storeToRefs(uxStore);

</script>

<template>
  <div class="overflow-y-auto">
  <nav class="flex-1 p-4 space-y-2 overflow-x-hidden">
    <h4 class="uppercase text-gray-400 dark:text-gray-500 p-4 select-none"
        :class="{'text-center font-extrabold': !sidebarExpanded && !sidebarHover}">
      {{ sidebarExpanded || sidebarHover ? "Dolandyryş" : "..." }}</h4>
    <sidebar-link link="/faculties">
      <div class="flex justify-center" :class="{'w-full': !sidebarExpanded && !sidebarHover}">

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
      </div>
      <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Fakultetler</span></sidebar-link>
    <sidebar-link link="/departments">
      <div class="flex justify-center" :class="{'w-full': !sidebarExpanded && !sidebarHover}">

      <svg class="w-6"
           xmlns="http://www.w3.org/2000/svg"
           fill="none"
           viewBox="0 0 24 24"
           strokeWidth="1.5"
           stroke="currentColor"
           className="size-6"
      >
        <path
          strokeLinecap="round"
          strokeLineJoin="round"
          d="M20.25 6.375c0 2.278-3.694 4.125-8.25 4.125S3.75 8.653 3.75 6.375m16.5 0c0-2.278-3.694-4.125-8.25-4.125S3.75 4.097 3.75 6.375m16.5 0v11.25c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125V6.375m16.5 0v3.75m-16.5-3.75v3.75m16.5 0v3.75C20.25 16.153 16.556 18 12 18s-8.25-1.847-8.25-4.125v-3.75m16.5 0c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125"
        />
      </svg>
      </div>
      <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Kafedralar</span></sidebar-link>
    <sidebar-link link="/specializations">
      <div class="flex justify-center" :class="{'w-full': !sidebarExpanded && !sidebarHover}">
      <svg class="w-6"
           xmlns="http://www.w3.org/2000/svg"
           fill="none"
           viewBox="0 0 24 24"
           strokeWidth="1.5"
           stroke="currentColor"
           className="size-6"
      >
        <path
          strokeLinecap="round"
          strokeLineJoin="round"
          d="M3.75 3v11.25A2.25 2.25 0 0 0 6 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0 1 18 16.5h-2.25m-7.5 0h7.5m-7.5 0-1 3m8.5-3 1 3m0 0 .5 1.5m-.5-1.5h-9.5m0 0-.5 1.5m.75-9 3-3 2.148 2.148A12.061 12.061 0 0 1 16.5 7.605"
        />
      </svg>
      </div>
      <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Hünarler</span></sidebar-link>
    <sidebar-link link="/nationalizations">
      <div class="flex justify-center" :class="{'w-full': !sidebarExpanded && !sidebarHover}">
      <svg class="w-6"
           xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"
           stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"
      >
        <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
        <circle cx="12" cy="10" r="3"></circle>
      </svg>
      </div>
      <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Milletler</span></sidebar-link>
    <sidebar-link link="/countries">
      <div class="flex justify-center" :class="{'w-full': !sidebarExpanded && !sidebarHover}">

      <svg class="w-6"
           xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"
           stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"
      >
        <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
        <circle cx="12" cy="10" r="3"></circle>
      </svg>
      </div>
      <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Ýurtlar</span></sidebar-link>
  </nav>
  </div>
</template>

<style scoped>

</style>
