<script setup>
import GridCell from '@/components/GridCell.vue';
import { useDiplomasStore } from '@/stores/api.store';
import { storeToRefs } from 'pinia';
import { onBeforeMount, watch, ref } from 'vue';
import { Field, Form } from "vee-validate";
import * as Yup from 'yup';
import TheToast from "@/components/TheToast.vue";
import useToast from "@/use/useToast.js";
import { useRoute } from 'vue-router';
import TheBreadcrumb from '@/components/TheBreadcrumb.vue';
import HighSchoolDiplomaReportsDataTable from '@/components/DataTables/HighSchoolDiplomaReportsDataTable.vue';
import HighSchoolDiplomaActionsDataTable from '@/components/DataTables/HighSchoolDiplomaActionsDataTable.vue';
import VerdictBtnsGroup from '@/components/VerdictBtnsGroup.vue';
import { useAuthStore } from '@/stores/auth.store';
import TheSpinner from '@/components/TheSpinner.vue';

const route = useRoute();

const { toasts, addToast } = useToast();

const authStore = useAuthStore()
const diplomasStore = useDiplomasStore();
const { diplomaRequestAdvanced, highSchoolDiplomaActions, submitStatus, updateStatus } = storeToRefs(diplomasStore);

const allowingDate = ref(null);

const schema = Yup.object().shape({
  allowed_until: Yup.date(),
});



onBeforeMount(() => {
  diplomasStore.getDiplomaRequestAdvancedById(route.params.id).then(() => {
    let allowingDt = new Date(diplomaRequestAdvanced.value.allowed_until);
    allowingDt.setHours(allowingDt.getHours() + 5);
    allowingDate.value = allowingDt.toISOString().slice(0, 16)
    console.log(allowingDate.value)
  });
  diplomasStore.getHighSchoolActions(route.params.id);
  authStore.fetchUser()
})


function update() {
  diplomasStore.getDiplomaRequestAdvancedById(route.params.id);
  diplomasStore.getHighSchoolActions(route.params.id);
}

function onSubmit(values, { setErrors }) {
  const { allowed_until } = values;
  return diplomasStore.put(route.params.id, { allowed_until }).catch(error => setErrors({ apiError: error }));
}

watch(submitStatus, (newVal) => {
  if (submitStatus.value) {
    if (submitStatus.value === 'success') {
      addToast('Hasabat üstünlikli tassyklandy', 'success');
    } else if (submitStatus.value === 'error') {
      addToast('Tassyklama prosesinde ýalňyşlyk ýüze çykdy', 'error');
    }
  }
  submitStatus.value = null;
})

watch(updateStatus, (newVal, oldVal) => {
  if (newVal) {
    if (newVal === 'success') {
      addToast('Hasabat üstünlikli üýtgedildi', 'success');
    } else if (newVal === 'error') {
      addToast('Üýtgetme prosesinde ýalňyşlyk ýüze çykdy', 'error');
    }
  }
  updateStatus.value = null;
})


function giveVerdict(id, verdict) {
  diplomasStore.giveVerdictDiplomaRequest(id, verdict).then(() => {
    update();
  });
}


async function markAsUnviewed() {
  await diplomasStore.markAsUnviewed(route.params.id);
  authStore.fetchUser()
  diplomasStore.getDiplomaRequestAdvancedById(route.params.id);
}


const breadcrumbPaths = [
  { path: "/diplomas", name: "Diplomlar" },
  { path: "/diplomas/view", name: "Görmek", current: true },
]

</script>
<template>
  <the-breadcrumb :paths="breadcrumbPaths"></the-breadcrumb>
  <div class="grid md:grid-cols-4 sm:grid-cols-2 gap-8">
    <grid-cell label="Başdaky talap edilen diplom sany" :custom-classes="'md:col-span-2 sm:col-span-1'"
      :data-value="diplomaRequestAdvanced.original_requested_quantity"
      icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_901_948)">
          <path
            d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        <defs>
          <clipPath id="clip0_901_948">
            <rect width="32" height="32" fill="white" />
          </clipPath>
        </defs>
      </svg>
    </grid-cell>
    <div
      class="bg-white dark:bg-[#171131ef] shadow-md rounded-lg flex justify-between items-center p-4 md:col-span-2 sm:col-span-1">
      <div>
        <div class="text-sm my-2 select-none">
          Umumy talap edilen diplom sany
        </div>

        <div class="mt-2 select-none font-bold text-lg"
          v-if="diplomaRequestAdvanced.original_requested_quantity === diplomaRequestAdvanced.total_requested_quantity">
          {{ diplomaRequestAdvanced.total_requested_quantity }}
        </div>
        <div class="mt-2 select-none" v-else><span class="text-base">{{
          diplomaRequestAdvanced.original_requested_quantity }} +
            {{
              diplomaRequestAdvanced.total_requested_quantity - diplomaRequestAdvanced.original_requested_quantity
            }} = </span><span class="font-bold text-lg">{{ diplomaRequestAdvanced.total_requested_quantity
            }}</span></div>
      </div>
      <div>
        <div class="w-12 h-12 rounded-full flex justify-center items-center bg-green-200 dark:bg-green-500/75">
          <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
            xmlns="http://www.w3.org/2000/svg">
            <g clip-path="url(#clip0_901_948)">
              <path
                d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
                stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            </g>
            <defs>
              <clipPath id="clip0_901_948">
                <rect width="32" height="32" fill="white" />
              </clipPath>
            </defs>
          </svg>
        </div>
      </div>
    </div>
    <grid-cell label='"Tapawutlanan" diplom sany' :custom-classes="'md:col-span-2 sm:col-span-1'"
      :data-value="diplomaRequestAdvanced.honor_diplomas_quantity" icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_901_948)">
          <path
            d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        <defs>
          <clipPath id="clip0_901_948">
            <rect width="32" height="32" fill="white" />
          </clipPath>
        </defs>
      </svg>
    </grid-cell>
    <grid-cell label="Adaty diplom sany" :custom-classes="'md:col-span-2 sm:col-span-1'"
      :data-value="diplomaRequestAdvanced.simple_diplomas_quantity" icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_901_948)">
          <path
            d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        <defs>
          <clipPath id="clip0_901_948">
            <rect width="32" height="32" fill="white" />
          </clipPath>
        </defs>
      </svg>
    </grid-cell>
    <grid-cell label="Iki ýyl iş" :data-value="diplomaRequestAdvanced.two_year_work_off"
      icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_901_948)">
          <path
            d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        <defs>
          <clipPath id="clip0_901_948">
            <rect width="32" height="32" fill="white" />
          </clipPath>
        </defs>
      </svg>
    </grid-cell>
    <grid-cell label="Ýogalan" :data-value="diplomaRequestAdvanced.died"
      icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_901_948)">
          <path
            d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        <defs>
          <clipPath id="clip0_901_948">
            <rect width="32" height="32" fill="white" />
          </clipPath>
        </defs>
      </svg>
    </grid-cell>
    <grid-cell label="Daşary ýurda giden" :data-value="diplomaRequestAdvanced.went_abroad"
      icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_901_948)">
          <path
            d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        <defs>
          <clipPath id="clip0_901_948">
            <rect width="32" height="32" fill="white" />
          </clipPath>
        </defs>
      </svg>
    </grid-cell>
    <grid-cell label="Gaýry sebäpler" :data-value="diplomaRequestAdvanced.other_reasons"
      icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_901_948)">
          <path
            d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        <defs>
          <clipPath id="clip0_901_948">
            <rect width="32" height="32" fill="white" />
          </clipPath>
        </defs>
      </svg>
    </grid-cell>
    <grid-cell label="Ätiýaçdaky diplomlar" :custom-classes="'md:col-span-2 sm:col-span-1'"
      :data-value="diplomaRequestAdvanced.spare_diplomas" icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_901_948)">
          <path
            d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        <defs>
          <clipPath id="clip0_901_948">
            <rect width="32" height="32" fill="white" />
          </clipPath>
        </defs>
      </svg>
    </grid-cell>
    <div class="tile md:col-span-2 sm:col-span-1">
      <div class="flex justify-between" v-if="!diplomaRequestAdvanced.verdict">
        <verdict-btns-group @submit-click="giveVerdict(route.params.id, 'C')"
          @reject-click="giveVerdict(route.params.id, 'R')"></verdict-btns-group>
        <button title="Okalmadyk ýaly bellemek" @click="markAsUnviewed()"
          class="mt-4 active:scale-80 transition-all duration-300 ease-in-out py-2 select-none text-nowrap px-3 my-2 text-[0.7rem] md:text-sm lg:text-sm rounded-lg shadow-md border-none dark:border-violet-500/50 border-1 bg-blue-500 dark:bg-violet-600 text-white"><svg
            xmlns="http://www.w3.org/2000/svg" class="w-6" viewBox="0 0 24 24">
            <rect width="24" height="24" fill="none" />
            <g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">
              <path d="M22 10.5V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v12c0 1.1.9 2 2 2h12.5" />
              <path d="m22 7l-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7m18 7v4m0 4v.01" />
            </g>
          </svg></button>
      </div>
      <div v-else-if="diplomaRequestAdvanced.verdict === 'C'" class="mt-4 flex justify-between">
        <div>
          <h4
            class="px-4 py-2 text-[0.8rem] w-max font-medium bg-emerald-400 hover:bg-emerald-500 transition ease-in hover:ease-out duration-200 text-white dark:bg-emerald-700 border border-gray-200 dark:border-gray-700 rounded-lg select-none">
            Tassyklanyldy
          </h4>
        </div>
        <button title="Okalmadyk ýaly bellemek" @click="markAsUnviewed()"
          class="active:scale-80 transition-all duration-300 ease-in-out py-2 select-none text-nowrap px-3 my-2 text-[0.7rem] md:text-sm lg:text-sm rounded-lg shadow-md border-none dark:border-violet-500/50 border-1 bg-blue-500 dark:bg-violet-600 text-white"><svg
            xmlns="http://www.w3.org/2000/svg" class="w-6" viewBox="0 0 24 24">
            <rect width="24" height="24" fill="none" />
            <g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">
              <path d="M22 10.5V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v12c0 1.1.9 2 2 2h12.5" />
              <path d="m22 7l-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7m18 7v4m0 4v.01" />
            </g>
          </svg></button>
      </div>
      <div v-else-if="diplomaRequestAdvanced.verdict === 'R'" class="mt-4 flex justify-center">
        <h4
          class="px-4 py-2 text-[0.8rem] w-max font-medium bg-red-400 hover:bg-red-500 transition ease-in hover:ease-out duration-200 text-white dark:bg-pink-900 dark:hover:bg-pink-600 border border-gray-200 rounded-lg  dark:border-gray-700  select-none">
          Ret edildi
        </h4>
      </div>

    </div>
    <div class="tile md:col-span-4 sm:col-span-2">
      <Form @submit="onSubmit" :validation-schema="schema" v-slot="{ errors, isSubmitting }" class="space-y-4 my-4">
        <div>
          <label for="allowingDate" class="info-label">Hasabat kabul ediş möhleti</label>
          <Field name="allowed_until" type="datetime-local" id="allowingDate" v-model="allowingDate"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.birth_date }" placeholder="Doglan senesi"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.allowed_until }}
          </div>
        </div>
        <div class="flex flex-wrap justify-center md:justify-end lg:justify-end">
          <button :disabled="isSubmitting"
            class="flex w-50 px-4 py-2 my-2 justify-center rounded-lg border-none dark:border-violet-500/50 border-1 bg-gradient-to-r from-blue-400 to-blue-500 dark:from-violet-600 dark:to-violet-500 text-white hover:shadow-lg hover:shadow-blue-300/50 hover:ease-in ease-out duration-200 dark:hover:shadow-violet-500/50">
            <the-spinner :class="{ hidden: !isSubmitting }"></the-spinner>
            <span :class="{ hidden: isSubmitting }">Üýtget</span>
          </button>
        </div>
        <div v-if="errors.apiError" class="text-center text-red-500 mt-3 mb-0 text-sm select-none">{{
          errors.apiError
        }}
        </div>
      </Form>
    </div>
  </div>
  <div v-if="diplomaRequestAdvanced.verdict === 'C'">
    <div class="mt-8">
      <high-school-diploma-reports-data-table @update="update"
        :data="highSchoolDiplomaActions.reports"></high-school-diploma-reports-data-table>
    </div>
    <div class="mt-8">
      <high-school-diploma-actions-data-table @update="update"
        :data="highSchoolDiplomaActions.actions"></high-school-diploma-actions-data-table>
    </div>
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
