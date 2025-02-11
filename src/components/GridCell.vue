<script setup>

import {useRouter} from "vue-router";

const router = useRouter();

const props = defineProps({
  label: String,
  dataValue: {
    type: Number,
    default: 0,
    required: false,
  },
  iconBgClass: String,
  link: {
    type: String,
    required: false,
    default: '',
  },
})

function cellClicked() {
  if (props.link !== '') {
    router.push(props.link);
  }
}

</script>

<template>
  <!-- TODO add router-link like a wrapper for this component -->
  <div class="bg-white dark:bg-[#171131ef] shadow-md rounded-lg flex justify-between items-center p-4" :class="{'cursor-pointer': props.link !== ''}" @click="cellClicked">
    <div>
      <div class="text-sm my-2 select-none">
        {{ label }}
      </div>
      <div class="font-bold mt-2 text-lg select-none">{{ dataValue }}</div>
    </div>
    <div>
      <div :class="iconBgClass" class="w-12 h-12 rounded-full flex justify-center items-center">
        <slot name="default"></slot>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
