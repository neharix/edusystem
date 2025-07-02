<script setup>

import SidebarLink from "@/components/SidebarLink.vue";
import { useUxStore } from "@/stores/ux.store.js";
import { storeToRefs } from "pinia";

const uxStore = useUxStore();
const { sidebarExpanded, sidebarHover } = storeToRefs(uxStore);

</script>


<template>
  <div class="overflow-y-auto">
    <nav class="flex-1 p-4 space-y-2 overflow-x-hidden">
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
      <sidebar-link link="/faculties">
        <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">
          <svg class="w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.3"
            stroke="currentColor">
            <path strokeLinecap="round" strokeLineJoin="round"
              d="M16.5 3.75V16.5L12 14.25 7.5 16.5V3.75m9 0H18A2.25 2.25 0 0 1 20.25 6v12A2.25 2.25 0 0 1 18 20.25H6A2.25 2.25 0 0 1 3.75 18V6A2.25 2.25 0 0 1 6 3.75h1.5m9 0h-9" />
          </svg>
        </div>
        <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Fakultetler</span>
      </sidebar-link>
      <sidebar-link link="/departments">
        <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">

          <svg class="w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5"
            stroke="currentColor" className="size-6">
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
        <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Hünärler</span>
      </sidebar-link>
      <sidebar-link link="/nationalizations">
        <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">
          <svg class="w-6" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 16">
            <path
              d="M8 .5A7.76 7.76 0 0 0 0 8a7.76 7.76 0 0 0 8 7.5A7.76 7.76 0 0 0 16 8 7.76 7.76 0 0 0 8 .5zm6.71 6.8L13.48 7c-.25-.07-.27-.09-.29-.12-.15-.2-.32-.47-.48-.73 0-.09-.13-.23-.16-.31s.35-.6.51-.84a2.43 2.43 0 0 1 .59-.45 5.87 5.87 0 0 1 1.06 2.75zM8 1.75l-.09.17a.19.19 0 0 1 0-.1c0 .06-.15.15-.25.25l-.3.29a.85.85 0 0 0-.08 1.08h-.12a1.05 1.05 0 0 0-.81.42 1.27 1.27 0 0 0-.2 1.07V5a3 3 0 0 0-.43.11l-.24.08-.64.21a1.2 1.2 0 0 0-.81.8 1 1 0 0 0 .2.93 5.67 5.67 0 0 0 1.38 1.09 4.17 4.17 0 0 0 1.67.65h1.68a1.2 1.2 0 0 1 1.04.51.49.49 0 0 1 .13.43.77.77 0 0 1-.15.35 2.71 2.71 0 0 0-.95 1.61 11.11 11.11 0 0 1-.48 1.38c-.12.31-.23.61-.31.85a3.32 3.32 0 0 1-1-.08 3.28 3.28 0 0 0-.5-2.12 2.24 2.24 0 0 1-.53-1.42 2.11 2.11 0 0 0-1.47-2.29 10.81 10.81 0 0 1-2.9-2.64A6.79 6.79 0 0 1 8 1.75zM1.25 8a5.64 5.64 0 0 1 .12-1.16 10.29 10.29 0 0 0 2.94 2.42c.6.22.69.45.69 1.12a3.45 3.45 0 0 0 .86 2.27A3.05 3.05 0 0 1 6 14a6.35 6.35 0 0 1-4.75-6zm8.32 6.08c0-.15.12-.32.18-.48a10.2 10.2 0 0 0 .55-1.6 1.55 1.55 0 0 1 .54-.86 1.91 1.91 0 0 0 .57-1.3 1.71 1.71 0 0 0-.47-1.27 2.45 2.45 0 0 0-2-.9H7.35a4.77 4.77 0 0 1-2-1.11l.47-.16.27-.08a.79.79 0 0 1 .38-.07l.09.15a.64.64 0 0 0 .81.29.65.65 0 0 0 .34-.8v-.18c-.11-.3-.24-.72-.32-1A1.42 1.42 0 0 0 8.68 4a1 1 0 0 0-.18-1 3.44 3.44 0 0 0 .33-.34 1 1 0 0 0 .22-.8 6.93 6.93 0 0 1 3.73 1.8 3 3 0 0 0-.79.7 9.14 9.14 0 0 0-.64 1.09 1.46 1.46 0 0 0 .24 1.39c.18.31.38.61.56.86a1.58 1.58 0 0 0 1 .58c.22.06 1 .22 1.55.33a6.44 6.44 0 0 1-5.13 5.47z" />
          </svg>
        </div>
        <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Milletler</span>
      </sidebar-link>
      <sidebar-link link="/countries">
        <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6" viewBox="0 0 24 24" fill="none">
            <rect x="4" y="3" width="16" height="18" rx="1" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" />
            <path d="M9 17H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <circle cx="12" cy="10" r="4.25" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
              stroke-linejoin="round" />
            <path
              d="M13.25 10C13.25 11.3097 13.0363 12.4609 12.7179 13.257C12.5578 13.6571 12.386 13.9306 12.2336 14.0917C12.0837 14.2502 12.0046 14.25 12.0001 14.25H12H11.9999C11.9954 14.25 11.9163 14.2502 11.7664 14.0917C11.614 13.9306 11.4422 13.6571 11.2821 13.257C10.9637 12.4609 10.75 11.3097 10.75 10C10.75 8.69028 10.9637 7.53908 11.2821 6.74301C11.4422 6.34289 11.614 6.06943 11.7664 5.90826C11.9163 5.7498 11.9954 5.74999 11.9999 5.75L12 5.75L12.0001 5.75C12.0046 5.74999 12.0837 5.7498 12.2336 5.90826C12.386 6.06943 12.5578 6.34289 12.7179 6.74301C13.0363 7.53908 13.25 8.69028 13.25 10Z"
              stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
            <path d="M8 10H16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
              stroke-linejoin="round" />
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
      <sidebar-link link="/expelled-students">
        <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="8.5" cy="7" r="4"></circle>
            <polyline points="17 11 19 13 23 9"></polyline>
          </svg>
        </div>
        <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Okuwdan boşadylanlar</span>
      </sidebar-link>

      <sidebar-link link="/diplomas">
        <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="16" r="3" stroke="currentColor" stroke-width="1.5" />
            <path
              d="M12 19.2599L9.73713 21.4293C9.41306 21.74 9.25102 21.8953 9.1138 21.9491C8.80111 22.0716 8.45425 21.9667 8.28977 21.7C8.21758 21.583 8.19509 21.3719 8.1501 20.9496C8.1247 20.7113 8.112 20.5921 8.07345 20.4922C7.98715 20.2687 7.80579 20.0948 7.57266 20.0121C7.46853 19.9751 7.3442 19.963 7.09553 19.9386C6.65512 19.8955 6.43491 19.8739 6.31283 19.8047C6.03463 19.647 5.92529 19.3145 6.05306 19.0147C6.10913 18.8832 6.27116 18.7278 6.59523 18.4171L8.07345 16.9999L9.1138 15.9596"
              stroke="currentColor" stroke-width="1.5" />
            <path
              d="M12 19.2599L14.2629 21.4294C14.5869 21.7401 14.749 21.8954 14.8862 21.9492C15.1989 22.0717 15.5457 21.9668 15.7102 21.7001C15.7824 21.5831 15.8049 21.372 15.8499 20.9497C15.8753 20.7113 15.888 20.5921 15.9265 20.4923C16.0129 20.2688 16.1942 20.0949 16.4273 20.0122C16.5315 19.9752 16.6558 19.9631 16.9045 19.9387C17.3449 19.8956 17.5651 19.874 17.6872 19.8048C17.9654 19.6471 18.0747 19.3146 17.9469 19.0148C17.8909 18.8832 17.7288 18.7279 17.4048 18.4172L15.9265 17L15 16.0735"
              stroke="currentColor" stroke-width="1.5" />
            <path
              d="M17.3197 17.9957C19.2921 17.9748 20.3915 17.8512 21.1213 17.1213C22 16.2426 22 14.8284 22 12V8C22 5.17157 22 3.75736 21.1213 2.87868C20.2426 2 18.8284 2 16 2L8 2C5.17157 2 3.75736 2 2.87868 2.87868C2 3.75736 2 5.17157 2 8L2 12C2 14.8284 2 16.2426 2.87868 17.1213C3.64706 17.8897 4.82497 17.9862 7 17.9983"
              stroke="currentColor" stroke-width="1.5" />
            <path d="M9 6L15 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
            <path d="M7 9.5H17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
          </svg>
        </div>
        <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Diplomlar</span>
      </sidebar-link>
      <sidebar-link link="/teachers">
        <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6" viewBox="0 0 24 24" fill="none">
            <path
              d="M10.05 2.53004L4.03002 6.46004C2.10002 7.72004 2.10002 10.54 4.03002 11.8L10.05 15.73C11.13 16.44 12.91 16.44 13.99 15.73L19.98 11.8C21.9 10.54 21.9 7.73004 19.98 6.47004L13.99 2.54004C12.91 1.82004 11.13 1.82004 10.05 2.53004Z"
              stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
            <path
              d="M5.63 13.08L5.62 17.77C5.62 19.04 6.6 20.4 7.8 20.8L10.99 21.86C11.54 22.04 12.45 22.04 13.01 21.86L16.2 20.8C17.4 20.4 18.38 19.04 18.38 17.77V13.13"
              stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
            <path d="M21.4 15V9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
              stroke-linejoin="round" />
          </svg>
        </div>
        <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Mugallymlar</span>
      </sidebar-link>

    </nav>
  </div>
</template>

<style scoped></style>
