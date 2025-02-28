<script setup>
import loginImage from '../assets/svgs/login.svg';
import { onMounted, ref } from "vue";
import ThemeToggler from "@/components/SiteTools.vue";

const isDark = ref(null)


if (!(document.body.classList.contains("empty-layout"))) {
  document.body.classList.add("empty-layout", "font-montserrat", "h-screen", "bg-gray-100", "dark:bg-[#171131ef]");
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
  <router-view></router-view>
</template>

<style scoped></style>
