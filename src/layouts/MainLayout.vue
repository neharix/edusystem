<template>
  <div id="sidebar" @mouseover="uxStore.mouseOverSidebar()" @mouseleave="uxStore.mouseLeaveSidebar()"
    :class="{ '-translate-x-full': showSidebar === false, 'w-64': sidebarExpanded || sidebarHover, 'w-25': !sidebarExpanded }"
    class="fixed z-30 shadow-md inset-y-0 left-0 bg-white/90 lg:bg-white text-gray-800 dark:text-white dark:bg-[#171131ef] lg:dark:bg-[#171131] flex flex-col transform duration-200 ease-out lg:translate-x-0 transition-all">
    <div class="flex items-center justify-between py-8 px-4 lg:hidden">
      <div class="w-10 h-10 rounded-full bg-gray-200 dark:bg-gray-800 overflow-hidden">
        <img src="../assets/svgs/favicon.svg" alt="User Avatar" />
      </div>
      <div>
        <p class="m-0 text-gray-900 dark:text-gray-100 font-medium select-none" v-if="user">
          {{ user.is_superuser ? 'Admin' : user.manager_of }}
        </p>
        <p class="m-0 text-gray-600 dark:text-gray-300 font-medium text-[0.8rem] select-none" v-if="user">
          {{ user.is_superuser ? "Admin" : "ÝOM" }}</p>
      </div>
      <div>
        <button @click="authStore.logout()"
          class="bg-none w-full flex items-center text-red-500 text-sm rounded-2xl hover:bg-gray-100 dark:hover:bg-[#261c52ef]">
          <svg class="w-6" viewBox="0 -0.5 25 25" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path
              d="M11.75 9.874C11.75 10.2882 12.0858 10.624 12.5 10.624C12.9142 10.624 13.25 10.2882 13.25 9.874H11.75ZM13.25 4C13.25 3.58579 12.9142 3.25 12.5 3.25C12.0858 3.25 11.75 3.58579 11.75 4H13.25ZM9.81082 6.66156C10.1878 6.48991 10.3542 6.04515 10.1826 5.66818C10.0109 5.29121 9.56615 5.12478 9.18918 5.29644L9.81082 6.66156ZM5.5 12.16L4.7499 12.1561L4.75005 12.1687L5.5 12.16ZM12.5 19L12.5086 18.25C12.5029 18.25 12.4971 18.25 12.4914 18.25L12.5 19ZM19.5 12.16L20.2501 12.1687L20.25 12.1561L19.5 12.16ZM15.8108 5.29644C15.4338 5.12478 14.9891 5.29121 14.8174 5.66818C14.6458 6.04515 14.8122 6.48991 15.1892 6.66156L15.8108 5.29644ZM13.25 9.874V4H11.75V9.874H13.25ZM9.18918 5.29644C6.49843 6.52171 4.7655 9.19951 4.75001 12.1561L6.24999 12.1639C6.26242 9.79237 7.65246 7.6444 9.81082 6.66156L9.18918 5.29644ZM4.75005 12.1687C4.79935 16.4046 8.27278 19.7986 12.5086 19.75L12.4914 18.25C9.08384 18.2892 6.28961 15.5588 6.24995 12.1513L4.75005 12.1687ZM12.4914 19.75C16.7272 19.7986 20.2007 16.4046 20.2499 12.1687L18.7501 12.1513C18.7104 15.5588 15.9162 18.2892 12.5086 18.25L12.4914 19.75ZM20.25 12.1561C20.2345 9.19951 18.5016 6.52171 15.8108 5.29644L15.1892 6.66156C17.3475 7.6444 18.7376 9.79237 18.75 12.1639L20.25 12.1561Z"
              fill="currentColor" />
          </svg>
        </button>
      </div>
    </div>
    <button @click="uxStore.toggleSidebar" class="hidden lg:flex lg:justify-center mt-4">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor"
        stroke-width="2" stroke-linecap="round" stroke-linejoin="round" v-if="!sidebarExpanded">
        <circle cx="12" cy="12" r="10"></circle>
      </svg>
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5" viewBox="0 0 24 24" fill="none" v-else stroke="currentColor"
        stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <circle cx="12" cy="12" r="3"></circle>
      </svg>
    </button>
    <component :is="sidebar"></component>


  </div>
  <!-- Overlay -->
  <div id="overlay" :class="{ hidden: showSidebar === false }"
    class="fixed inset-0 z-10 bg-black/50 lg:hidden transition-colors duration-200 ease-out"
    @click="showSidebar = !showSidebar"></div>
  <!-- Main Content -->
  <div class="flex-1 flex flex-col dark:bg-[#1b1829] bg-gray-100 transition-all duration-200 ease-out"
    :class="{ 'lg:pl-64': sidebarExpanded, 'lg:pl-24': !sidebarExpanded }">
    <!-- Navbar -->
    <div :class="showSidebar ? 'bg-white/25 dark:bg-[#1711313b]' : 'bg-white/90 dark:bg-[#171131ef]'"
      class=" lg:bg-white text-gray-800 dark:text-white lg:dark:bg-[#171131] shadow-md dark:shadow-lg rounded-2xl sticky top-0 z-10 flex justify-between items-center p-4 lg:m-4 lg:mt-4 m-4 lg:mb-0 mb-0">
      <button id="menuButton" class="lg:hidden px-4 py-2 rounded" @click="showSidebar = !showSidebar">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16m-7 6h7"></path>
        </svg>
      </button>
      <router-link to="/">
        <div class="text-xl font-semibold flex items-center"><img class="w-12 h-12 select-none"
            src="/src/assets/svgs/favicon.svg" alt=""><span class="px-2 select-none">BMDU</span></div>
      </router-link>

      <site-tools :is-mobile="true" :is-dark="isDark"
        :notifications="user.is_superuser && user.notifications.length > 0" @toggle-theme="toggleTheme"></site-tools>
      <div class="hidden lg:flex items-center space-x-4">
        <site-tools :is-mobile="false" :is-dark="isDark"
          :notifications="user.is_superuser && user.notifications.length > 0" @toggle-theme="toggleTheme"></site-tools>
        <user-dropdown v-if="user"></user-dropdown>
      </div>
    </div>
    <!-- Page Content -->
    <div class="flex-1 p-6 text-gray-800 dark:text-gray-100 overflow-y-auto lg:w-full w-screen">
      <router-view></router-view>
      <div class="mt-8">
        <p class="select-none lg:text-end md:text-end text-center text-[0.75rem] text-gray-500 dark:text-gray-400">
          &copy; {{ year }} "Sanly Çözgüt IT Meýdança" HJ,
          Ähli hukuklar
          goralan</p>
      </div>
    </div>
  </div>

</template>

<script setup>
import { onBeforeMount, onMounted, ref, shallowRef, watch } from "vue";
import SiteTools from "@/components/SiteTools.vue";
import { useAuthStore } from '@/stores/auth.store.js';
import UserDropdown from "@/components/UserDropdown.vue";
import { storeToRefs } from "pinia";
import RootSidebar from "@/components/Sidebars/RootSidebar.vue";
import UserSidebar from "@/components/Sidebars/UserSidebar.vue";
import EmptySidebar from "@/components/Sidebars/EmptySidebar.vue";
import { useUxStore } from "@/stores/ux.store.js";

const uxStore = useUxStore();
const { sidebarExpanded, sidebarHover } = storeToRefs(uxStore);

const authStore = useAuthStore();


const { user, role } = storeToRefs(authStore);
const sidebar = shallowRef(EmptySidebar);
const showSidebar = ref(false);
const isDark = ref(null)
const year = ref(new Date().getFullYear())


function toggleTheme() {
  const html = document.documentElement;
  const prevTheme = html.classList.contains('dark') ? 'dark' : 'light'
  html.classList.remove(prevTheme)
  html.classList.add(prevTheme === "dark" ? "light" : "dark")

  localStorage.setItem('theme', html.classList.contains('dark') ? 'dark' : 'light');
  const theme = localStorage.getItem("theme");

  html.classList.add(theme)
  html.classList.remove(theme === "dark" ? "light" : "dark")
  isDark.value = theme === "dark";

}


if (role.value === "root") {
  sidebar.value = RootSidebar;
} else if (role.value === "user") {
  sidebar.value = UserSidebar;
} else if (role.value === "empty") {
  sidebar.value = EmptySidebar;
}

watch(role, (newValue, oldValue) => {
  if (newValue === "root") {
    sidebar.value = RootSidebar;
  } else if (newValue === "user") {
    sidebar.value = UserSidebar;
  } else if (newValue === "empty") {
    sidebar.value = EmptySidebar;
  }
})


onMounted(() => {
  if (!(document.body.classList.contains("main-layout"))) {
    document.body.className = "";
    document.body.classList.add("main-layout", "font-montserrat", "antialiased", "bg-gray-100", "relative", "w-screen");
  }

  const theme = localStorage.getItem("theme")
  if (theme !== null) {
    document.querySelector("html").setAttribute("class", theme)
    isDark.value = theme === "dark"

  } else {
    localStorage.setItem("theme", "light")
    document.querySelector("html").setAttribute("class", "light")
    isDark.value = false
  }

})
</script>

<style scoped></style>
