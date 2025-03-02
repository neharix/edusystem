<script setup>

import SidebarLink from "@/components/SidebarLink.vue";
import TabBar from "@/components/TabBar.vue";
import TabItem from "@/components/TabItem.vue";
import { ref } from "vue";
import { useUxStore } from "@/stores/ux.store.js";
import { storeToRefs } from "pinia";


const selectedTab = ref("hs");

const uxStore = useUxStore();
const { sidebarExpanded, sidebarHover } = storeToRefs(uxStore);


</script>

<template>
  <div class=" text-2xl font-bold border-gray-200 text-center select-none py-4 px-8" :class="{
    'font-extrabold': !sidebarExpanded && !sidebarHover,
  }">{{ sidebarExpanded || sidebarHover ? 'Bölümler' : '...' }}
  </div>
  <tab-bar :center="true">
    <tab-item :is-active="selectedTab === 'hs'" @click="selectedTab = 'hs'">
      ÝOM
    </tab-item>
    <!--    <tab-item :is-active="selectedTab === 'ss'" @click="selectedTab = 'ss'">-->
    <!--      OHM-->
    <!--    </tab-item>-->

  </tab-bar>
  <div class="flex justify-center overflow-y-auto">
    <nav class="p-4 space-y-2 overflow-x-hidden"
      :class="{ 'flex-1': sidebarExpanded || sidebarHover, 'flex': !sidebarExpanded && !sidebarHover }">
      <div v-if="selectedTab === 'hs'">
        <sidebar-link link="/">
          <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6" viewBox="0 0 24 24" fill="transparent"
              stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
              <polyline points="9 22 9 12 15 12 15 22"></polyline>
            </svg>

          </div>
          <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Baş sahypa</span>
        </sidebar-link>
        <h4 class="uppercase text-gray-400 dark:text-gray-500 p-4 select-none text-nowrap"
          :class="{ 'text-center font-extrabold': !sidebarExpanded && !sidebarHover }">
          {{ sidebarExpanded || sidebarHover ? "Dolandyryş" : "..." }}</h4>
        <sidebar-link link="/high-schools">
          <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">
            <svg class="w-6" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <g clip-path="url(#clip0_901_948)">
                <path
                  d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
                  stroke-width="2" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" />
              </g>
              <defs>
                <clipPath id="clip0_901_948">
                  <rect width="32" height="32" fill="white" />
                </clipPath>
              </defs>
            </svg>
          </div>
          <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Ýokary okuw mek...</span>
        </sidebar-link>
        <sidebar-link link="/faculties">
          <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">
            <svg class="w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="4"
              stroke="currentColor">
              <path strokeLinecap="round" strokeLineJoin="round"
                d="M16.5 3.75V16.5L12 14.25 7.5 16.5V3.75m9 0H18A2.25 2.25 0 0 1 20.25 6v12A2.25 2.25 0 0 1 18 20.25H6A2.25 2.25 0 0 1 3.75 18V6A2.25 2.25 0 0 1 6 3.75h1.5m9 0h-9" />
            </svg>
          </div>
          <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Fakultetler</span>
        </sidebar-link>
        <sidebar-link link="/departments">
          <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">
            <svg class="w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.3"
              stroke="currentColor">
              <path strokeLinecap="round" strokeLineJoin="round"
                d="M20.25 6.375c0 2.278-3.694 4.125-8.25 4.125S3.75 8.653 3.75 6.375m16.5 0c0-2.278-3.694-4.125-8.25-4.125S3.75 4.097 3.75 6.375m16.5 0v11.25c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125V6.375m16.5 0v3.75m-16.5-3.75v3.75m16.5 0v3.75C20.25 16.153 16.556 18 12 18s-8.25-1.847-8.25-4.125v-3.75m16.5 0c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125" />
            </svg>
          </div>
          <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Kafedralar</span>
        </sidebar-link>
        <sidebar-link link="/specializations">
          <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">
            <svg class="w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5"
              stroke="currentColor" className="size-6">
              <path strokeLinecap="round" strokeLineJoin="round"
                d="M3.75 3v11.25A2.25 2.25 0 0 0 6 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0 1 18 16.5h-2.25m-7.5 0h7.5m-7.5 0-1 3m8.5-3 1 3m0 0 .5 1.5m-.5-1.5h-9.5m0 0-.5 1.5m.75-9 3-3 2.148 2.148A12.061 12.061 0 0 1 16.5 7.605" />
            </svg>
          </div>
          <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Hünarler</span>
        </sidebar-link>
        <sidebar-link link="/nationalizations">
          <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">
            <svg class="w-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"
              stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
              <circle cx="12" cy="10" r="3"></circle>
            </svg>
          </div>
          <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Milletler</span>
        </sidebar-link>
        <sidebar-link link="/countries">
          <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">
            <svg class="w-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"
              stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
              <circle cx="12" cy="10" r="3"></circle>
            </svg>
          </div>
          <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Ýurtlar</span>
        </sidebar-link>
        <sidebar-link link="/regions">
          <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">
            <svg class="w-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"
              stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
              <circle cx="12" cy="10" r="3"></circle>
            </svg>
          </div>
          <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Welaýatlar</span>
        </sidebar-link>
        <sidebar-link link="/degrees">
          <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6" viewBox="0 0 24 24" fill="transparent"
              stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="7" height="7"></rect>
              <rect x="14" y="3" width="7" height="7"></rect>
              <rect x="14" y="14" width="7" height="7"></rect>
              <rect x="3" y="14" width="7" height="7"></rect>
            </svg>
          </div>
          <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Hünär derejeleri</span>
        </sidebar-link>
        <sidebar-link link="/classificators">
          <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6" viewBox="0 0 24 24" fill="transparent"
              stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="7" height="7"></rect>
              <rect x="14" y="3" width="7" height="7"></rect>
              <rect x="14" y="14" width="7" height="7"></rect>
              <rect x="3" y="14" width="7" height="7"></rect>
            </svg>
          </div>
          <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Klassifikatorlar</span>
        </sidebar-link>
        <h4 class="uppercase text-gray-400 dark:text-gray-500 p-4 select-none text-nowrap"
          :class="{ 'text-center font-extrabold': !sidebarExpanded && !sidebarHover }">
          {{ sidebarExpanded || sidebarHover ? "Okuw işleri" : "..." }}</h4>
        <sidebar-link link="/students">
          <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">
            <svg class="w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"
              stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
          </div>
          <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Talyplar</span>
        </sidebar-link>
        <sidebar-link link="/expulsion-reasons">
          <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6" viewBox="0 0 24 24" fill="transparent"
              stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="7" height="7"></rect>
              <rect x="14" y="3" width="7" height="7"></rect>
              <rect x="14" y="14" width="7" height="7"></rect>
              <rect x="3" y="14" width="7" height="7"></rect>
            </svg>
          </div>
          <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Okuwdan çykarmak</span>
        </sidebar-link>
        <sidebar-link link="/statements">
          <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">

            <svg xmlns="http://www.w3.org/2000/svg" class="w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor"
              stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path
                d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z">
              </path>
              <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
              <line x1="12" y1="22.08" x2="12" y2="12"></line>
            </svg>
          </div>
          <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Arzalar</span>
        </sidebar-link>
        <sidebar-link link="/diplomas">
          <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">

            <svg xmlns="http://www.w3.org/2000/svg" class="w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor"
              stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path
                d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z">
              </path>
              <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
              <line x1="12" y1="22.08" x2="12" y2="12"></line>
            </svg>
          </div>
          <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Diplomlar</span>
        </sidebar-link>
        <sidebar-link link="/teachers">
          <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">

            <svg xmlns="http://www.w3.org/2000/svg" class="w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor"
              stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path
                d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z">
              </path>
              <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
              <line x1="12" y1="22.08" x2="12" y2="12"></line>
            </svg>
          </div>
          <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Mugallymlar</span>
        </sidebar-link>
        <h4 class="uppercase text-gray-400 dark:text-gray-500 p-4 select-none text-nowrap"
          :class="{ 'text-center font-extrabold': !sidebarExpanded && !sidebarHover }">
          {{ sidebarExpanded || sidebarHover ? "Gurallar" : "..." }}</h4>
        <sidebar-link link="/filter">
          <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">

            <svg xmlns="http://www.w3.org/2000/svg" class="w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor"
              stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
            </svg>
          </div>
          <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Süzgüç</span>
        </sidebar-link>


        <div class="h-16"></div>


      </div>
      <div v-if="selectedTab === 'ss'">
        <sidebar-link link="/secondary-schools">Secondary Schools</sidebar-link>
      </div>
    </nav>
  </div>
</template>

<style scoped></style>
