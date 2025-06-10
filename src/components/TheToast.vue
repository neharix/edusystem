<script setup>
import { onMounted, onUnmounted, ref } from "vue";

const props = defineProps({
  message: String,
  type: {
    type: String,
    default: "info",
  },
  duration: {
    type: Number,
    default: 3000,
  },
  onClose: Function,
});

const visible = ref(true);
let timer;

onMounted(() => {
  timer = setTimeout(() => closeToast(), props.duration);
});

onUnmounted(() => clearTimeout(timer));

const closeToast = () => {
  visible.value = false;
  setTimeout(() => props.onClose(), 300);
};

const toastStyles = {
  success: "border-l-8 border-green-500",
  error: "border-l-8 border-red-500",
  warning: "border-l-8 border-yellow-500",
  info: "border-l-8 border-blue-500",
};

const toastHeaders = {
  success: "Üstünlik",
  error: "Ýalňyşlyk",
  warning: "Duýduryş",
  info: "Bildiriş"
}

</script>

<template>

  <div v-if="visible"
    :class="`toast my-2 p-4 bg-white dark:bg-[#171131] w-full dark:text-white rounded-lg shadow-lg transition-all ${toastStyles[type]}`">
    <h3 class="hidden md:block mb-3 text-base font-semibold select-none">{{ toastHeaders[type] }}</h3>
    <button class="absolute top-3 right-5 font-bold dark:text-white select-none" @click.stop="closeToast">✖</button>
    <div class="flex justify-between text-sm items-center mt-4 md:mt-0">
      <div class="select-none">{{ message }}</div>
    </div>
  </div>
</template>

<style scoped>
.toast {
  animation: fadeIn 0.3s ease-out, fadeOut 0.3s ease-in 2.7s forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeOut {
  from {
    opacity: 1;
    transform: translateY(0);
  }

  to {
    opacity: 0;
    transform: translateY(-20px);
  }
}
</style>
