<script setup>

import { useFacultiesStore } from "@/stores/api.store.js";
import { useRoute } from "vue-router";
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue';
import { storeToRefs } from "pinia";
import TheSpinner from "@/components/TheSpinner.vue";
import { useUxStore } from "@/stores/ux.store";


const emit = defineEmits(['update']);

const route = useRoute()
const facultiesStore = useFacultiesStore()
const uxStore = useUxStore();
const { addToast } = storeToRefs(uxStore);

const isSubmitting = ref(false);
const { highSchoolExcFaculties, createHighSchoolFacultiesStatus } = storeToRefs(facultiesStore);


const searchQuery = ref('');
const selectedIds = ref(new Set());
const isDropdownOpen = ref(false);

const filteredOptions = computed(() => {
  const query = searchQuery.value.toLowerCase();
  return highSchoolExcFaculties.value.filter(option => option.name.toLowerCase().includes(query));
});

const toggleOption = async (option) => {
  if (selectedIds.value.has(option.id)) {
    selectedIds.value.delete(option.id);
  } else {
    selectedIds.value.add(option.id);
  }
  // console.log(selectedOptions.value[0].id);
  searchQuery.value = '';
  await nextTick();
  isDropdownOpen.value = false;
};

const selectedOptions = computed(() => {
  return highSchoolExcFaculties.value.filter(option => selectedIds.value.has(option.id));
});

const handleClickOutside = (event) => {
  if (!event.target.closest('.multi-select')) {
    isDropdownOpen.value = false;
  }
};

onMounted(() => {
  facultiesStore.getHighSchoolExcFaculties(route.params.id)
  document.addEventListener('mousedown', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('mousedown', handleClickOutside);
});

const openDropdown = () => {
  isDropdownOpen.value = true;
};

const onSubmit = () => {
  const data = Array.from(selectedIds.value);
  if (data.length !== 0) {
    console.log(data);
    isSubmitting.value = true;
    facultiesStore.createHighSchoolFaculty({ high_school: parseInt(route.params.id), faculties: data }).then(() => {
      emit("update");
      selectedIds.value.clear();
      isSubmitting.value = false;
    })
  }
}

watch(createHighSchoolFacultiesStatus, (newVal, oldVal) => {
  if (newVal) {
    if (newVal === 'success') {
      addToast('Fakultet üstünlikli hasaba alyndy', 'success');
    } else if (newVal === 'error') {
      addToast('Hasaba alma prosesinde ýalňyşlyk ýüze çykdy', 'error');
    }
  }
  createHighSchoolFacultiesStatus.value = null;
})


</script>
<template>
  <div class="tile mb-6">
    <h3 class="text-xl font-bold mx-2 select-none my-3">Täze fakultet goşmak</h3>
    <div>
      <div class="relative w-full multi-select">
        <div class="flex flex-wrap items-center gap-2 border border-gray-300 rounded-md px-2 py-1 cursor-text"
          @click="openDropdown">
          <template v-for="option in selectedOptions" :key="option.id">
            <div
              class="flex items-center bg-blue-100 dark:bg-violet-600 text-blue-700 dark:text-white rounded-md px-2 py-1 text-sm select-none cursor-default">
              {{ option.name }}
              <button @click.stop.prevent="selectedIds.delete(option.id)"
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
              Maglumat gorunda fakultet tapylmady
            </li>
          </ul>
        </transition>

      </div>
    </div>
    <div class="flex flex-wrap justify-center md:justify-end lg:justify-end mt-3">
      <button :disabled="isSubmitting" @click="onSubmit"
        class="flex w-50 px-4 py-2 my-2 justify-center rounded-lg border-none dark:border-violet-500/50 border-1 bg-gradient-to-r from-blue-400 to-blue-500 dark:from-violet-600 dark:to-violet-500 text-white hover:shadow-lg hover:shadow-blue-300/50 hover:ease-in ease-out duration-200 dark:hover:shadow-violet-500/50 select-none">
        <the-spinner :class="{ hidden: !isSubmitting }"></the-spinner>
        <span :class="{ hidden: isSubmitting }">Hasaba al</span>
      </button>
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
