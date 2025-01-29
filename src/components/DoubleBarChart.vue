<script setup>
import {defineProps, ref, watch} from "vue";

const props = defineProps({
  admissions: {
    type: Array,
  }
})

const barOptions = {
  colors: ["#1A56DB", "#FDBA8C"],
  chart: {
    type: "bar",
    fontFamily: "Inter, sans-serif",
    toolbar: {
      show: false,
    },
  },
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: "70%",
      borderRadiusApplication: "end",
      borderRadius: 8,
    },
  },
  tooltip: {
    shared: true,
    intersect: false,
    style: {
      fontFamily: "Inter, sans-serif",
    },
  },
  states: {
    hover: {
      filter: {
        type: "darken",
        value: 1,
      },
    },
  },
  stroke: {
    show: true,
    width: 0,
    colors: ["transparent"],
  },
  grid: {
    show: false,
    strokeDashArray: 4,
    padding: {
      left: 2,
      right: 2,
      top: -14
    },
  },
  dataLabels: {
    enabled: false,
  },
  legend: {
    show: true,
  },
  xaxis: {
    floating: false,
    labels: {
      show: true,
      style: {
        fontFamily: "Inter, sans-serif",
        cssClass: 'text-xs font-normal fill-gray-500 dark:fill-gray-400'
      }
    },
    axisBorder: {
      show: false,
    },
    axisTicks: {
      show: false,
    },
  },
  yaxis: {
    show: false,
  },
  fill: {
    opacity: 1,
  },

}

const barSeries = ref([
  {
    name: "Oglanlar",
    color: "#1A56DB",
    data: [],
  },
  {
    name: "Gyzlar",
    color: "#f22254",
    data: [],
  },
])


watch(props, (newVal, oldVal) => {
  let femaleCount = [];
  let maleCount = [];
  for (var obj of newVal.admissions) {
    femaleCount.push({x: obj.year, y: obj.female_students_count});
    maleCount.push({x: obj.year, y: obj.male_students_count});
  }
  barSeries.value[0].data = maleCount;
  barSeries.value[1].data = femaleCount;
})


</script>

<template>
  <div class="w-full bg-white rounded-lg shadow-sm dark:bg-[#171131ef] p-4 md:p-6">
    <h2 class="text-center">Okuwa tabşyryşyklar</h2>

    <div class="flex h-full items-center">
      <div class="block w-full">
        <apexchart id="column-data" :options="barOptions" :series="barSeries" type="bar"></apexchart>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
