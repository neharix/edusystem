<template>
  <aside id="sidebar" :class="{ '-translate-x-full': !showSidebar }"
    class="fixed md:static inset-y-0 left-0 md:w-1/6 w-64 bg-white shadow-lg h-screen transform md:translate-x-0 transition-transform duration-300 ease-in-out overflow-y-auto z-20">
    <!-- User Info Block -->
    <div class="flex md:hidden items-center space-x-4 bg-blue-50 px-4 py-6">
      <img class="w-12 h-12 rounded-full border-2 border-blue-400" src="https://via.placeholder.com/150"
        alt="User Avatar">
      <div>
        <p class="text-lg font-semibold text-gray-800">afych afych</p>
        <p class="text-sm text-gray-500">@afych</p>
      </div>
    </div>
    <!-- Menu -->
    <div class="px-4 py-6">
      <nav class="mt-4 space-y-2">
        <!-- TODO make some components for sidebar links -->
        <router-link to="/">
          <button
            class="px-3 py-2 flex items-center rounded-md text-white bg-blue-400 hover:bg-blue-300 transition-all duration-200 ease-out hover:transition-all hover:duration-200 hover:ease-in">
            <img class="px-3" src="../assets/svgs/home_active.svg">
            <span>Baş sahypa</span>
          </button>
        </router-link>
        <p class="text-gray-500 px-3 py-2 block-header">DOLANDYRYŞ</p>
        <router-link to="/high-schools"
          class="px-3 py-2 flex items-center rounded-md text-gray-700 hover:bg-blue-100 transition-all duration-200 ease-in hover:transition-all hover:duration-200 hover:ease-in">
          <img class="px-3" src="../assets/svgs/educenter.svg">
          <span>ÝOM</span>
        </router-link>
      </nav>
    </div>
  </aside>
  <!-- Overlay -->
  <div @click="showSidebar = !showSidebar" :class="{ 'hidden': !showSidebar }" class="fixed inset-0 bg-black/50  z-10">
  </div>
  <!-- Main Content -->
  <main class="flex-1 p-6 overflow-y-auto">
    <nav class="bg-white shadow-md rounded-md fixed md:w-9/12 w-10/12">
      <div class="container mx-auto flex justify-between items-center px-4 py-3">
        <!-- Toggle button for sidebar -->
        <button @click="showSidebar = !showSidebar" class="text-gray-700 md:hidden focus:outline-none">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16m-7 6h7"></path>
          </svg>
        </button>
        <a href="/" class="text-2xl font-bold text-blue-500">BMDU</a>
        <div class="hidden md:flex space-x-4">
          <div class="flex items-center space-x-4">
            <img class="w-10 h-10 rounded-full border-2 border-blue-400" src="https://via.placeholder.com/150"
              alt="User Avatar">
            <div>
              <p class="text-sm font-semibold text-gray-800">afych afych
              </p>
              <p class="text-sm text-gray-500">@hello</p>
            </div>
          </div>
        </div>
      </div>
    </nav>
    <router-view></router-view>
  </main>
</template>

<script>
import { ref } from "vue";
export default {
  name: "Main Layout",
  setup() {
    const showSidebar = ref(false);
    return { showSidebar };
  },
};
</script>

<style scoped></style>
