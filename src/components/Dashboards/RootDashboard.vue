<script setup>

import RadialBarChart from "@/components/Charts/RadialBarChart.vue";
import DoubleBarChart from "@/components/Charts/DoubleBarChart.vue";
import GridCell from "@/components/GridCell.vue";
import useDashboard from "@/use/useDashboard.js";


const { data } = useDashboard();
</script>

<template>
  <!--  <div>-->
  <!--    <the-leaflet-map></the-leaflet-map>-->
  <!--  </div>-->

  <div class="grid md:grid-cols-4 sm:grid-cols-2 gap-8">
    <grid-cell link="/high-schools" label="Ýokary okuw mekdepler" :data-value="data.high_schools_count"
      icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_901_948)">
          <path
            d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        <defs>
          <clipPath id="clip0_901_948">
            <rect width="32" height="32" fill="white" />
          </clipPath>
        </defs>
      </svg>
    </grid-cell>
    <grid-cell link="/faculties" label="Fakultetler" :data-value="data.faculties_count"
      icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 h-8 stroke-green-500 dark:stroke-green-900" xmlns="http://www.w3.org/2000/svg" fill="none"
        viewBox="0 0 24 24" strokeWidth="4" stroke="currentColor">
        <path strokeLinecap="round" strokeLineJoin="round"
          d="M16.5 3.75V16.5L12 14.25 7.5 16.5V3.75m9 0H18A2.25 2.25 0 0 1 20.25 6v12A2.25 2.25 0 0 1 18 20.25H6A2.25 2.25 0 0 1 3.75 18V6A2.25 2.25 0 0 1 6 3.75h1.5m9 0h-9" />
      </svg>
    </grid-cell>
    <grid-cell link="/departments" label="Kafedralar" :data-value="data.departments_count"
      icon-bg-class="bg-yellow-200 dark:bg-yellow-500/75">
      <svg class="w-6 h-8 stroke-yellow-500 dark:stroke-yellow-900" xmlns="http://www.w3.org/2000/svg" fill="none"
        viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="size-6">
        <path strokeLinecap="round" strokeLineJoin="round"
          d="M20.25 6.375c0 2.278-3.694 4.125-8.25 4.125S3.75 8.653 3.75 6.375m16.5 0c0-2.278-3.694-4.125-8.25-4.125S3.75 4.097 3.75 6.375m16.5 0v11.25c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125V6.375m16.5 0v3.75m-16.5-3.75v3.75m16.5 0v3.75C20.25 16.153 16.556 18 12 18s-8.25-1.847-8.25-4.125v-3.75m16.5 0c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125" />
      </svg>
    </grid-cell>
    <grid-cell link="/specializations" label="Hünärler" :data-value="data.specializations_count"
      icon-bg-class="bg-yellow-200 dark:bg-yellow-500/75">
      <svg class="w-6 h-8 stroke-yellow-500 dark:stroke-yellow-900" xmlns="http://www.w3.org/2000/svg" fill="none"
        viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="size-6">
        <path strokeLinecap="round" strokeLineJoin="round"
          d="M3.75 3v11.25A2.25 2.25 0 0 0 6 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0 1 18 16.5h-2.25m-7.5 0h7.5m-7.5 0-1 3m8.5-3 1 3m0 0 .5 1.5m-.5-1.5h-9.5m0 0-.5 1.5m.75-9 3-3 2.148 2.148A12.061 12.061 0 0 1 16.5 7.605" />
      </svg>
    </grid-cell>
    <grid-cell link="/nationalizations" label="Milletler" :data-value="data.nationalities_count"
      icon-bg-class="bg-red-200 dark:bg-red-500/75">
      <svg class="w-6 h-8 stroke-red-500 dark:stroke-red-900" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
        <circle cx="12" cy="10" r="3"></circle>
      </svg>
    </grid-cell>
    <grid-cell link="/students" label="Talyplar" :data-value="data.students_count"
      icon-bg-class="bg-sky-200 dark:bg-sky-500/75">
      <svg class="w-6 h-8 stroke-sky-500 dark:stroke-sky-900" xmlns="http://www.w3.org/2000/svg" width="14" height="14"
        viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
        stroke-linejoin="round">
        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
        <circle cx="9" cy="7" r="4"></circle>
        <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
        <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
      </svg>
    </grid-cell>
    <grid-cell label="Gyzlar" :data-value="data.female_students_count" icon-bg-class="bg-sky-200 dark:bg-sky-500/75">
      <svg class="w-6 h-8 stroke-sky-500 dark:stroke-sky-900" xmlns="http://www.w3.org/2000/svg" width="14" height="14"
        viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
        stroke-linejoin="round">
        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
        <circle cx="9" cy="7" r="4"></circle>
        <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
        <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
      </svg>
    </grid-cell>
    <grid-cell label="Oglanlar" :data-value="data.male_students_count" icon-bg-class="bg-sky-200 dark:bg-sky-500/75">
      <svg class="w-6 h-8 stroke-sky-500 dark:stroke-sky-900" xmlns="http://www.w3.org/2000/svg" width="14" height="14"
        viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
        stroke-linejoin="round">
        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
        <circle cx="9" cy="7" r="4"></circle>
        <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
        <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
      </svg>
    </grid-cell>
  </div>
  <div class="mt-8 grid lg:grid-cols-3 md:grid-cols-2 sm:grid-cols-1 gap-8">

    <double-bar-chart :admissions="data.admissions"></double-bar-chart>
    <radial-bar-chart :studentsCount="data.students_count" :femaleCount="data.female_students_count"
      :maleCount="data.male_students_count"></radial-bar-chart>
    <div class="space-y-6">
      <h2 class="my-8 text-2xl select-none">Okuwy tamamlaýanlar</h2>
      <grid-cell label="Gyzlar" :data-value="data.female_graduates" icon-bg-class="bg-sky-200 dark:bg-sky-500/75">
        <svg class="w-6 h-8 stroke-sky-500 dark:stroke-sky-900" xmlns="http://www.w3.org/2000/svg" width="14"
          height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
          stroke-linejoin="round">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
          <circle cx="9" cy="7" r="4"></circle>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
          <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
        </svg>
      </grid-cell>
      <grid-cell label="Oglanlar" :data-value="data.male_graduates" icon-bg-class="bg-sky-200 dark:bg-sky-500/75">
        <svg class="w-6 h-8 stroke-sky-500 dark:stroke-sky-900" xmlns="http://www.w3.org/2000/svg" width="14"
          height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
          stroke-linejoin="round">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
          <circle cx="9" cy="7" r="4"></circle>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
          <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
        </svg>
      </grid-cell>
    </div>

  </div>

</template>

<style scoped></style>
