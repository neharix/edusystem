<script setup>
import ButtonWithTooltip from "./ButtonWithTooltip.vue";
import { useAuthStore } from "@/stores/auth.store";
import DropdownNotification from "./DropdownNotification.vue";
import { computed, ref } from "vue";
import { storeToRefs } from "pinia";
import useConfirmModal from "@/use/useModalWindow";
import ConfirmModal from "@/components/Modals/ConfirmModal.vue";
import { useSpecialFunctionsStore, useStudentsStore } from "@/stores/api.store";
import { useRoute } from "vue-router";


const props = defineProps({
  enableDumper: {
    type: Boolean,
    required: false,
    default: false,
  },
  isDark: Boolean,
  isMobile: Boolean,
});

const submitFunction = ref(() => { console.log('nothing to do') });

const specialFunctionsStore = useSpecialFunctionsStore();
const studentsStore = useStudentsStore();
const authStore = useAuthStore();

const { notifications, user, role } = storeToRefs(authStore);

const route = useRoute();

const { isModalOpen, openModal, header, context } = useConfirmModal();

function getDumpFile() {
  specialFunctionsStore.getDump().then(() => {
    let now = new Date();
    const blob = new Blob([specialFunctionsStore.dump], { type: specialFunctionsStore.dumpContentType })
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.target = "_blank";
    link.download = `bmdu-dump-${now.toISOString()}.zip`;
    link.classList.add('hidden');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  })
}

function updateStudyYears() {
  studentsStore.updateStudyYears().then(() => {
    studentsStore.getAllAdditional();
  });
}

function openModalWrap(header, content, func) {
  submitFunction.value = func;
  openModal(header, content);
}

function submitModal(func) {
  func();
  isModalOpen.value = false;
}


const diplomas = ref(null);

const statementsVisibility = computed(() => {
  try {
    let isVisible = false;
    for (let notification of user.value.notifications) {
      if (notification.type === "expulsion" || notification.type === "reinstate") {
        isVisible = true;
      }
    }
    return isVisible;
  } catch {
    return false
  }
})

const diplomasVisibility = computed(() => {
  try {
    let isVisible = false;
    for (let notification of user.value.notifications) {
      if (notification.type === "diploma") {
        isVisible = true;
      }
    }
    return isVisible;
  } catch {
    return false
  }
})

const teacherStatementsVisibility = computed(() => {
  try {
    let isVisible = false;
    for (let notification of user.value.notifications) {
      if (notification.type === "teacher") {
        isVisible = true;
      }
    }
    return isVisible;
  } catch {
    return false
  }
})


const isOpen = ref(false);
const isMobileMenuOpen = ref(false);


function toggleMenu() {
  isOpen.value = !isOpen.value;
}

function toggleMobileMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
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


const emit = defineEmits(["toggle-theme"]);

</script>

<template>
  <div>
    <div class="hidden lg:flex lg:items-center space-x-2">
      <div class="relative inline-block text-left">
        <div>
          <button v-if="notifications.length > 0" id="dropdown" class="relative" @click="toggleMenu">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 mt-1" viewBox="0 0 24 24">
              <rect width="24" height="24" fill="none" />
              <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M10.268 21a2 2 0 0 0 3.464 0M22 8c0-2.3-.8-4.3-2-6M3.262 15.326A1 1 0 0 0 4 17h16a1 1 0 0 0 .74-1.673C19.41 13.956 18 12.499 18 8A6 6 0 0 0 6 8c0 4.499-1.411 5.956-2.738 7.326M4 2C2.8 3.7 2 5.7 2 8" />
            </svg>
            <div class="bg-red-500 px-1.5 py-0.5 text-white text-xs rounded-full absolute -top-1 -right-1">{{
              notifications.length
              }}</div>
          </button>
          <transition name="fade-scale" @before-enter="el => (el.style.display = 'block')"
            @after-leave="el => (el.style.display = 'none')">
            <div v-show="isOpen"
              class="absolute overflow-y-auto right-0 z-10 mt-2 w-56 max-h-[40vh] origin-top-right rounded-md border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#171131ef] shadow-lg ring-1 ring-white dark:ring-gray-800 ring-opacity-5">
              <div class="px-2 pt-2 select-none" v-if="statementsVisibility">
                <h3 class="uppercase text-center">
                  Arzalar</h3>
              </div>
              <div class="py-1" v-if="statementsVisibility">
                <dropdown-notification :types="['expulsion', 'reinstate']"
                  :redirect-to="`/statements/${notification.id}/${notification.type}`"
                  v-for="(notification, index) in user.notifications" :notification="notification"
                  :key="index"></dropdown-notification>
              </div>
              <div class="px-2 pt-2 select-none" v-if="diplomasVisibility">
                <h3 class="uppercase text-center">Diplomlar</h3>
              </div>
              <div class="py-1" ref="diplomas" v-if="diplomasVisibility">
                <dropdown-notification :types="['diploma']" :redirect-to="`/diplomas/view/${notification.id}`"
                  v-for="(notification, index) in user.notifications" :notification="notification"
                  :key="index"></dropdown-notification>
              </div>
              <div class="px-2 pt-2 select-none" v-if="teacherStatementsVisibility">
                <h3 class="uppercase text-center">
                  Mugallymlar</h3>
              </div>
              <div class="py-1" v-if="teacherStatementsVisibility">
                <dropdown-notification :types="['teacher']" :redirect-to="`/teachers/view/${notification.id}`"
                  v-for="(notification, index) in user.notifications" :notification="notification"
                  :key="index"></dropdown-notification>
              </div>

            </div>
          </transition>
        </div>
      </div>
      <button-with-tooltip v-if="role === 'root' && enableDumper" text-value="Umumy import" position-classes="right-30"
        @clicked="openModalWrap('Umumy import', 'Maglumat gorundaky ähli maglumatlaryň importyny tassyklaýarsyňyzmy?', getDumpFile)">
        <template #btn-content>
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6" viewBox="0 0 24 24" fill="none">
            <path
              d="M16.9999 19C19.209 19 20.9999 17.2091 20.9999 15C20.9999 12.7909 19.209 11 16.9999 11H16.9774C16.9923 10.8353 16.9999 10.6685 16.9999 10.5C16.9999 7.46243 14.5374 5 11.4999 5C8.4623 5 5.99986 7.46243 5.99986 10.5C5.99986 10.5047 5.99987 10.5095 5.99988 10.5142C4.04366 10.9113 2.57129 12.6408 2.57129 14.7142C2.57129 17.0811 4.49007 18.9999 6.857 18.9999"
              stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <path d="M12 14L12 19M12 19L14 17M12 19L10 17" stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round" />
          </svg>
        </template>
      </button-with-tooltip>

      <button-with-tooltip @clicked="emit('toggle-theme')" position-classes="right-20"
        :text-value="isDark ? 'Ýagty tema' : 'Garaňky tema'" class="flex items-center p-2 dark:text-gray-100 rounded">
        <template #btn-content>
          <svg viewBox="0 0 24 24" class="w-6 h-6 m-0 text-gray-800 dark:text-white" :class="{ hidden: isDark }"
            fill="none" xmlns="http://www.w3.org/2000/svg">
            <path
              d="M11 1C11 0.447715 11.4477 0 12 0C12.5523 0 13 0.447715 13 1V3C13 3.55228 12.5523 4 12 4C11.4477 4 11 3.55228 11 3V1Z"
              fill="currentColor" />
            <path fill-rule="evenodd" clip-rule="evenodd"
              d="M18 12C18 15.3137 15.3137 18 12 18C8.68629 18 6 15.3137 6 12C6 8.68629 8.68629 6 12 6C15.3137 6 18 8.68629 18 12ZM8.06167 12C8.06167 14.1751 9.82492 15.9383 12 15.9383C14.1751 15.9383 15.9383 14.1751 15.9383 12C15.9383 9.82492 14.1751 8.06167 12 8.06167C9.82492 8.06167 8.06167 9.82492 8.06167 12Z"
              fill="currentColor" />
            <path
              d="M20.4853 3.51472C20.0947 3.12419 19.4616 3.12419 19.0711 3.51472L17.6568 4.92893C17.2663 5.31946 17.2663 5.95262 17.6568 6.34315C18.0474 6.73367 18.6805 6.73367 19.0711 6.34315L20.4853 4.92893C20.8758 4.53841 20.8758 3.90524 20.4853 3.51472Z"
              fill="currentColor" />
            <path
              d="M1 13C0.447715 13 0 12.5523 0 12C0 11.4477 0.447715 11 1 11H3C3.55228 11 4 11.4477 4 12C4 12.5523 3.55228 13 3 13H1Z"
              fill="currentColor" />
            <path
              d="M3.51472 3.51472C3.1242 3.90524 3.1242 4.53841 3.51472 4.92893L4.92894 6.34315C5.31946 6.73367 5.95263 6.73367 6.34315 6.34315C6.73368 5.95262 6.73368 5.31946 6.34315 4.92893L4.92894 3.51472C4.53841 3.12419 3.90525 3.12419 3.51472 3.51472Z"
              fill="currentColor" />
            <path
              d="M11 21C11 20.4477 11.4477 20 12 20C12.5523 20 13 20.4477 13 21V23C13 23.5523 12.5523 24 12 24C11.4477 24 11 23.5523 11 23V21Z"
              fill="currentColor" />
            <path
              d="M6.34315 17.6569C5.95263 17.2663 5.31946 17.2663 4.92894 17.6569L3.51473 19.0711C3.1242 19.4616 3.1242 20.0948 3.51473 20.4853C3.90525 20.8758 4.53842 20.8758 4.92894 20.4853L6.34315 19.0711C6.73368 18.6805 6.73368 18.0474 6.34315 17.6569Z"
              fill="currentColor" />
            <path
              d="M21 13C20.4477 13 20 12.5523 20 12C20 11.4477 20.4477 11 21 11H23C23.5523 11 24 11.4477 24 12C24 12.5523 23.5523 13 23 13H21Z"
              fill="currentColor" />
            <path
              d="M17.6568 17.6569C17.2663 18.0474 17.2663 18.6805 17.6568 19.0711L19.0711 20.4853C19.4616 20.8758 20.0947 20.8758 20.4853 20.4853C20.8758 20.0948 20.8758 19.4616 20.4853 19.0711L19.0711 17.6569C18.6805 17.2663 18.0474 17.2663 17.6568 17.6569Z"
              fill="currentColor" />
          </svg>
          <svg viewBox="0 0 24 24" class="w-6 h-6 m-0" :class="{ hidden: !isDark }" fill="none"
            xmlns="http://www.w3.org/2000/svg">
            <path
              d="M13 6V3M18.5 12V7M14.5 4.5H11.5M21 9.5H16M15.5548 16.8151C16.7829 16.8151 17.9493 16.5506 19 16.0754C17.6867 18.9794 14.7642 21 11.3698 21C6.74731 21 3 17.2527 3 12.6302C3 9.23576 5.02061 6.31331 7.92462 5C7.44944 6.05072 7.18492 7.21708 7.18492 8.44523C7.18492 13.0678 10.9322 16.8151 15.5548 16.8151Z"
              stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </template>
      </button-with-tooltip>

    </div>
    <div class="flex items-center space-x-2 lg:hidden">
      <button @click="toggleMobileMenu">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="w-6" fill="currentColor">
          <path
            d="M495.9 166.6c3.2 8.7 .5 18.4-6.4 24.6l-43.3 39.4c1.1 8.3 1.7 16.8 1.7 25.4s-.6 17.1-1.7 25.4l43.3 39.4c6.9 6.2 9.6 15.9 6.4 24.6c-4.4 11.9-9.7 23.3-15.8 34.3l-4.7 8.1c-6.6 11-14 21.4-22.1 31.2c-5.9 7.2-15.7 9.6-24.5 6.8l-55.7-17.7c-13.4 10.3-28.2 18.9-44 25.4l-12.5 57.1c-2 9.1-9 16.3-18.2 17.8c-13.8 2.3-28 3.5-42.5 3.5s-28.7-1.2-42.5-3.5c-9.2-1.5-16.2-8.7-18.2-17.8l-12.5-57.1c-15.8-6.5-30.6-15.1-44-25.4L83.1 425.9c-8.8 2.8-18.6 .3-24.5-6.8c-8.1-9.8-15.5-20.2-22.1-31.2l-4.7-8.1c-6.1-11-11.4-22.4-15.8-34.3c-3.2-8.7-.5-18.4 6.4-24.6l43.3-39.4C64.6 273.1 64 264.6 64 256s.6-17.1 1.7-25.4L22.4 191.2c-6.9-6.2-9.6-15.9-6.4-24.6c4.4-11.9 9.7-23.3 15.8-34.3l4.7-8.1c6.6-11 14-21.4 22.1-31.2c5.9-7.2 15.7-9.6 24.5-6.8l55.7 17.7c13.4-10.3 28.2-18.9 44-25.4l12.5-57.1c2-9.1 9-16.3 18.2-17.8C227.3 1.2 241.5 0 256 0s28.7 1.2 42.5 3.5c9.2 1.5 16.2 8.7 18.2 17.8l12.5 57.1c15.8 6.5 30.6 15.1 44 25.4l55.7-17.7c8.8-2.8 18.6-.3 24.5 6.8c8.1 9.8 15.5 20.2 22.1 31.2l4.7 8.1c6.1 11 11.4 22.4 15.8 34.3zM256 336c44.2 0 80-35.8 80-80s-35.8-80-80-80s-80 35.8-80 80s35.8 80 80 80z" />
        </svg>
      </button>
      <transition name="fade-scale" @before-enter="el => (el.style.display = 'block')"
        @after-leave="el => (el.style.display = 'none')">
        <div v-show="isMobileMenuOpen"
          class="absolute overflow-y-auto top-16 right-0 space-y-4 p-4 z-10 mt-2 w-56 max-h-[40vh] origin-top-right rounded-md border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#171131ef] shadow-lg ring-1 ring-white dark:ring-gray-800 ring-opacity-5">
          <button v-if="role === 'root' && enableDumper" class="flex items-center space-x-2 w-full"
            @click="openModalWrap('Umumy import', 'Maglumat gorundaky ähli maglumatlaryň importyny tassyklaýarsyňyzmy?', getDumpFile)">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6" viewBox="0 0 24 24" fill="none">
              <path
                d="M16.9999 19C19.209 19 20.9999 17.2091 20.9999 15C20.9999 12.7909 19.209 11 16.9999 11H16.9774C16.9923 10.8353 16.9999 10.6685 16.9999 10.5C16.9999 7.46243 14.5374 5 11.4999 5C8.4623 5 5.99986 7.46243 5.99986 10.5C5.99986 10.5047 5.99987 10.5095 5.99988 10.5142C4.04366 10.9113 2.57129 12.6408 2.57129 14.7142C2.57129 17.0811 4.49007 18.9999 6.857 18.9999"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              <path d="M12 14L12 19M12 19L14 17M12 19L10 17" stroke="currentColor" stroke-width="2"
                stroke-linecap="round" stroke-linejoin="round" />
            </svg>
            <p>
              Umumy import
            </p>
          </button>
          <button class="flex items-center space-x-2 w-full" @click="emit('toggle-theme')">
            <svg viewBox="0 0 24 24" class="w-6 h-6" :class="{ hidden: isDark }" fill="none"
              xmlns="http://www.w3.org/2000/svg">
              <path
                d="M11 1C11 0.447715 11.4477 0 12 0C12.5523 0 13 0.447715 13 1V3C13 3.55228 12.5523 4 12 4C11.4477 4 11 3.55228 11 3V1Z"
                fill="currentColor" />
              <path fill-rule="evenodd" clip-rule="evenodd"
                d="M18 12C18 15.3137 15.3137 18 12 18C8.68629 18 6 15.3137 6 12C6 8.68629 8.68629 6 12 6C15.3137 6 18 8.68629 18 12ZM8.06167 12C8.06167 14.1751 9.82492 15.9383 12 15.9383C14.1751 15.9383 15.9383 14.1751 15.9383 12C15.9383 9.82492 14.1751 8.06167 12 8.06167C9.82492 8.06167 8.06167 9.82492 8.06167 12Z"
                fill="currentColor" />
              <path
                d="M20.4853 3.51472C20.0947 3.12419 19.4616 3.12419 19.0711 3.51472L17.6568 4.92893C17.2663 5.31946 17.2663 5.95262 17.6568 6.34315C18.0474 6.73367 18.6805 6.73367 19.0711 6.34315L20.4853 4.92893C20.8758 4.53841 20.8758 3.90524 20.4853 3.51472Z"
                fill="currentColor" />
              <path
                d="M1 13C0.447715 13 0 12.5523 0 12C0 11.4477 0.447715 11 1 11H3C3.55228 11 4 11.4477 4 12C4 12.5523 3.55228 13 3 13H1Z"
                fill="currentColor" />
              <path
                d="M3.51472 3.51472C3.1242 3.90524 3.1242 4.53841 3.51472 4.92893L4.92894 6.34315C5.31946 6.73367 5.95263 6.73367 6.34315 6.34315C6.73368 5.95262 6.73368 5.31946 6.34315 4.92893L4.92894 3.51472C4.53841 3.12419 3.90525 3.12419 3.51472 3.51472Z"
                fill="currentColor" />
              <path
                d="M11 21C11 20.4477 11.4477 20 12 20C12.5523 20 13 20.4477 13 21V23C13 23.5523 12.5523 24 12 24C11.4477 24 11 23.5523 11 23V21Z"
                fill="currentColor" />
              <path
                d="M6.34315 17.6569C5.95263 17.2663 5.31946 17.2663 4.92894 17.6569L3.51473 19.0711C3.1242 19.4616 3.1242 20.0948 3.51473 20.4853C3.90525 20.8758 4.53842 20.8758 4.92894 20.4853L6.34315 19.0711C6.73368 18.6805 6.73368 18.0474 6.34315 17.6569Z"
                fill="currentColor" />
              <path
                d="M21 13C20.4477 13 20 12.5523 20 12C20 11.4477 20.4477 11 21 11H23C23.5523 11 24 11.4477 24 12C24 12.5523 23.5523 13 23 13H21Z"
                fill="currentColor" />
              <path
                d="M17.6568 17.6569C17.2663 18.0474 17.2663 18.6805 17.6568 19.0711L19.0711 20.4853C19.4616 20.8758 20.0947 20.8758 20.4853 20.4853C20.8758 20.0948 20.8758 19.4616 20.4853 19.0711L19.0711 17.6569C18.6805 17.2663 18.0474 17.2663 17.6568 17.6569Z"
                fill="currentColor" />
            </svg>
            <svg viewBox="0 0 24 24" class="w-6 h-6" :class="{ hidden: !isDark }" fill="none"
              xmlns="http://www.w3.org/2000/svg">
              <path
                d="M13 6V3M18.5 12V7M14.5 4.5H11.5M21 9.5H16M15.5548 16.8151C16.7829 16.8151 17.9493 16.5506 19 16.0754C17.6867 18.9794 14.7642 21 11.3698 21C6.74731 21 3 17.2527 3 12.6302C3 9.23576 5.02061 6.31331 7.92462 5C7.44944 6.05072 7.18492 7.21708 7.18492 8.44523C7.18492 13.0678 10.9322 16.8151 15.5548 16.8151Z"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
            <p>
              {{ isDark ? 'Garaňky tema' : 'Ýagty tema' }}
            </p>
          </button>

        </div>
      </transition>
    </div>

    <div v-if="role === 'root'">
      <confirm-modal :is-open="isModalOpen" @close="isModalOpen = false;" @submit="submitModal(submitFunction)"
        :header="header" :context='context'></confirm-modal>
    </div>
  </div>
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
</style>
