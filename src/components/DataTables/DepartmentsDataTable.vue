<script setup>
import { computed, defineProps, onMounted, ref, watch } from 'vue';
import ConfirmModal from "@/components/Modals/ConfirmModal.vue";
import useConfirmModal from "@/use/useModalWindow.js";
import TheToast from "@/components/TheToast.vue";
import useToast from "@/use/useToast.js";
import { useDepartmentsStore } from "@/stores/api.store.js";
import { storeToRefs } from "pinia";
import router from "@/router/index.js";
import { useAuthStore } from "@/stores/auth.store.js";


const props = defineProps(["data"])
const emit = defineEmits(["update"]);

watch(props, (newVal, oldVal) => {
  data.value = newVal.data;
  filteredData.value = [...data.value];
})

const { isModalOpen, openModal, header, context } = useConfirmModal();
const { toasts, addToast } = useToast();
const authStore = useAuthStore();
const departmentsStore = useDepartmentsStore();
const { deleteStatus, updateStatus, createStatus } = storeToRefs(departmentsStore);

const data = ref([]);
const filteredData = ref([]);
const selectedItem = ref(null);

if (props.data.length > 0) {
  data.value = props.data;
  filteredData.value = [...data.value];
}

const activeBtnClasses = ref("p-4 py-2 my-2 rounded-full border-none dark:border-violet-500/50 border-1 bg-blue-500 dark:bg-violet-600 text-white");
const defaultBtnClasses = ref("p-4 py-2 my-2 rounded-full border-none bg-gray-200 dark:bg-[#261953]");
const sortColumn = ref("name");
const sortOrder = ref('asc');
const currentPage = ref(1);
const rowsPerPage = ref(10);
const rowsPerPageOptions = [10, 20, 50, 100];
const searchQuery = ref('');
const isSearching = ref(false);

const applySearch = () => {
  filteredData.value = data.value.filter((item) =>
    item.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
  currentPage.value = 1;
  isSearching.value = true;
};

const resetTable = () => {
  searchQuery.value = '';
  filteredData.value = [...data.value];
  currentPage.value = 1;
  isSearching.value = false;
};

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
  departmentsStore.delete(selectedItem.value).then(() => {
    emit('update');
  });
  selectedItem.value = null;
}

watch(deleteStatus, (newVal, oldVal) => {
  if (newVal) {
    if (newVal === 'success') {
      addToast('Kafedra üstünlikli ýok edildi', 'success');
    } else if (newVal === 'error') {
      addToast('Ýok etme prosesinde ýalňyşlyk ýüze çykdy', 'error');
    }
  }
  deleteStatus.value = null;
})

onMounted(() => {
  if (updateStatus.value) {
    if (updateStatus.value === 'success') {
      addToast('Kafedra üstünlikli üýtgedildi', 'success');
    } else if (updateStatus.value === 'error') {
      addToast('Üýtgetme prosesinde ýalňyşlyk ýüze çykdy', 'error');
    }
  }
  updateStatus.value = null;

  if (createStatus.value) {
    if (createStatus.value === 'success') {
      addToast('Kafedra üstünlikli hasaba alyndy', 'success');
    } else if (createStatus.value === 'error') {
      addToast('Hasaba alma prosesinde ýalňyşlyk ýüze çykdy', 'error');
    }
  }
  createStatus.value = null;
})


window.addEventListener("click", onClickOutside);

</script>

<template>
  <confirm-modal :is-open="isModalOpen" @close="closeModal" @submit="submitModal" :header="header"
    :context='`\"${context}\" ýok edilmegini tassyklaýarsyňyzmy?`'></confirm-modal>

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
        <div class="lg:w-1/3 md:w-1/3 w-2/3 flex items-center space-x-2">
          <button @click="resetTable" :class="{ 'opacity-0': !isSearching }" :disabled="!isSearching"
            class="p-2 text-sm rounded-xl shadow-md border-none dark:border-violet-500/50 border-1 bg-blue-500 dark:bg-violet-600 text-white">
            <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="w-6 h-6"
              viewBox="0 0 24 24" version="1.1">
              <title>Reload</title>
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
          <input v-model="searchQuery" type="text" @keyup.enter="applySearch" placeholder="Gözleg"
            class="w-full dark:text-gray-300 transition duration-200 ease-in bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none" />
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
              @click="sort('name')">
              KAFEDRA
              <span :class="sortColumn === 'name' ? (sortOrder === 'asc' ? 'rotate-180' : '') : 'opacity-50'"
                class="ml-2 transition-transform duration-200 inline-block">
                ▲
              </span>
            </th>
            <th
              class="transition duration-200 ease-in border-y border-gray-300 dark:border-[#171131ef] dark:hover:bg-[#32237cef] p-3 select-none cursor-pointer hover:bg-gray-300  text-left text-[0.8rem]"
              @click="sort('faculty')" v-if="authStore.role === 'user'">
              FAKULTETI
              <span :class="sortColumn === 'faculty' ? (sortOrder === 'asc' ? 'rotate-180' : '') : 'opacity-50'"
                class="ml-2 transition-transform duration-200 inline-block">
                ▲
              </span>
            </th>
            <th
              class="transition duration-200 ease-in border-y border-gray-300 dark:border-[#171131ef] dark:hover:bg-[#32237cef] p-3 select-none cursor-pointer hover:bg-gray-300  text-left text-[0.8rem]"
              @click="sort('specializations_count')" v-if="authStore.role === 'user'">
              HÜNÄR SANY
              <span
                :class="sortColumn === 'specializations_count' ? (sortOrder === 'asc' ? 'rotate-180' : '') : 'opacity-50'"
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
            <th class="border-y border-gray-300 dark:border-[#171131ef]  p-3 select-none text-center text-[0.8rem]"
              v-if="authStore.role === 'root'">
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
              item.name
              }}
            </td>
            <td class="border-y border-gray-300 dark:border-[#32237cef] p-2 break-words text-[0.8rem]"
              v-if="authStore.role === 'user'">{{
                item.faculty
              }}
            </td>
            <td class="border-y border-gray-300 dark:border-[#32237cef] p-2 break-words text-[0.8rem]"
              v-if="authStore.role === 'user'">{{
                item.specializations_count
              }}
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
            <td class="border-y border-gray-300 dark:border-[#32237cef] p-2 break-words text-[0.8rem]"
              v-if="authStore.role === 'root'">
              <div class="w-full flex items-center justify-center">
                <div class="inline-flex rounded-md shadow-xs" role="group">
                  <button type="button" :key="item.id" @click="router.push(`/departments/edit/${item.id}`)"
                    title="Üýtgetmek"
                    class="px-4 py-2 text-[0.8rem] font-medium bg-emerald-400 hover:bg-emerald-500 transition ease-in hover:ease-out duration-200 text-white dark:bg-emerald-700 border border-gray-200 rounded-s-lg focus:z-10 focus:ring-2 focus:ring-emerald-500 dark:border-gray-700 select-none">
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-5" viewBox="0 0 24 24">
                      <title />
                      <g id="Complete">
                        <g id="edit">
                          <g>
                            <path d="M20,16v4a2,2,0,0,1-2,2H4a2,2,0,0,1-2-2V6A2,2,0,0,1,4,4H8" fill="none"
                              stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
                            <polygon fill="none" points="12.5 15.8 22 6.2 17.8 2 8.3 11.5 8 16 12.5 15.8"
                              stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
                          </g>
                        </g>
                      </g>
                    </svg>
                  </button>
                  <button type="button" :key="item.id"
                    @click="router.push({ name: 'students-list', query: { 'department': item.id } })"
                    class="px-4 py-2 text-[0.8rem] font-medium bg-violet-400 hover:bg-violet-500 transition ease-in hover:ease-out duration-200 text-white dark:bg-violet-700 border border-gray-200 focus:z-10 focus:ring-2 focus:ring-violet-500 dark:border-gray-700 select-none"
                    title="Görmek">
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-5" viewBox="0 0 24 24" fill="none">
                      <path fill-rule="evenodd" clip-rule="evenodd"
                        d="M12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9ZM11 12C11 11.4477 11.4477 11 12 11C12.5523 11 13 11.4477 13 12C13 12.5523 12.5523 13 12 13C11.4477 13 11 12.5523 11 12Z"
                        fill="currentColor" />
                      <path fill-rule="evenodd" clip-rule="evenodd"
                        d="M21.83 11.2807C19.542 7.15186 15.8122 5 12 5C8.18777 5 4.45796 7.15186 2.17003 11.2807C1.94637 11.6844 1.94361 12.1821 2.16029 12.5876C4.41183 16.8013 8.1628 19 12 19C15.8372 19 19.5882 16.8013 21.8397 12.5876C22.0564 12.1821 22.0536 11.6844 21.83 11.2807ZM12 17C9.06097 17 6.04052 15.3724 4.09173 11.9487C6.06862 8.59614 9.07319 7 12 7C14.9268 7 17.9314 8.59614 19.9083 11.9487C17.9595 15.3724 14.939 17 12 17Z"
                        fill="currentColor" />
                    </svg>
                  </button>
                  <button type="button" :key="item.id" @click="openModalWrapper('Ýok etmek', item.name, item.id)"
                    class="px-4 py-2 text-[0.8rem] font-medium bg-red-400 hover:bg-red-500 transition ease-in hover:ease-out duration-200 text-white dark:bg-pink-900 dark:hover:bg-pink-600 border border-gray-200 rounded-e-lg focus:z-10 focus:ring-2 focus:ring-red-500 dark:border-gray-700  dark:focus:ring-pink-500 select-none"
                    title="Pozmak">
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-5" viewBox="0 0 24 24" fill="none">
                      <path
                        d="M18 6L17.1991 18.0129C17.129 19.065 17.0939 19.5911 16.8667 19.99C16.6666 20.3412 16.3648 20.6235 16.0011 20.7998C15.588 21 15.0607 21 14.0062 21H9.99377C8.93927 21 8.41202 21 7.99889 20.7998C7.63517 20.6235 7.33339 20.3412 7.13332 19.99C6.90607 19.5911 6.871 19.065 6.80086 18.0129L6 6M4 6H20M16 6L15.7294 5.18807C15.4671 4.40125 15.3359 4.00784 15.0927 3.71698C14.8779 3.46013 14.6021 3.26132 14.2905 3.13878C13.9376 3 13.523 3 12.6936 3H11.3064C10.477 3 10.0624 3 9.70951 3.13878C9.39792 3.26132 9.12208 3.46013 8.90729 3.71698C8.66405 4.00784 8.53292 4.40125 8.27064 5.18807L8 6M14 10V17M10 10V17"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
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
  <teleport to="body">
    <div class="toast-container w-5/6 fixed top-25
       md:top-auto md:bottom-5 right-5 md:w-1/4 flex flex-col-reverse space-y-2">
      <TransitionGroup name="toast">
        <the-toast v-for="toast in toasts" :key="toast.id" :message="toast.message" :type="toast.type"
          :duration="toast.duration" :onClose="() => (toasts = toasts.filter((t) => t.id !== toast.id))"></the-toast>
      </TransitionGroup>
    </div>
  </teleport>
</template>

<style scoped>
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


.toast-move,
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>
