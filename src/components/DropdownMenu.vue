<script setup>
import {ref} from "vue";

const isOpen = ref(false);

function toggleMenu() {
  isOpen.value = !isOpen.value;
}

function closeMenu() {
  isOpen.value = false;
}

function onClickOutside(event) {
  if (!event.target.closest("#dropdown")) {
    closeMenu();
  }
}

window.addEventListener("click", onClickOutside);
</script>

<template>
  <div id="dropdown" class="relative inline-block text-left">
    <div>
      <button
        @click="toggleMenu"
        type="button"
        class="inline-flex w-full justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-gray-100"
      >
        Меню
        <svg
          class="-mr-1 ml-2 h-5 w-5"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
          aria-hidden="true"
        >
          <path
            fill-rule="evenodd"
            d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
            clip-rule="evenodd"
          />
        </svg>
      </button>
    </div>

    <transition
      name="fade-scale"
      @before-enter="el => (el.style.display = 'block')"
      @after-leave="el => (el.style.display = 'none')"
    >
      <div
        v-show="isOpen"
        class="absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5"
      >
        <div class="py-1">
          <a
            href="#"
            class="text-gray-700 block px-4 py-2 text-sm hover:bg-gray-100"
          >
            Пункт 1
          </a>
          <a
            href="#"
            class="text-gray-700 block px-4 py-2 text-sm hover:bg-gray-100"
          >
            Пункт 2
          </a>
          <a
            href="#"
            class="text-gray-700 block px-4 py-2 text-sm hover:bg-gray-100"
          >
            Пункт 3
          </a>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
/* Tailwind-based transition */
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

.fade-scale-enter-to,
.fade-scale-leave-from {
  opacity: 1;
  transform: scale(1);
}
</style>
