<template>
  <the-breadcrumb :paths="breadcrumbPaths">
  </the-breadcrumb>
  <div class="w-full rounded-lg shadow-lg p-4 bg-white dark:bg-[#171131ef]">
    <h3 class="text-xl font-bold mx-2 select-none">Hünäri üýtgetmek</h3>
    <Form :initial-values="{ classificator: 0, degree: 0 }" @submit="onSubmit" :validation-schema="schema"
          v-slot="{ errors, isSubmitting }" class="space-y-4 my-4">
      <div class="grid lg:grid-cols-3 md:grid-cols-3 sm:grid-cols-1 gap-4">
        <div class="lg:col-span-2 md:col-span-2 lg:col-span-1">
          <Field name="name" type="text" id="name" v-model="specializationName"
                 class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
                 :class="{ 'is-invalid': errors.name }"
                 placeholder="Hünäriň ady"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.name }}
          </div>
        </div>
        <div>
          <Field name="abbreviation" type="text" id="abbreviation" v-model="specializationAbbreviation"
                 class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
                 :class="{ 'is-invalid': errors.abbreviation }"
                 placeholder="Hünäriň gysgaltmasy"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.abbreviation }}
          </div>
        </div>
      </div>
      <div class="grid lg:grid-cols-2 md:grid-cols-2 sm:grid-cols-1 gap-4">
        <div>
          <label for="classificator" class="block mb-1 select-none">Klassifikatory</label>
          <Field
            as="select"
            name="classificator"
            id="classificator"
            class="w-full border border-gray-300 dark:border-gray-700 rounded-md p-2 focus:outline-none select-none"
            v-model="specializationClassificator"
          >
            <option :value="0" class="text-gray-600 dark:bg-[#171131ef] dark:text-white">Saýlanmadyk</option>
            <option class="text-gray-600 dark:bg-[#171131ef] dark:text-white" v-for="classificator in classificators"
                    :value="classificator.id">{{ classificator.name }}
            </option>
          </Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.classificator }}
          </div>
        </div>
        <div>
          <label for="degree" class="block mb-1 select-none">Hünär derejesi</label>
          <Field
            as="select"
            name="degree"
            id="degree"
            class="w-full border border-gray-300 dark:border-gray-700 rounded-md p-2 focus:outline-none select-none"
            v-model="specializationDegree"
          >
            <option class="text-gray-600 dark:bg-[#171131ef] dark:text-white" v-for="degree in degrees"
                    :value="degree.id">{{ degree.name }} ({{ degree.duration }} ýyl)
            </option>
          </Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.degree }}
          </div>
        </div>
      </div>
      <div class="flex flex-wrap justify-center md:justify-end lg:justify-end">
        <button :disabled="isSubmitting"
                class="flex w-50 px-4 py-2 my-2 justify-center rounded-lg border-none dark:border-violet-500/50 border-1 bg-gradient-to-r from-blue-400 to-blue-500 dark:from-violet-600 dark:to-violet-500 text-white hover:shadow-lg hover:shadow-blue-300/50 hover:ease-in ease-out duration-200 dark:hover:shadow-violet-500/50 select-none">
          <the-spinner :class="{ hidden: !isSubmitting }"></the-spinner>
          <span :class="{ hidden: isSubmitting }">Hasaba al</span>
        </button>
      </div>
      <div v-if="errors.apiError" class="text-center text-red-500 mt-3 mb-0 text-sm select-none">{{ errors.apiError }}</div>
    </Form>
  </div>

</template>

<script setup>

import TheSpinner from "@/components/TheSpinner.vue";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import {Field, Form} from "vee-validate";
import * as Yup from 'yup';
import {useClassificatorsStore, useDegreesStore, useSpecializationsStore} from "@/stores/api.store.js";
import router from "@/router/index.js";
import {onMounted, ref} from "vue";
import {storeToRefs} from "pinia";
import {useRoute} from "vue-router";

const specializationsStore = useSpecializationsStore();
const classificatorsStore = useClassificatorsStore();
const degreesStore = useDegreesStore();

const {classificators} = storeToRefs(classificatorsStore);
const {degrees} = storeToRefs(degreesStore);

const specializationName = ref('');
const specializationAbbreviation = ref('');
const specializationClassificator = ref(0);
const specializationDegree = ref(0);

const route = useRoute();

const schema = Yup.object().shape({
  name: Yup.string().trim().required('Hünariň ady hökman girizilmeli'),
  abbreviation: Yup.string().trim().required('Hünäriň gysgaltmasy hökman girizilmeli'),
  classificator: Yup.number(),
  degree: Yup.number().required('Hünär derejesini saýlaň').notOneOf([0], 'Hünär derejesi hökman saýlanylmaly'),
});

function onSubmit(values, {setErrors}) {
  const {name, abbreviation, classificator, degree} = values;
  return specializationsStore.put(route.params.id, {name, abbreviation, classificator, degree}).then(() => {
      router.go(-1);
    }
  )
    .catch(error => setErrors({apiError: error}));
}

onMounted(() => {
  specializationsStore.get(route.params.id).then(() => {
    specializationName.value = specializationsStore.specialization.name;
    specializationAbbreviation.value = specializationsStore.specialization.abbreviation;
    if (specializationsStore.specialization.classificator) {
      specializationClassificator.value = specializationsStore.specialization.classificator;
    }
    specializationDegree.value = specializationsStore.specialization.degree;
  });
  degreesStore.getAll();
  classificatorsStore.getAll();
});

const breadcrumbPaths = [
  {path: "/specializations", name: "Hünärler"},
  {path: "/specializations/add", name: "Üýtgetmek", current: true},
]
</script>
