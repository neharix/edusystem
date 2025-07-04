<script setup>
import { computed, defineProps, onMounted, ref, watch } from 'vue';
import { useSpecializationsStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import router from "@/router/index.js";
import { useAuthStore } from "@/stores/auth.store.js";
import { useRoute } from 'vue-router';
import { useUxStore } from '@/stores/ux.store';
import CreateSpecializationShell from '../Forms/CreateSpecializationShell.vue';


const props = defineProps({
  data: Array,
  totalPages: Number,
  sortedBy: {
    type: String,
    required: false,
    default: "name"
  }
})
const emit = defineEmits(["update"]);

watch(props, (newVal, oldVal) => {
  data.value = newVal.data;
  filteredData.value = [...data.value];
})

const route = useRoute();

const authStore = useAuthStore();
const specializationsStore = useSpecializationsStore();
const { deleteStatus, updateStatus, createStatus } = storeToRefs(specializationsStore);
const uxStore = useUxStore();

const data = ref([]);
const filteredData = ref([]);
const selectedItem = ref(null);

if (props.data.length > 0) {
  data.value = props.data;
  filteredData.value = [...data.value];
}

const activeBtnClasses = ref("p-4 py-2 my-2 rounded-full border-none dark:border-violet-500/50 border-1 bg-blue-500 dark:bg-violet-600 text-white");
const defaultBtnClasses = ref("p-4 py-2 my-2 rounded-full border-none bg-gray-200 dark:bg-[#261953]");
const sortColumn = ref(route.query.column || "name");
const sortOrder = ref(route.query.order || 'asc');
const currentPage = ref(Number(route.query.page || 1));
const rowsPerPage = ref(localStorage.getItem("rowsPerPage") || 10);
const rowsPerPageOptions = [10, 20, 50, 100, 250, 500];
const searchQuery = ref('');
const isSearching = ref(!!route.query.search || false);
const customPage = ref(currentPage.value);
const selectedItems = ref([]);


const selectedItemsCount = computed(() => {
  return selectedItems.value.length
})

const isAllSelected = computed(() => {
  if (data.value.length === selectedItems.value.length) {
    return true;
  }
  return false;
})

const selectAll = () => {
  if (isAllSelected.value) {
    selectedItems.value = [];
  } else {
    selectedItems.value = data.value.map(item => item.id)
  }
}

const checkboxClicked = (id) => {
  if (selectedItems.value.includes(id)) {
    selectedItems.value = selectedItems.value.filter(item => item !== id);
  } else {
    selectedItems.value.push(id);
  }
}


const applySearch = () => {
  router.push({ name: 'specializations-list', query: { ...route.query, search: searchQuery.value } }).then(() => {
    emit('update')
  });
};

const resetTable = () => {
  const newQuery = { ...route.query };
  delete newQuery.search;

  router.replace({ query: newQuery }).then(() => {
    emit('update');
    isSearching.value = false;
  });
};

const changePage = (page) => {
  if (page >= 1 && page <= props.totalPages) {
    currentPage.value = page;
  }
};

const changeRowsPerPage = async (option) => {
  rowsPerPage.value = parseInt(option, 10);
  localStorage.setItem("rowsPerPage", rowsPerPage.value)
  if (currentPage.value === 1) {
    emit('update')
  } else {
    currentPage.value = 1;
  }
  isOpen.value = false;
};

const pagesBefore = computed(() => {
  const start = Math.max(2, currentPage.value - 2);
  return Array.from({ length: Math.max(0, currentPage.value - start) }, (_, i) => start + i);
});

const pagesAfter = computed(() => {
  const end = Math.min(props.totalPages - 1, currentPage.value + 2);
  return Array.from({ length: Math.max(0, end - currentPage.value) }, (_, i) => currentPage.value + i + 1);
});


const sort = (column) => {
  if (sortColumn.value === column) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortColumn.value = column;
    sortOrder.value = 'asc';
  }
};

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


watch(currentPage, (newVal) => {
  router.push({ name: 'specializations-list', query: { ...route.query, page: newVal } }).then(() => {
    emit('update')
  });
})
watch(sortColumn, (newVal) => {
  setTimeout(() => {
    router.push({ name: 'specializations-list', query: { ...route.query, order: sortOrder.value, column: newVal } }).then(() => {
      emit('update');
    })
  }, 50)
})

watch(sortOrder, (newVal) => {
  router.push({ name: 'specializations-list', query: { ...route.query, order: newVal, column: sortColumn.value } }).then(() => {
    emit('update');
  })
})

watch(deleteStatus, (newVal, oldVal) => {
  if (newVal) {
    if (newVal === 'success') {
      uxStore.addToast('Hünar üstünlikli ýok edildi', 'success');
    } else if (newVal === 'error') {
      uxStore.addToast('Ýok etme prosesinde ýalňyşlyk ýüze çykdy', 'error');
    }
  }
  deleteStatus.value = null;
})

onMounted(() => {
  if (updateStatus.value) {
    if (updateStatus.value === 'success') {
      uxStore.addToast('Hünär üstünlikli üýtgedildi', 'success');
    } else if (updateStatus.value === 'error') {
      uxStore.addToast('Üýtgetme prosesinde ýalňyşlyk ýüze çykdy', 'error');
    }
  }
  updateStatus.value = null;

  if (createStatus.value) {
    if (createStatus.value === 'success') {
      uxStore.addToast('Hünär üstünlikli hasaba alyndy', 'success');
    } else if (createStatus.value === 'error') {
      uxStore.addToast('Hasaba alma prosesinde ýalňyşlyk ýüze çykdy', 'error');
    }
  }
  createStatus.value = null;
  if (currentPage.value != specializationsStore.currentPage) {
    changePage(specializationsStore.currentPage);
  }
})

window.addEventListener("click", onClickOutside);

const isShellModalOpen = ref(false);

function openShellModal() {
  isShellModalOpen.value = true;
}
function closeShellModal() {
  isShellModalOpen.value = false;
}
function submitShellModal() {
  isShellModalOpen.value = false;
  selectedItems.value = [];
}

</script>

<template>
  <create-specialization-shell v-if="authStore.user.is_complex_branched" :is-open="isShellModalOpen"
    :specializations="selectedItems" @close="closeShellModal()"
    @submit="submitShellModal()"></create-specialization-shell>
  <div class="w-full rounded-lg shadow-lg">
    <div class="pt-1  rounded-t-lg dark:bg-[#171131ef] bg-white">
      <div class="flex items-center justify-between space-x-2 py-3 px-4">
        <div class="flex items-center">
          <div id="dropdown" class="relative inline-block text-left">
            <div>
              <button @click="toggleMenu" type="button"
                class="inline-flex transition duration-200 ease-in w-full justify-center rounded-md border border-gray-300 dark:border-gray-800 bg-white dark:bg-[#171131ef] dark:text-gray-200 px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 dark:hover:bg-[#32237cef] focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-[#32237cef] focus:ring-offset-2 focus:ring-offset-gray-100 dark:focus:ring-offset-[#32237cef] select-none">
                Setir sany: {{ rowsPerPage }}
              </button>
            </div>

            <transition name="fade-scale" @before-enter="el => (el.style.display = 'block')"
              @after-leave="el => (el.style.display = 'none')">
              <div v-show="isOpen"
                class="absolute left-0 z-10 mt-2 w-24 origin-top-left rounded-md bg-white dark:bg-[#171131ef] shadow-lg ring-1 ring-white dark:ring-gray-800 ring-opacity-5">
                <div class="py-1">
                  <button v-for="option in rowsPerPageOptions" :key="option" :value="option"
                    @click="changeRowsPerPage(option)"
                    class="w-full text-start text-gray-700 dark:text-gray-200 block px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-[#32237cef] select-none">
                    {{ option }} setir
                  </button>

                </div>
              </div>
            </transition>
          </div>
        </div>
        <div v-if="authStore.user.is_complex_branched">
          <div class="dropdown dropdown-end">
            <div tabindex="0" role="button" class="btn-primary w-full">
              <svg class="w-5 h-5 md:w-6 md:h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16m-7 6h7"></path>
              </svg>
            </div>
            <ul tabindex="0"
              class="dropdown-content menu border border-white/10 bg-mbg dark:bg-[#171131ef] bg-white rounded-box z-1 w-48 lg:w-64 p-2 shadow-sm">
              <li class="px-4 py-2 select-none">
                Umumy {{ specializationsStore.objectsCount }} element
              </li>
              <li class="px-4 py-2 select-none" v-if="selectedItemsCount > 0">
                {{ selectedItemsCount }} element saýlanan
              </li>
              <hr class="hr">
              <li>
                <button @click="openShellModal()"
                  class="w-full text-start text-gray-700 dark:text-gray-200 block px-4 py-2 text-[0.8rem] md:text-sm hover:bg-gray-100 dark:hover:bg-[#261953] select-none">
                  Saýlanan hünärleri birikdirmek
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div class="mx-4 pb-4 flex">
        <input v-model="searchQuery" type="text" @keyup.enter="applySearch" placeholder="Gözleg"
          :class="{ 'rounded-l-md': isSearching, 'rounded-md': !isSearching }"
          class="w-full text-[0.8rem] md:text-sm dark:text-gray-300 transition duration-200 ease-in bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 focus:ring focus:ring-blue-300 dark:focus:ring-violet-800 focus:outline-none" />
        <button @click="resetTable" v-if="isSearching"
          class="py-2 select-none text-nowrap px-3 text-[0.7rem] md:text-sm rounded-r-md shadow-md dark:border-violet-500/50 bg-blue-500 dark:bg-violet-600 text-white ring-0 ring-blue-400 dark:ring-violet-800 active:ring-4 duration-100 ease-in active:scale-95">
          <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="w-6 h-6"
            viewBox="0 0 24 24" version="1.1">
            <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
              <g id="Reload">
                <rect id="Rectangle" fill-rule="nonzero" x="0" y="0" width="24" height="24">
                </rect>
                <path
                  d="M4,13 C4,17.4183 7.58172,21 12,21 C16.4183,21 20,17.4183 20,13 C20,8.58172 16.4183,5 12,5 C10.4407,5 8.98566,5.44609 7.75543,6.21762"
                  id="Path" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                </path>
                <path
                  d="M9.2384,1.89795 L7.49856,5.83917 C7.27552,6.34441 7.50429,6.9348 8.00954,7.15784 L11.9508,8.89768"
                  id="Path" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                </path>
              </g>
            </g>
          </svg>
        </button>
      </div>
    </div>
    <div class="w-full overflow-x-auto rounded-b-lg">
      <table class="w-full min-w-full table-auto bg-white dark:bg-[#171131ef]">
        <thead class="bg-gray-200 dark:bg-[#211849ef]">
          <tr>
            <th v-if="authStore.user.is_complex_branched"
              class="border-y border-gray-300 dark:border-[#171131ef] p-3 select-none text-[0.8rem]">
              <button class="pt-2 select-none" @click="selectAll">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-4" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <circle :class="{ 'opacity-0': !isAllSelected, 'opacity-100': isAllSelected }"
                    class="transition duration-300 ease-out" cx="12" cy="12" r="3">
                  </circle>
                </svg>
              </button>
            </th>
            <th class="border-y border-gray-300 dark:border-[#171131ef] p-3 select-none text-left text-[0.8rem]">
              T/B
            </th>
            <th
              class="transition duration-200 ease-in border-y border-gray-300 dark:border-[#171131ef] dark:hover:bg-[#32237cef] p-3 select-none cursor-pointer hover:bg-gray-300  text-left text-[0.8rem]"
              @click="sort('name')">
              ADY
              <span :class="sortColumn === 'name' ? (sortOrder === 'asc' ? 'rotate-180' : '') : 'opacity-50'"
                class="ml-2 transition-transform duration-200 inline-block">
                ▲
              </span>
            </th>
            <th
              class="transition duration-200 ease-in border-y border-gray-300 dark:border-[#171131ef] dark:hover:bg-[#32237cef] p-3 select-none cursor-pointer hover:bg-gray-300  text-left text-[0.8rem]"
              @click="sort('department')" v-if="authStore.role === 'user'">
              KAFEDRASY
              <span :class="sortColumn === 'department' ? (sortOrder === 'asc' ? 'rotate-180' : '') : 'opacity-50'"
                class="ml-2 transition-transform duration-200 inline-block">
                ▲
              </span>
            </th>
            <th
              class="transition duration-200 ease-in border-y border-gray-300 dark:border-[#171131ef] dark:hover:bg-[#32237cef] p-3 select-none cursor-pointer hover:bg-gray-300  text-left text-[0.8rem]"
              @click="sort('classificator')">
              KLASSIFIKATORY
              <span :class="sortColumn === 'classificator' ? (sortOrder === 'asc' ? 'rotate-180' : '') : 'opacity-50'"
                class="ml-2 transition-transform duration-200 inline-block">
                ▲
              </span>
            </th>
            <th
              class="transition duration-200 ease-in border-y border-gray-300 dark:border-[#171131ef] dark:hover:bg-[#32237cef] p-3 select-none cursor-pointer hover:bg-gray-300 text-left text-[0.8rem]"
              @click="sort('students_count')">
              JEMI
              <span :class="sortColumn === 'students_count' ? (sortOrder === 'asc' ? 'rotate-180' : '') : 'opacity-50'"
                class="ml-2 transition-transform duration-200 inline-block">
                ▲
              </span>
            </th>
            <th
              class="transition duration-200 ease-in border-y border-gray-300 dark:border-[#171131ef] dark:hover:bg-[#32237cef] p-3 select-none cursor-pointer hover:bg-gray-300 text-left text-[0.8rem]"
              @click="sort('male_count')">
              OGLAN
              <span :class="sortColumn === 'male_count' ? (sortOrder === 'asc' ? 'rotate-180' : '') : 'opacity-50'"
                class="ml-2 transition-transform duration-200 inline-block">
                ▲
              </span>
            </th>
            <th
              class="transition duration-200 ease-in border-y border-gray-300 dark:border-[#171131ef] dark:hover:bg-[#32237cef] p-3 select-none cursor-pointer hover:bg-gray-300 text-left text-[0.8rem]"
              @click="sort('female_count')">
              GYZ
              <span :class="sortColumn === 'female_count' ? (sortOrder === 'asc' ? 'rotate-180' : '') : 'opacity-50'"
                class="ml-2 transition-transform duration-200 inline-block">
                ▲
              </span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in data" :key="item.id"
            class="transition ease-in hover:ease-out duration-200 hover:bg-gray-100 dark:hover:bg-[#261953]">
            <td v-if="authStore.user.is_complex_branched"
              class="border-y border-gray-300 dark:border-[#32237cef] px-4 py-2 break-words text-[0.8rem] text-center">
              <button class="select-none" @click="checkboxClicked(item.id)">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-4" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <circle
                    :class="{ 'opacity-0': !selectedItems.includes(item.id), 'opacity-100': selectedItems.includes(item.id) }"
                    class="transition duration-300 ease-out" cx="12" cy="12" r="3">
                  </circle>
                </svg>
              </button>
            </td>
            <td class="border-y border-gray-300 dark:border-[#32237cef] px-4 py-2 break-words text-[0.8rem]">{{
              ((currentPage - 1) * rowsPerPage) + (index + 1)
            }}
            </td>
            <td class="border-y border-gray-300 dark:border-[#32237cef] p-2 break-words text-[0.8rem]">{{
              item.name
            }}
            </td>
            <td class="border-y border-gray-300 dark:border-[#32237cef] py-2 px-3 break-words text-[0.8rem]"
              v-if="typeof (item.department) === 'string'">{{
                item.department
              }}
            </td>
            <td v-else :title="item.department.join('\n')"
              class="border-y border-gray-300 dark:border-[#32237cef] py-2 px-3 break-words text-[0.8rem]">Birnäçe
              kafedrasy bar
            </td>
            <td v-if="typeof (item.classificator) === 'string'"
              class="border-y border-gray-300 dark:border-[#32237cef] p-2 break-words text-[0.8rem]">
              <div
                class="max-w-32 lg:max-w-64 text-wrap py-2 px-3 transition duration-200 ease-out select-none rounded-lg"
                :class="{ 'hover:bg-red-500 dark:hover:bg-pink-900 hover:text-white': item.classificator === 'Ýok', 'hover:bg-emerald-500 dark:hover:bg-emerald-700 hover:text-white': item.classificator !== 'Ýok' }">
                {{
                  item.classificator }}</div>
            </td>
            <td v-else :title="item.classificator.join('\n')"
              class="border-y border-gray-300 dark:border-[#32237cef] py-2 px-5 break-words text-[0.8rem]">Birnäçe
              klassifikatory bar
            </td>
            <td class="border-y border-gray-300 dark:border-[#32237cef] p-2 break-words text-[0.8rem]">
              {{ item.students_count }}
            </td>
            <td class="border-y border-gray-300 dark:border-[#32237cef] p-2 break-words text-[0.8rem]">{{
              item.male_count
            }}
            </td>
            <td class="border-y border-gray-300 dark:border-[#32237cef] p-2 break-words text-[0.8rem]">
              {{ item.female_count }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="flex justify-center items-center mt-4 space-x-2 overflow-x-auto">
    <button class="select-none" :class="activeBtnClasses" v-if="currentPage !== 1" @click="changePage(currentPage - 1)">
      <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M13 8L9 12M9 12L13 16M9 12H21M19.4845 7C17.8699 4.58803 15.1204 3 12 3C7.02944 3 3 7.02944 3 12C3 16.9706 7.02944 21 12 21C15.1204 21 17.8699 19.412 19.4845 17"
          stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
    </button>

    <button class="select-none" v-if="currentPage > 3" :class="defaultBtnClasses" @click="changePage(1)">
      1
    </button>

    <span v-if="currentPage > 4" class="px-2 select-none">...</span>

    <button class="select-none" v-for="page in pagesBefore" :key="'before-' + page" :class="defaultBtnClasses"
      @click="changePage(page)">
      {{ page }}
    </button>

    <button class="select-none" :class="activeBtnClasses" v-if="totalPages !== 0">
      {{ currentPage }}
    </button>

    <button class="select-none" v-for="page in pagesAfter" :key="'after-' + page" :class="defaultBtnClasses"
      @click="changePage(page)">
      {{ page }}
    </button>

    <span v-if="currentPage < totalPages - 3" class="px-2 select-none">...</span>

    <button v-if="currentPage < totalPages - 2" :class="defaultBtnClasses" @click="changePage(totalPages)">
      {{ totalPages }}
    </button>

    <button class="select-none" :class="activeBtnClasses" v-if="currentPage !== totalPages && totalPages !== 0"
      @click="changePage(currentPage + 1)">
      <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M11 16L15 12M15 12L11 8M15 12H3M4.51555 17C6.13007 19.412 8.87958 21 12 21C16.9706 21 21 16.9706 21 12C21 7.02944 16.9706 3 12 3C8.87958 3 6.13007 4.58803 4.51555 7"
          stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
    </button>
  </div>
  <div class="flex items-center justify-center">
    <input placeholder="#" type="number" v-model.number="customPage"
      class="w-14 dark:text-gray-300 transition duration-200 ease-in bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-l-full focus:ring focus:ring-blue-200 focus:outline-none">
    <button @click="changePage(customPage)"
      class="p-4 py-2 my-2 rounded-r-full border-none dark:border-violet-500/50 border-1 bg-blue-500 dark:bg-violet-600 text-white">
      <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M11 16L15 12M15 12L11 8M15 12H3M4.51555 17C6.13007 19.412 8.87958 21 12 21C16.9706 21 21 16.9706 21 12C21 7.02944 16.9706 3 12 3C8.87958 3 6.13007 4.58803 4.51555 7"
          stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
    </button>
  </div>
</template>

<style scoped></style>
