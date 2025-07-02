<script setup>
import { computed, defineProps, ref, watch } from 'vue';
import useConfirmModal from "@/use/useModalWindow.js";
import { useDiplomasStore } from "@/stores/api.store.js";
import ConfirmModal from '../Modals/ConfirmModal.vue';

const props = defineProps(["data"])
const emit = defineEmits(["update"]);

watch(props, (newVal) => {
  data.value = newVal.data;
  filteredData.value = [...data.value];
})

const { isModalOpen, openModal, header, context } = useConfirmModal();
const diplomasStore = useDiplomasStore();

const data = ref([]);
const filteredData = ref([]);
const selectedItem = ref(null);


const activeBtnClasses = ref("p-4 py-2 my-2 rounded-full border-none dark:border-violet-500/50 border-1 bg-blue-500 dark:bg-violet-600 text-white");
const defaultBtnClasses = ref("p-4 py-2 my-2 rounded-full border-none bg-gray-200 dark:bg-[#261953]");
const sortColumn = ref("request_date");
const sortOrder = ref('asc');
const currentPage = ref(1);
const rowsPerPage = ref(10);
const rowsPerPageOptions = [10, 20, 50, 100];
const customPage = ref(currentPage.value);


const sortedData = computed(() => {
  if (!sortColumn.value) return data.value;
  return [...filteredData.value].sort((a, b) => {
    if (a[sortColumn.value] < b[sortColumn.value]) return sortOrder.value === 'asc' ? -1 : 1;
    if (a[sortColumn.value] > b[sortColumn.value]) return sortOrder.value === 'asc' ? 1 : -1;
    return 0;
  });
});

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * rowsPerPage.value;
  return sortedData.value.slice(start, start + rowsPerPage.value);
});

const totalPages = computed(() => Math.ceil(sortedData.value.length / rowsPerPage.value));

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
};

const changeRowsPerPage = (option) => {
  rowsPerPage.value = parseInt(option, 10);
  currentPage.value = 1;
  isOpen.value = false;

};

const pagesBefore = computed(() => {
  const start = Math.max(2, currentPage.value - 2);
  return Array.from({ length: Math.max(0, currentPage.value - start) }, (_, i) => start + i);
});

const pagesAfter = computed(() => {
  const end = Math.min(totalPages.value - 1, currentPage.value + 2);
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


function openModalWrapper(headerText, content, id) {
  openModal(headerText, content);
  selectedItem.value = id;
}


function closeModal() {
  isModalOpen.value = false;
  selectedItem.value = null;
}


function submitModal() {
  isModalOpen.value = false;
  diplomasStore.submitReport(selectedItem.value).then(() => {
    emit('update');
  });
  selectedItem.value = null;
}


</script>

<template>
  <confirm-modal :is-open="isModalOpen" @close="closeModal" @submit="submitModal" :header="header"
    :context='`${context} arzasyny tassyklaýarsyňyzmy?`'></confirm-modal>

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
        <div>
          <h4 class="font-bold select-none">HASABATLAR</h4>
        </div>
      </div>
    </div>
    <div class="w-full overflow-x-auto rounded-b-lg">
      <table class="w-full min-w-full table-auto bg-white dark:bg-[#171131ef]">
        <thead class="bg-gray-200 dark:bg-[#211849ef]">
          <tr>
            <th class="border-y border-gray-300 dark:border-[#171131ef] p-3 select-none text-left text-[0.8rem]">
              T/B
            </th>
            <th
              class="transition duration-200 ease-in border-y border-gray-300 dark:border-[#171131ef] dark:hover:bg-[#32237cef] p-3 select-none cursor-pointer hover:bg-gray-300  text-left text-[0.8rem]"
              @click="sort('sender')">
              UGRADYJY
              <span :class="sortColumn === 'sender' ? (sortOrder === 'asc' ? 'rotate-180' : '') : 'opacity-50'"
                class="ml-2 transition-transform duration-200 inline-block">
                ▲
              </span>
            </th>
            <th
              class="transition duration-200 ease-in border-y border-gray-300 dark:border-[#171131ef] dark:hover:bg-[#32237cef] p-3 select-none cursor-pointer hover:bg-gray-300  text-left text-[0.8rem]"
              @click="sort('two_year_work_off')">
              IKI ÝYL IŞ
              <span
                :class="sortColumn === 'two_year_work_off' ? (sortOrder === 'asc' ? 'rotate-180' : '') : 'opacity-50'"
                class="ml-2 transition-transform duration-200 inline-block">
                ▲
              </span>
            </th>
            <th
              class="transition duration-200 ease-in border-y border-gray-300 dark:border-[#171131ef] dark:hover:bg-[#32237cef] p-3 select-none cursor-pointer hover:bg-gray-300  text-left text-[0.8rem]"
              @click="sort('died')">
              ÝOGALAN
              <span :class="sortColumn === 'died' ? (sortOrder === 'asc' ? 'rotate-180' : '') : 'opacity-50'"
                class="ml-2 transition-transform duration-200 inline-block">
                ▲
              </span>
            </th>
            <th
              class="transition duration-200 ease-in border-y border-gray-300 dark:border-[#171131ef] dark:hover:bg-[#32237cef] p-3 select-none cursor-pointer hover:bg-gray-300  text-left text-[0.8rem]"
              @click="sort('went_abroad')">
              DAŞARY ÝURDA GIDEN
              <span :class="sortColumn === 'went_abroad' ? (sortOrder === 'asc' ? 'rotate-180' : '') : 'opacity-50'"
                class="ml-2 transition-transform duration-200 inline-block">
                ▲
              </span>
            </th>
            <th
              class="transition duration-200 ease-in border-y border-gray-300 dark:border-[#171131ef] dark:hover:bg-[#32237cef] p-3 select-none cursor-pointer hover:bg-gray-300  text-left text-[0.8rem]"
              @click="sort('other_reasons')">
              GAÝRY SEBÄPLER
              <span :class="sortColumn === 'other_reasons' ? (sortOrder === 'asc' ? 'rotate-180' : '') : 'opacity-50'"
                class="ml-2 transition-transform duration-200 inline-block">
                ▲
              </span>
            </th>
            <th
              class="transition duration-200 ease-in border-y border-gray-300 dark:border-[#171131ef] dark:hover:bg-[#32237cef] p-3 select-none cursor-pointer hover:bg-gray-300  text-left text-[0.8rem]"
              @click="sort('request_date')">
              WAGTY
              <span :class="sortColumn === 'request_date' ? (sortOrder === 'asc' ? 'rotate-180' : '') : 'opacity-50'"
                class="ml-2 transition-transform duration-200 inline-block">
                ▲
              </span>
            </th>
            <th class="border-y border-gray-300 dark:border-[#171131ef]  p-3 select-none text-center text-[0.8rem]">
              GURALLAR
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in paginatedData" :key="item.id"
            class="transition ease-in hover:ease-out duration-200 hover:bg-gray-100 dark:hover:bg-[#261953]">
            <td class="border-y border-gray-300 dark:border-[#32237cef] px-4 py-2 break-words text-[0.8rem]">{{
              ((currentPage - 1) * rowsPerPage) + (index + 1)
              }}
            </td>
            <td class="border-y border-gray-300 dark:border-[#32237cef] p-2 break-words text-[0.8rem]">{{
              item.sender
              }}
            </td>
            <td class="border-y border-gray-300 dark:border-[#32237cef] p-2 break-words text-[0.8rem]">
              {{
                item.two_year_work_off
              }}
            </td>
            <td class="border-y border-gray-300 dark:border-[#32237cef] p-2 break-words text-[0.8rem]">
              {{
                item.died
              }}
            </td>
            <td class="border-y border-gray-300 dark:border-[#32237cef] p-2 break-words text-[0.8rem]">
              {{
                item.went_abroad
              }}
            </td>
            <td class="border-y border-gray-300 dark:border-[#32237cef] p-2 break-words text-[0.8rem]">
              {{
                item.other_reasons
              }}
            </td>
            <td class="border-y border-gray-300 dark:border-[#32237cef] p-2 break-words text-[0.8rem]">{{
              item.request_date
              }}
            </td>
            <td class="border-y border-gray-300 dark:border-[#32237cef] p-2 break-words text-[0.8rem]">
              <div class="w-full flex items-center justify-center" v-if="item.verdict === 'C'">
                <div class="inline-flex rounded-md shadow-xs" role="group">
                  <div
                    class="px-4 py-2 text-[0.8rem] font-medium bg-emerald-600  transition ease-in hover:ease-out duration-200 text-white dark:bg-emerald-700 border border-gray-200 rounded-lg dark:border-gray-700 select-none">
                    Tassyklandy
                  </div>
                </div>
              </div>
              <div class="w-full flex items-center justify-center" v-else>
                <div class="inline-flex rounded-md shadow-xs" role="group">
                  <button type="button" @click="openModalWrapper('Tassyklamak', item.sender, item.id)"
                    class="px-4 py-2 text-[0.8rem] font-medium bg-emerald-400 hover:bg-emerald-500 transition ease-in hover:ease-out duration-200 text-white dark:bg-emerald-700 border border-gray-200 rounded-lg focus:z-10 focus:ring-2 focus:ring-emerald-500 dark:border-gray-700 select-none">
                    Tassyklamak
                  </button>
                </div>
              </div>
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
