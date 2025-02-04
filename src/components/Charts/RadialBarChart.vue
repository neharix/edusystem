<script setup>
import {defineProps, onMounted, ref, watch} from "vue";

const props = defineProps({
  studentsCount: Number,
  maleCount: Number,
  femaleCount: Number,
})

const radialOptions = {
  colors: ["#37a75a", "#ce2750"],
  chart: {
    height: "350px",
    width: "100%",
    type: "radialBar",
    sparkline: {
      enabled: true,
    },
  },
  plotOptions: {
    radialBar: {
      track: {
        background: '#E5E7EB',
      },
      dataLabels: {
        show: false,
      },
      hollow: {
        margin: 0,
        size: "32%",
      }
    },
  },
  grid: {
    show: false,
    strokeDashArray: 4,
    padding: {
      left: 2,
      right: 2,
      top: -23,
      bottom: -20,
    },
  },
  labels: ["Oglanlar", "Gyzlar"],
  legend: {
    show: true,
    position: "bottom",
    fontFamily: "Inter, sans-serif",
  },
  tooltip: {
    enabled: true,
    x: {
      show: false,
    },
  },
  yaxis: {
    show: false,
    labels: {
      formatter: function (value) {
        return value + '%';
      }
    }
  }
}

const radialSeries = ref([0, 0]);


watch(props, (newVal, oldVal) => {
  radialSeries.value[0] = props.maleCount / props.studentsCount * 100;
  radialSeries.value[1] = props.femaleCount / props.studentsCount * 100;

})

onMounted(() => {
  if (props.studentsCount && props.femaleCount && props.maleCount) {
    radialSeries.value[0] = props.maleCount / props.studentsCount * 100;
    radialSeries.value[1] = props.femaleCount / props.studentsCount * 100;
  }
})


</script>

<template>
  <div class="w-full bg-white rounded-lg shadow-sm dark:bg-[#171131ef] p-4 md:p-6">
    <h2 class="text-center select-none">Umumy gyz/oglan koefissenti</h2>

    <apexchart id="column-data" :options="radialOptions" :series="radialSeries" type="radialBar"></apexchart>

  </div>


</template>

<style scoped>

</style>
