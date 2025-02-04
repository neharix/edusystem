<template>
  <div class="grid md:grid-cols-4 sm:grid-cols-2 gap-8">
    <grid-cell label="Talyp sany" :data-value="highSchoolAbout.students_count"
               icon-bg-class="bg-sky-200 dark:bg-sky-500/75">
      <svg class="w-6 h-8 stroke-sky-500 dark:stroke-sky-900"
           xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none"
           stroke="currentColor"
           stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
        <circle cx="9" cy="7" r="4"></circle>
        <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
        <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
      </svg>
    </grid-cell>
    <grid-cell label="Oglanlar" :data-value="highSchoolAbout.male_students_count"
               icon-bg-class="bg-sky-200 dark:bg-sky-500/75">
      <svg class="w-6 h-8 stroke-sky-500 dark:stroke-sky-900"
           xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none"
           stroke="currentColor"
           stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
        <circle cx="9" cy="7" r="4"></circle>
        <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
        <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
      </svg>
    </grid-cell>
    <grid-cell label="Gyzlar" :data-value="highSchoolAbout.female_students_count"
               icon-bg-class="bg-sky-200 dark:bg-sky-500/75">
      <svg class="w-6 h-8 stroke-sky-500 dark:stroke-sky-900"
           xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none"
           stroke="currentColor"
           stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
        <circle cx="9" cy="7" r="4"></circle>
        <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
        <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
      </svg>
    </grid-cell>
    <grid-cell label="Ätiýaçdaky diplom sany" :data-value="0"
               icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-8 stroke-green-500 dark:stroke-green-900" viewBox="0 0 24 24" fill="none"
           stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"></polygon>
        <line x1="8" y1="2" x2="8" y2="18"></line>
        <line x1="16" y1="6" x2="16" y2="22"></line>
      </svg>
    </grid-cell>
  </div>
  <div class="mt-8 grid lg:grid-cols-2 md:grid-cols-2 sm:grid-cols-1 gap-8">

    <double-bar-chart :admissions="highSchoolAbout.admissions"></double-bar-chart>
    <radial-bar-chart :studentsCount="highSchoolAbout.students_count"
                      :femaleCount="highSchoolAbout.female_students_count"
                      :maleCount="highSchoolAbout.male_students_count"></radial-bar-chart>
  </div>
  <h2 class="my-8 select-none">Welaýatlar boýunça talyp sany</h2>
  <div class="grid md:grid-cols-4 sm:grid-cols-2 gap-8">
    <grid-cell v-for="(item, index) in highSchoolAbout.students_count_by_regions" :key="index" :label="item.region" :data-value="item.students_count"
               icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-8 stroke-green-500 dark:stroke-green-900" viewBox="0 0 24 24" fill="none"
           stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"></polygon>
        <line x1="8" y1="2" x2="8" y2="18"></line>
        <line x1="16" y1="6" x2="16" y2="22"></line>
      </svg>
    </grid-cell>
  </div>
</template>

<script setup>
import RadialBarChart from "@/components/Charts/RadialBarChart.vue";
import DoubleBarChart from "@/components/Charts/DoubleBarChart.vue";
import GridCell from "@/components/GridCell.vue";
import {useHighSchoolsStore} from "@/stores/api.store.js";
import {useRoute} from "vue-router";
import {storeToRefs} from "pinia";

const route = useRoute();
const highSchoolsStore = useHighSchoolsStore();
highSchoolsStore.getAbout(route.params.id);

const {highSchoolAbout} = storeToRefs(highSchoolsStore);

</script>

<!---->
