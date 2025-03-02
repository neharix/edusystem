<script setup>
import { useRoute } from "vue-router";
import { computed, nextTick, onMounted, onUnmounted, ref } from 'vue';

const props = defineProps({
  data: Array,
  emptyLabel: String
})

const emit = defineEmits(['update'])

const searchQuery = ref('');
const selectedIds = ref(new Set());
const isDropdownOpen = ref(false);

const filteredOptions = computed(() => {
  const query = searchQuery.value.toLowerCase();
  return props.data.filter(option => option.name.toLowerCase().includes(query));
});

const toggleOption = async (option) => {
  if (selectedIds.value.has(option.id)) {
    selectedIds.value.delete(option.id);
  } else {
    selectedIds.value.add(option.id);
  }
  emit('update', Array.from(selectedIds.value))
  searchQuery.value = '';
  await nextTick();
  isDropdownOpen.value = false;
};

const selectedOptions = computed(() => {
  return props.data.filter(option => selectedIds.value.has(option.id));
});

const handleClickOutside = (event) => {
  if (!event.target.closest('.multi-select')) {
    isDropdownOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener('mousedown', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('mousedown', handleClickOutside);
});

const openDropdown = () => {
  isDropdownOpen.value = true;
};

function removeItem(id) {
  selectedIds.value.delete(id);
  emit('update', Array.from(selectedIds.value))
}

</script>

<template>
  <div>
    <div class="relative w-full multi-select">
      <div class="flex flex-wrap items-center gap-2 border border-gray-300 rounded-md px-2 py-1 cursor-text"
        @click="openDropdown">
        <template v-for="option in selectedOptions" :key="option.id">
          <div
            class="flex items-center bg-blue-100 dark:bg-violet-600 text-blue-700 dark:text-white rounded-md px-2 py-1 text-sm select-none cursor-default">
            {{ option.name }}
            <button @click.stop.prevent="removeItem(option.id)"
              class="ml-1 text-blue-700 dark:text-white focus:outline-none select-none">
              ✕
            </button>
          </div>
        </template>
        <input v-model="searchQuery" type="text" placeholder="" class="flex-1 py-1 focus:outline-none" />
      </div>
      <transition name="dropdown">
        <ul v-if="isDropdownOpen"
          class="absolute z-10 w-full bg-white dark:bg-[#171131] border border-gray-300 dark:border-gray-800 rounded-md shadow-md max-h-48 overflow-y-auto ">
          <li v-for="option in filteredOptions" :key="option.id" @mousedown.prevent="toggleOption(option)" :class="{
            'px-3 py-2 cursor-pointer select-none transition ease-in duration-200': true,
            'bg-blue-100 text-blue-700 dark:bg-violet-600/25 dark:text-white': selectedIds.has(option.id),
            'hover:bg-blue-50 dark:hover:bg-[#261c52]': !selectedIds.has(option.id),
          }">
            {{ option.name }}
          </li>
          <li v-if="filteredOptions.length === 0" class="px-3 py-2 text-gray-500 select-none">
            {{ emptyLabel }}
          </li>
        </ul>
      </transition>

    </div>
  </div>
</template>

<style scoped>
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.dropdown-enter-to {
  opacity: 1;
  transform: translateY(0);
}

.dropdown-leave-from {
  opacity: 1;
  transform: translateY(0);
}

.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
