<script setup>
import { useUxStore } from '@/stores/ux.store';
import { storeToRefs } from 'pinia';
import { ref, watch } from 'vue';

const uxStore = useUxStore();
const { toasts } = storeToRefs(uxStore);

watch(toasts, (newVal) => {
  console.log(newVal);
})

</script>
<template>
  <teleport to="#toasts">
    <div class="toast min-w-32 max-w-96">
      <div :class="{ 'alert-error': item._type === 'error', 'alert-success': item._type === 'success' }"
        class="alert flex items-start justify-between border-0 w-full text-white" v-for="item in toasts" :key="item.id">
        <span>{{ item.message }}</span>
        <button class="w-max" @click="uxStore.deleteToast(item.id)">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6" viewBox="0 0 24 24">
            <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M18 6L6 18M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  </teleport>
</template>
<style scoped>
.alert {
  animation: fadeIn 0.3s ease-out, fadeOut 0.3s ease-in 4.7s forwards;
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
