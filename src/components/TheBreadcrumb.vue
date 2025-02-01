<script setup>
import {useRouter} from "vue-router";

const router = useRouter();

const props = defineProps({
  paths: Array,
})
</script>

<template>
  <div
    class="px-3 py-4 w-full rounded-xl shadow-md dark:shadow-lg flex justify-between mb-8 bg-white dark:bg-[#171131ef]">
    <div class="flex items-center overflow-x-auto">
      <div v-for="(item, index) in paths" :key="index">
      <div class="flex items-center" v-if="router.currentRoute.value.path === item.path">
        <p class="py-2 select-none text-nowrap px-3 my-2 text-[0.7rem] md:text-sm lg:text-sm rounded-lg shadow-md border-none dark:border-violet-500/50 border-1 bg-blue-500 dark:bg-violet-600 text-white">{{ item.name }}</p>
        <p class="mx-2 text-sm" v-if="index !== paths.length - 1">/</p>
      </div>
      <div v-else class="flex items-center">
        <router-link :to="item.path"
                     class="text-nowrap text-[0.7rem] md:text-sm lg:text-sm px-3 my-2 py-2 hover:text-blue-500 dark:hover:text-violet-600 transition ease-in hover:ease-out duration-200">{{
            item.name
          }}</router-link>
        <p class="mx-2 text-sm" v-if="index !== paths.length - 1">/</p>
      </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
