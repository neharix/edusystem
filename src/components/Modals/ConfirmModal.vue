<template>
  <teleport to="body">
    <transition name="fade">
      <div
        v-if="isOpen"
        class="absolute z-30 inset-0 flex items-center justify-center bg-black bg-opacity-50"
        @click.self="close"
      >
        <transition name="modal">
          <div
            v-if="isOpen"
            class="bg-white dark:bg-[#171131] p-6 rounded-2xl shadow-xl w-96"
          >
            <h2 class="dark:text-white text-xl font-bold">{{ header }}</h2>
            <p class="dark:text-white mt-2">{{ context }}</p>
            <div class="flex justify-end space-x-2">
              <button @click="close" class="px-4 py-2 text-[0.8rem] font-medium bg-blue-400 hover:bg-blue-500 transition ease-in hover:ease-out duration-200 text-white dark:bg-blue-700 dark:hover:bg-blue-800 border border-gray-200 rounded-lg focus:z-10 focus:ring-2 focus:ring-blue-500 dark:border-gray-700  dark:focus:ring-blue-700">
                Ýok
              </button>
              <button @click="close" class="px-4 py-2 text-[0.8rem] font-medium bg-red-400 hover:bg-red-500 transition ease-in hover:ease-out duration-200 text-white dark:bg-pink-900 dark:hover:bg-pink-600 border border-gray-200 rounded-lg focus:z-10 focus:ring-2 focus:ring-red-500 dark:border-gray-700  dark:focus:ring-pink-500">
                Hawa
              </button>
            </div>
          </div>
        </transition>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  isOpen: Boolean,
  header: String,
  context: String,
});
const emit = defineEmits(['close']);

const close = () => {
  emit('close');
};
</script>

<style>

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.modal-enter-active, .modal-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}
.modal-enter-from, .modal-leave-to {
  opacity: 0;
  transform: scale(0.9);
}
</style>
