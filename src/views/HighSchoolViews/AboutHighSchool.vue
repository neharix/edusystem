<script setup>

import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import {useRoute} from "vue-router";
import {useHighSchoolsStore} from "@/stores/api.store.js";
import {storeToRefs} from "pinia";

const route = useRoute();

const highSchoolsStore = useHighSchoolsStore();
highSchoolsStore.get(route.params.id);

const { highSchool } = storeToRefs(highSchoolsStore);


const breadcrumbPaths = [
  {path: "/high-schools", name: "Ýokary okuw mekdepleri"},
  {name: "Görmek", current: true},
]

</script>

<template>
  <the-breadcrumb :paths="breadcrumbPaths"></the-breadcrumb>
  <div class="my-2 select-none" :class="{'opacity-0' : !highSchool.name }">
    {{ highSchool.name ? highSchool.name : "h" }}
  </div>
  <div class="flex md:flex-row flex-col mb-4 md:space-x-2 space-x-0">
    <router-link :to="`/high-schools/view/${route.params.id}`" v-slot="{ isExactActive }">
      <p class="text-[0.8rem] px-4 py-2 my-2 rounded-lg text-center select-none" :class="{'link-active': isExactActive,
         'link-inactive-primary': !isExactActive }">
        ÝOM barada</p>
    </router-link>
    <router-link :to="`/high-schools/view/${route.params.id}/faculties`" v-slot="{ isExactActive }">
      <p class="text-[0.8rem] px-4 py-2 my-2 rounded-lg text-center select-none" :class="{'link-active': isExactActive,
         'link-inactive-primary': !isExactActive }">
        Fakultetler</p>
    </router-link>
    <router-link :to="`/high-schools/view/${route.params.id}/departments`" v-slot="{ isExactActive }">
      <p class="text-[0.8rem] px-4 py-2 my-2 rounded-lg text-center select-none" :class="{'link-active': isExactActive,
         'link-inactive-primary': !isExactActive }">
        Kafedralar</p>
    </router-link>
    <router-link :to="`/high-schools/view/${route.params.id}/specializations`" v-slot="{ isExactActive }">
      <p class="text-[0.8rem] px-4 py-2 my-2 rounded-lg text-center select-none" :class="{'link-active': isExactActive,
         'link-inactive-primary': !isExactActive }">
        Hünarler</p>
    </router-link>
  </div>
  <router-view></router-view>
</template>

<style scoped>
</style>
