<template>
  <div id="sidebar" :class="{ '-translate-x-full': showSidebar === false }"
    class="fixed shadow-lg inset-y-0 left-0 z-20 w-64 bg-white/90 lg:bg-white text-gray-800 dark:text-white dark:bg-[#171131ef] lg:dark:bg-[#171131] flex flex-col transform transition-transform duration-300 lg:translate-x-0">
    <div class="flex items-center space-x-4 p-8 lg:hidden">
      <div class="w-10 h-10 rounded-full bg-gray-200 overflow-hidden">
        <img src="https://via.placeholder.com/40" alt="User Avatar" />
      </div>
      <div>
        <p class="m-0 text-gray-900 dark:text-gray-100 font-medium">Azat Jurjenow</p>
        <p class="m-0 text-gray-600 dark:text-gray-300 font-medium">@afych</p>
      </div>
    </div>
    <div class="lg:p-8 lg:pb-4 py-4 px-8 text-2xl font-bold border-gray-200">Bölümler</div>
    <!-- User info (видимо только на мобильных) -->
    <nav class="flex-1 p-4 space-y-2 overflow-y-auto">
      <sidebar-link link="/">Home</sidebar-link>
      <a href="#" class="block px-4 py-2 rounded hover:bg-gray-100">Пункт 2</a>
      <a href="#" class="block px-4 py-2 rounded hover:bg-gray-100">Пункт 3</a>
      <a href="#" class="block px-4 py-2 rounded hover:bg-gray-100">Пункт 4</a>
    </nav>
  </div>
  <!-- Overlay -->
  <div id="overlay" :class="{ hidden: showSidebar === false }" class="fixed inset-0 z-10 bg-black/50 lg:hidden"
    @click="showSidebar = !showSidebar"></div>
  <!-- Main Content -->
  <div class="flex-1 flex flex-col lg:pl-64 dark:bg-[#1b1829] bg-gray-100">
    <!-- Navbar -->
    <div :class="showSidebar ? 'bg-white/25 dark:bg-[#1711313b]' : 'bg-white/90 dark:bg-[#171131ef]'"
      class=" lg:bg-white text-gray-800 dark:text-white lg:dark:bg-[#171131] shadow-md rounded-2xl sticky top-0 z-10 flex justify-between items-center p-4 lg:m-8 lg:my-4 m-4">
      <button id="menuButton" class="lg:hidden px-4 py-2 rounded" @click="showSidebar = !showSidebar"><svg
          class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16m-7 6h7"></path>
        </svg></button>
      <router-link to="/">
        <div class="text-xl font-semibold flex items-center"><img class="w-12 h-12" src="/src/assets/svgs/favicon.svg"
            alt=""><span class="px-2">BMDU</span></div>
      </router-link>
      <theme-toggler :is-mobile="true" :is-dark="isDark" @toggle-theme="toggleTheme"></theme-toggler>
      <div class="hidden lg:flex items-center space-x-4">
        <theme-toggler :is-mobile="false" :is-dark="isDark" @toggle-theme="toggleTheme"></theme-toggler>
        <div class="hidden lg:flex items-center space-x-4">
          <div class="w-10 h-10 rounded-full bg-gray-200 overflow-hidden">
            <img src="https://via.placeholder.com/40" alt="User Avatar" />
          </div>
          <div>
            <p class="m-0 text-gray-900 dark:text-gray-100 font-medium">Azat Jurjenow</p>
            <p class="m-0 text-gray-600 dark:text-gray-300 font-medium">@afych</p>
          </div>
        </div>
      </div>
    </div>
    <!-- Page Content -->
    <div class="flex-1 p-6 text-gray-800 dark:text-gray-100 overflow-y-auto">
      <router-view></router-view>
      <div>
        <p class="text-end text-gray-500 dark:text-gray-400">&copy; {{ year }} "Sanly Çözgüt IT Meýdança" HJ,
          Ähli hukuklar
          goralan</p>
      </div>
    </div>
  </div>

</template>

<script>
import { ref } from "vue";
import ThemeToggler from "@/components/ThemeToggler.vue";
import SidebarLink from "@/components/SidebarLink.vue";
export default {
  name: "Main Layout",
  setup() {
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
      if (theme === "dark") {
        isDark.value = true
      } else {
        isDark.value = false
      }

    }

    return { showSidebar, toggleTheme, isDark, year };
  },
  mounted() {
    const theme = localStorage.getItem("theme")
    if (theme !== null) {
      document.querySelector("html").setAttribute("class", theme)
      this.isDark = theme === "dark" ? true : false

    } else {
      localStorage.setItem("theme", "light")
      document.querySelector("html").setAttribute("class", "light")
      this.isDark = false
    }
  },
  components: { ThemeToggler, SidebarLink }
};
</script>

<style scoped></style>
