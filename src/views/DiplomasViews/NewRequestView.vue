<script setup>
import { Form, Field } from 'vee-validate';
import TheSpinner from '@/components/TheSpinner.vue';
import * as Yup from 'yup';
import TheBreadcrumb from '@/components/TheBreadcrumb.vue';
import { useDiplomasStore } from '@/stores/api.store';
import { storeToRefs } from 'pinia';
import { onBeforeMount, computed, ref, onMounted, watch } from 'vue';
import router from '@/router';

const diplomasStore = useDiplomasStore();
const { diplomaRequestAdvanced } = storeToRefs(diplomasStore);

const breadcrumbPaths = [
  { path: "/diplomas", name: "Diplomlar" },
  { path: "/diplomas/new-request", name: "Hasabaty täzelemek", current: true }
];

const simpleDiplomaCount = ref(0);
const honorDiplomaCount = ref(0);
const twoYearWorkOff = ref(0);
const died = ref(0);
const wentAbroad = ref(0);
const otherReasons = ref(0);

let allowedUntil = 0;
let now = 0;

onBeforeMount(() => {
  diplomasStore.getDiplomaRequestAdvanced().then(() => {
    if (!diplomaRequestAdvanced.value.null) {
      allowedUntil = new Date(diplomaRequestAdvanced.value.allowed_until).getTime();
      now = new Date().getTime()
    }
    if (!(diplomaRequestAdvanced.value.verdict === "C") || (allowedUntil <= now)) {
      router.push('/diplomas');
    }
  })
})



const schema = Yup.object().shape({
  simple_diploma_count: Yup.number().typeError('Adaty diplom sany hökman girizilmeli').min(0, "San otrisatel bolup bilmez").required('Adaty diplom sany hökman girizilmeli'),
  honor_diploma_count: Yup.number().typeError('"Tapawutlanan" diplom sany hökman girizilmeli').min(0, "San otrisatel bolup bilmez").required('"Tapawutlanan" diplom sany hökman girizilmeli'),
  two_year_work_off: Yup.number().typeError('Meýdança boş bolup bilmez').min(0, "San otrisatel bolup bilmez").required('Meýdança boş bolup bilmez'),
  died: Yup.number().typeError('Meýdança boş bolup bilmez').min(0, "San otrisatel bolup bilmez").required('Meýdança boş bolup bilmez'),
  went_abroad: Yup.number().typeError('Meýdança boş bolup bilmez').min(0, "San otrisatel bolup bilmez").required('Meýdança boş bolup bilmez'),
  other_reasons: Yup.number().typeError('Meýdança boş bolup bilmez').min(0, "San otrisatel bolup bilmez").required('Meýdança boş bolup bilmez'),
});

function onSubmit(values, { setErrors }) {
  const { simple_diploma_count, honor_diploma_count, two_year_work_off, died, went_abroad, other_reasons } = values;
  return diplomasStore.update(diplomaRequestAdvanced.value.id, { simple_diploma_count, honor_diploma_count, two_year_work_off, died, went_abroad, other_reasons }).then(() => {
    router.push('/diplomas');
  })
    .catch(error => setErrors({ apiError: error }));
}

const currentDiplomasQuantity = computed(() => {
  return diplomaRequestAdvanced.value.spare_diplomas + (simpleDiplomaCount.value ? simpleDiplomaCount.value : 0) + (honorDiplomaCount.value ? honorDiplomaCount.value : 0)
})

const currentSpareDiplomasQuantity = computed(() => {
  return currentDiplomasQuantity.value - (twoYearWorkOff.value ? twoYearWorkOff.value : 0) - (died.value ? died.value : 0) - (wentAbroad.value ? wentAbroad.value : 0) - (otherReasons.value ? otherReasons.value : 0)
})



</script>

<template>
  <the-breadcrumb :paths="breadcrumbPaths"></the-breadcrumb>

  <div class="tile">
    <h3 class="text-xl font-bold mx-2 select-none">Täze diplom talap etmek</h3>
    <Form @submit="onSubmit" :validation-schema="schema" v-slot="{ errors, isSubmitting }"
      :initial-values="{ simple_diploma_count: 0, honor_diploma_count: 0, two_year_work_off: 0, died: 0, went_abroad: 0, other_reasons: 0 }"
      class="space-y-4 my-4">
      <div class="w-full">
        <label class="info-label" for="simple-diploma-count">Adaty diplom sany</label>
        <Field name="simple_diploma_count" type="number" id="simple-diploma-count" v-model.number="simpleDiplomaCount"
          class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
          :class="{ 'is-invalid': errors.simple_diploma_count }" placeholder="Adaty diplom sany"></Field>
        <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.simple_diploma_count }}
        </div>
      </div>
      <div class="w-full">
        <label class="info-label" for="honor-diploma-count">"Tapawutlanan" diplom sany</label>
        <Field name="honor_diploma_count" type="number" id="honor-diploma-count" v-model.number="honorDiplomaCount"
          class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
          :class="{ 'is-invalid': errors.honor_diploma_count }" placeholder='"Tapawutlanan" diplom sany'></Field>
        <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.honor_diploma_count }}
        </div>
      </div>
      <p class="text-center md:text-end select-none mx-2">Diplom sany: {{ currentDiplomasQuantity }}
      </p>
      <h3 class="text-xl font-bold mx-2 select-none">Diplom sebäpleri</h3>
      <div class="w-full grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="info-label" for="two-year-work-off">Iki ýyl iş</label>
          <Field name="two_year_work_off" type="number" id="two-year-work-off" v-model.number="twoYearWorkOff"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.two_year_work_off }" placeholder="Iki ýyl iş"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.two_year_work_off }}
          </div>
        </div>
        <div>
          <label class="info-label" for="died">Ýogalan</label>
          <Field name="died" type="number" id="died" v-model.number="died"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.died }" placeholder="Ýogalan"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.died }}
          </div>
        </div>
        <div>
          <label class="info-label" for="went-abroad">Daşary ýurda giden</label>
          <Field name="went_abroad" type="number" id="went-abroad" v-model.number="wentAbroad"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.went_abroad }" placeholder="Daşary ýurda giden"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.went_abroad }}
          </div>
        </div>
        <div>
          <label class="info-label" for="other-reasons">Gaýry sebäpler</label>
          <Field name="other_reasons" type="number" id="other-reasons" v-model.number="otherReasons"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.other_reasons }" placeholder="Gaýry sebäpler"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.other_reasons }}
          </div>
        </div>
      </div>
      <p class="text-center md:text-end select-none mx-2" :class="{ 'text-red-500': currentSpareDiplomasQuantity < 0 }"
        :title="currentSpareDiplomasQuantity < 0 ? 'Diplom sany ýeterlik däl' : ''">
        Ätiýaçdaky diplom sany: {{ currentSpareDiplomasQuantity }}
      </p>
      <div class="flex flex-wrap justify-center md:justify-end items-center">

        <button :disabled="isSubmitting"
          class="flex w-50 px-4 py-2 my-2 justify-center rounded-lg border-none dark:border-violet-500/50 border-1 bg-gradient-to-r from-blue-400 to-blue-500 dark:from-violet-600 dark:to-violet-500 text-white hover:shadow-lg hover:shadow-blue-300/50 hover:ease-in ease-out duration-200 dark:hover:shadow-violet-500/50 select-none">
          <the-spinner :class="{ hidden: !isSubmitting }"></the-spinner>
          <span :class="{ hidden: isSubmitting }">Hasaba al</span>
        </button>
      </div>
      <div v-if="errors.apiError" class="text-center text-red-500 mt-3 mb-0 text-sm select-none">{{
        errors.apiError
      }}
      </div>
    </Form>
  </div>
</template>
