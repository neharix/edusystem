<script setup>

import SidebarLink from "@/components/SidebarLink.vue";
import TabBar from "@/components/TabBar.vue";
import TabItem from "@/components/TabItem.vue";
import {ref} from "vue";

const selectedTab = ref("hs");


</script>

<template>
  <div class="lg:p-8 lg:pb-4 py-4 px-8 text-2xl font-bold border-gray-200 text-center">Bölümler</div>
  <tab-bar :center="true">
    <tab-item :is-active="selectedTab === 'hs'" @click="selectedTab = 'hs'">
      ÝOM
    </tab-item>
    <tab-item :is-active="selectedTab === 'ss'" @click="selectedTab = 'ss'">
      OHM
    </tab-item>

  </tab-bar>

  <nav class="flex-1 p-4 space-y-2 overflow-y-auto">
    <div v-if="selectedTab === 'hs'">
      <h4 class="uppercase text-gray-400 dark:text-gray-500 p-4">Dolandyryş</h4>
      <sidebar-link link="/high-schools">
        <svg class="w-6" viewBox="0 0 32 32" fill="none"
             xmlns="http://www.w3.org/2000/svg">
          <g clip-path="url(#clip0_901_948)">
            <path
              d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
              stroke-width="2" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>
          </g>
          <defs>
            <clipPath id="clip0_901_948">
              <rect width="32" height="32" fill="white"/>
            </clipPath>
          </defs>
        </svg>
        <span>Ýokary okuw mek...</span>
      </sidebar-link>
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
    </div>
    <div v-if="selectedTab === 'ss'">
      <sidebar-link link="/secondary-schools">Secondary Schools</sidebar-link>
    </div>
  </nav>
</template>

<style scoped>

</style>
