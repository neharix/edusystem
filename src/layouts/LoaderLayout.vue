<script setup>

import {onBeforeUnmount, onMounted, onUnmounted, ref} from "vue";
import TheSpinner from "@/components/TheSpinner.vue";

const isDark = ref(null)


if (!(document.body.classList.contains("loader-layout"))) {
  document.body.classList.add("loader-layout", "font-montserrat", "h-screen", "bg-gray-100", "dark:bg-[#171131ef]");
}

onUnmounted(() => {
  document.body.className = "bg-gray-100 dark:bg-[#171131ef]";
})


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
  <div class="w-full h-full flex items-center justify-center text-blue-500 dark:text-violet-500">
    <the-spinner size-class="w-48"></the-spinner>
  </div>
</template>

<style scoped>

</style>
