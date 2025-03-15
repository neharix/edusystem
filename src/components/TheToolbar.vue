<script setup>
import { ref } from 'vue';

const mouseOnToolbar = ref(false);
const isActive = ref(false)
const timerId = ref(null)

function mouseEnter() {
  if (timerId.value) {
    clearTimeout(timerId.value);
  }
  isActive.value = true;
  mouseOnToolbar.value = true;
}

function mouseLeave() {
  timerId.value = setTimeout(() => { isActive.value = false }, 3000)
  mouseOnToolbar.value = false;
}

</script>
<template>
  <teleport to="body">
    <div class="absolute left-1/2 right-1/2 flex justify-center text-white text-xs bottom-transition"
      :class="{ 'bottom-0': !isActive, 'bottom-4': isActive }">
      <div @mouseenter="mouseEnter" @mouseleave="mouseLeave"
        class="w-max shadow-sm hover:shadow-lg  flex justify-between bg-white dark:bg-[#171131ef] transition-all duration-500 ease-out"
        :class="{
          'rounded-full': isActive,
          'shadow-black/10': isActive && !mouseOnToolbar,
          'shadow-sky-700/30 dark:shadow-violet-600/15': isActive && mouseOnToolbar,
          'shadow-black/10 rounded-t-full': !isActive,
        }">
        <slot name="default" :is-active="isActive"></slot>
      </div>
    </div>
  </teleport>
</template>
<style scoped>
.bottom-transition {
  transition: bottom 300ms ease-in-out;
}
</style>
