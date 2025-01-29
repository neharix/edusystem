<script setup>
import loginImage from '../assets/svgs/login.svg';
import {onMounted, ref} from "vue";
import ThemeToggler from "@/components/ThemeToggler.vue";

if (!(document.body.classList.contains("empty-layout"))) {
  document.body.classList.add("empty-layout", "font-montserrat", "h-screen", "bg-gray-100", "dark:bg-gray-800");
}

const isDark = ref(null)

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

onMounted(() => {
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

<template>
  <div class="hidden lg:flex w-2/3 bg-gray-200 dark:bg-[#1b1829] justify-center items-center">
    <img :src="loginImage"
         alt="Left Section Image"
         class="max-w-[80%] max-h-[80%] object-contain dark:opacity-75"/>
  </div>
  <!-- Right Section (Login Form) -->
  <div class="flex flex-col justify-center px-8 lg:px-16 bg-white dark:bg-[#171131ef] w-full lg:w-1/3">
    <theme-toggler class="absolute top-5 right-5" :is-dark="isDark" @toggle-theme="toggleTheme"></theme-toggler>
    <router-view></router-view>
  </div>

</template>

<style scoped>

</style>
