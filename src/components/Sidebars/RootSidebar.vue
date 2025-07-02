<script setup>

import SidebarLink from "@/components/SidebarLink.vue";
import TabBar from "@/components/TabBar.vue";
import TabItem from "@/components/TabItem.vue";
import { computed, onMounted, ref } from "vue";
import { useUxStore } from "@/stores/ux.store.js";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth.store";


const selectedTab = ref("hs");

const uxStore = useUxStore();
const authStore = useAuthStore();

const { sidebarExpanded, sidebarHover } = storeToRefs(uxStore);
const { notifications } = storeToRefs(authStore);


const expulsionStatementsCount = computed(() => {
  return notifications.value.filter((e) => { return e.type === 'expulsion' }).length
})
const reinstateStatementsCount = computed(() => {
  return notifications.value.filter((e) => { return e.type === 'reinstate' }).length
})
const diplomaStatementsCount = computed(() => {
  return notifications.value.filter((e) => { return e.type === 'diploma' }).length
})
const teacherStatementsCount = computed(() => {
  return notifications.value.filter((e) => { return e.type === 'teacher' }).length
})


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
              <path d="M9 17H15" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                stroke-linejoin="round" />
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
        <sidebar-link link="/degrees">
          <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">
            <svg class="w-6" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"
              id="Layer_1" viewBox="0 0 32 32" enable-background="new 0 0 32 32" xml:space="preserve">
              <polyline fill="none" stroke="currentColor" stroke-width="2" stroke-miterlimit="10"
                points="17.4,21 21.3,26.9 22.7,23.6 26.3,23.6   22.6,18 " />
              <polyline fill="none" stroke="currentColor" stroke-width="2" stroke-miterlimit="10"
                points="14.6,21 10.7,26.9 9.3,23.6 5.7,23.6   9.4,18 " />
              <path fill="none" stroke="currentColor" stroke-width="2" stroke-miterlimit="10"
                d="M17.2,4.4L19,5.7L21.2,6c0.9,0.1,1.6,0.8,1.7,1.7  l0.4,2.2l1.3,1.8c0.5,0.7,0.5,1.7,0,2.5L23.3,16L23,18.2c-0.1,0.9-0.8,1.6-1.7,1.7L19,20.3l-1.8,1.3c-0.7,0.5-1.7,0.5-2.5,0L13,20.3  L10.8,20c-0.9-0.1-1.6-0.8-1.7-1.7L8.7,16l-1.3-1.8c-0.5-0.7-0.5-1.7,0-2.5L8.7,10L9,7.8C9.2,6.9,9.9,6.2,10.8,6L13,5.7l1.8-1.3  C15.5,3.9,16.5,3.9,17.2,4.4z" />
            </svg>
          </div>
          <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Hünär derejeleri</span>
        </sidebar-link>
        <sidebar-link link="/classificators">
          <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6" viewBox="0 0 24 24" fill="none">
              <path d="M7.80005 10.2V14.3999" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
                stroke-linejoin="round" />
              <path
                d="M7.95001 9.89999C9.02697 9.89999 9.90002 9.02697 9.90002 7.95001C9.90002 6.87306 9.02697 6 7.95001 6C6.87306 6 6 6.87306 6 7.95001C6 9.02697 6.87306 9.89999 7.95001 9.89999Z"
                stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
              <path
                d="M7.79999 17.9999C8.7941 17.9999 9.59998 17.194 9.59998 16.1999C9.59998 15.2058 8.7941 14.3999 7.79999 14.3999C6.80588 14.3999 6 15.2058 6 16.1999C6 17.194 6.80588 17.9999 7.79999 17.9999Z"
                stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
              <path
                d="M16.2 17.9999C17.1941 17.9999 18 17.194 18 16.1999C18 15.2058 17.1941 14.3999 16.2 14.3999C15.2059 14.3999 14.4 15.2058 14.4 16.1999C14.4 17.194 15.2059 17.9999 16.2 17.9999Z"
                stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
              <path
                d="M7.88 10.2C8.15 11.25 9.10999 12.0299 10.24 12.0199L12.3 12.0099C13.87 11.9999 15.21 13.01 15.7 14.42"
                stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
              <path d="M9 22H15C20 22 22 20 22 15V9C22 4 20 2 15 2H9C4 2 2 4 2 9V15C2 20 4 22 9 22Z"
                stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
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
        <sidebar-link link="/graduates">
          <div class="flex justify-center" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">
            <svg class="w-5" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
              fill="currentColor" version="1.1" id="Capa_1" viewBox="0 0 401.168 401.168" xml:space="preserve">
              <g>
                <g>
                  <path
                    d="M401.004,250.538c-0.834-5.295-4.759-9.572-9.961-10.859c-0.872-0.215-71.379-17.925-123.181-49.804l-56.563-56.576    c-31.844-51.777-49.596-122.305-49.811-123.174c-1.286-5.203-5.565-9.128-10.859-9.962c-5.293-0.834-10.572,1.585-13.396,6.14    l-17.078,27.542c-9.682-8.729-24.245-12.872-36.144-9.729l-0.973,0.259C40.87,37.292,14.092,64.07,1.175,106.237l-0.258,0.974    c-2.961,13.143,1.392,27.9,11.09,37.599c0.729,0.729,1.494,1.433,2.272,2.092l0.294,0.241    c32.075,25.631,63.309,52.74,93.259,80.913c-26.838,14.876-50.168,22.272-67.996,21.479c-2.969-0.133-5.679,1.683-6.688,4.479    s-0.084,5.923,2.286,7.719l20.133,15.26l-22.844,21.916c-1.961,1.882-2.611,4.751-1.653,7.293    c0.348,0.924,0.882,1.737,1.552,2.407c1.177,1.178,2.772,1.906,4.501,1.982c20.176,0.897,42.373-3.433,66.34-12.889    c-9.457,23.967-13.786,46.163-12.889,66.339c0.077,1.729,0.806,3.325,1.983,4.502c0.67,0.67,1.485,1.204,2.408,1.552    c2.542,0.958,5.412,0.31,7.293-1.651l21.917-22.846l15.258,20.136c1.796,2.367,4.922,3.295,7.718,2.283    c2.795-1.009,4.61-3.72,4.478-6.688c-0.792-17.828,6.604-41.159,21.481-67.999c28.188,29.964,55.298,61.198,80.914,93.263    l0.243,0.3c0.657,0.774,1.359,1.536,2.086,2.266c9.698,9.698,24.457,14.053,37.601,11.094l0.978-0.259    c42.17-12.923,68.947-39.7,81.861-81.865c0,0,7.035-21.217-9.47-37.115l27.542-17.076    C399.419,261.109,401.838,255.832,401.004,250.538z M144.092,45.804c2.646,8.297,5.908,17.908,9.772,28.236    c-5.276-6.201-10.505-12.439-15.675-18.717L144.092,45.804z M131.16,213.438c-31.956-30.331-65.39-59.483-99.773-86.967    c-0.182-0.159-0.363-0.328-0.539-0.504c-3.135-3.135-5.27-8.371-4.02-12.497c10.398-33.443,30-53.046,63.446-63.445    c3.783-1.262,9.22-0.221,13,4.559c2.096,2.622,4.204,5.238,6.319,7.85l4.047,4.964c24.407,29.881,50.045,58.988,76.598,86.963    L131.16,213.438z M351.141,310.894c-10.395,33.441-29.996,53.046-63.441,63.446c-4.096,0.889-9.366-0.887-12.501-4.021    c-0.175-0.177-0.345-0.354-0.501-0.535c-27.465-34.371-56.617-67.807-86.965-99.775l59.076-59.075    c27.979,26.561,57.088,52.198,86.968,76.603l4.958,4.041c2.61,2.115,5.229,4.225,7.854,6.32c0.181,0.157,0.36,0.325,0.535,0.501    C350.255,301.531,352.291,306.884,351.141,310.894z M345.843,262.979c-6.276-5.17-12.517-10.397-18.72-15.677    c10.33,3.864,19.943,7.126,28.241,9.773L345.843,262.979z" />
                </g>
              </g>
            </svg>
          </div>
          <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Uçurymlar</span>
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
          <div class="flex justify-center relative" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">

            <svg xmlns="http://www.w3.org/2000/svg" class="w-6" viewBox="0 0 24 24" fill="none">
              <path fill-rule="evenodd" clip-rule="evenodd"
                d="M9.29289 1.29289C9.48043 1.10536 9.73478 1 10 1H18C19.6569 1 21 2.34315 21 4V20C21 21.6569 19.6569 23 18 23H6C4.34315 23 3 21.6569 3 20V8C3 7.73478 3.10536 7.48043 3.29289 7.29289L9.29289 1.29289ZM18 3H11V8C11 8.55228 10.5523 9 10 9H5V20C5 20.5523 5.44772 21 6 21H18C18.5523 21 19 20.5523 19 20V4C19 3.44772 18.5523 3 18 3ZM6.41421 7H9V4.41421L6.41421 7ZM7 13C7 12.4477 7.44772 12 8 12H16C16.5523 12 17 12.4477 17 13C17 13.5523 16.5523 14 16 14H8C7.44772 14 7 13.5523 7 13ZM7 17C7 16.4477 7.44772 16 8 16H16C16.5523 16 17 16.4477 17 17C17 17.5523 16.5523 18 16 18H8C7.44772 18 7 17.5523 7 17Z"
                fill="currentColor" />
            </svg>
            <div v-if="expulsionStatementsCount + reinstateStatementsCount > 0"
              class="bg-red-500 px-1.5 py-0.5 text-white text-xs rounded-full absolute -top-2 -right-2">{{
                expulsionStatementsCount + reinstateStatementsCount
              }}</div>
          </div>
          <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Arzalar</span>
        </sidebar-link>
        <sidebar-link link="/diplomas">
          <div class="flex justify-center relative" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">

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
            <div v-if="diplomaStatementsCount > 0"
              class="bg-red-500 px-1.5 py-0.5 text-white text-xs rounded-full absolute -top-2 -right-2">{{
                diplomaStatementsCount
              }}</div>
          </div>
          <span v-if="sidebarExpanded || sidebarHover" class="text-nowrap">Diplomlar</span>
        </sidebar-link>
        <sidebar-link link="/teachers">
          <div class="flex justify-center relative" :class="{ 'w-full': !sidebarExpanded && !sidebarHover }">
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
            <div v-if="teacherStatementsCount > 0"
              class="bg-red-500 px-1.5 py-0.5 text-center text-white text-xs rounded-full absolute -top-2 -right-2">
              {{
                teacherStatementsCount
              }}</div>
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
