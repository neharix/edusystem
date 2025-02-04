<template>
  <the-breadcrumb :paths="breadcrumbPaths"></the-breadcrumb>
  <div class="w-full rounded-lg shadow-lg p-4 bg-white dark:bg-[#171131ef]">
    <h3 class="text-xl font-bold mx-2 select-none">Ýokary okuw mekdebini üýtgetmek</h3>
    <Form @submit="onSubmit" :validation-schema="schema" v-slot="{ errors, isSubmitting }" class="space-y-4 my-4">
      <div class="grid lg:grid-cols-3 md:grid-cols-3 sm:grid-cols-1 gap-4">
        <div class="lg:col-span-2 md:col-span-2 lg:col-span-1">
          <Field name="high_school_name" type="text" id="high_school_name" v-model="highSchoolName"
                 class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
                 :class="{ 'is-invalid': errors.name }"
                 placeholder="Ýokary okuw mekdebiniň ady"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.name }}
          </div>
        </div>
        <div>
          <Field name="abbreviation" type="text" id="abbreviation" v-model="highSchoolAbbreviation"
                 class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
                 :class="{ 'is-invalid': errors.abbreviation }"
                 placeholder="Ýokary okuw mekdebiniň gysgaltmasy"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.abbreviation }}
          </div>
        </div>
      </div>
      <div class="grid lg:grid-cols-2 md:grid-cols-2 sm:grid-cols-1 gap-4">
        <div>
          <Field name="username" type="text" id="username" v-model="usernameF"
                 class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
                 :class="{ 'is-invalid': errors.username }"
                 placeholder="Ulanyjy ady"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.username }}
          </div>
        </div>
        <div>
          <Field name="password" type="text" id="password" v-model="passwordF"
                 class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
                 :class="{ 'is-invalid': errors.password }"
                 placeholder="Açar sözi"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.password }}
          </div>
        </div>
      </div>
      <div class="flex flex-wrap justify-center md:justify-end lg:justify-end">
        <button :disabled="isSubmitting"
                class="flex w-50 px-4 py-2 my-2 justify-center rounded-lg border-none dark:border-violet-500/50 border-1 bg-gradient-to-r from-blue-400 to-blue-500 dark:from-violet-600 dark:to-violet-500 text-white hover:shadow-lg hover:shadow-blue-300/50 hover:ease-in ease-out duration-200 dark:hover:shadow-violet-500/50">
          <the-spinner :class="{ hidden: !isSubmitting }"></the-spinner>
          <span :class="{ hidden: isSubmitting }">Üýtget</span>
        </button>
      </div>
      <div v-if="errors.apiError" class="text-center text-red-500 mt-3 mb-0 text-sm select-none">{{ errors.apiError }}</div>
    </Form>
  </div>

</template>

<script setup>

import TheSpinner from "@/components/TheSpinner.vue";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import {Field, Form, useForm} from "vee-validate";
import * as Yup from 'yup';
import {useHighSchoolsStore} from "@/stores/api.store.js";
import {useRoute} from "vue-router";
import router from "@/router/index.js";
import {onMounted, ref} from "vue";

const route = useRoute();
const highSchoolsStore = useHighSchoolsStore();

const highSchoolName = ref('');
const highSchoolAbbreviation = ref('');
const usernameF = ref('');
const passwordF = ref('');


const PASSWORD_MIN_LENGTH = 8;


const schema = Yup.object().shape({
  high_school_name: Yup.string().trim().required('Ýokary okuw mekdebiniň ady hökman girizilmeli'),
  abbreviation: Yup.string().trim().required('Ýokary okuw mekdebiniň gysgaltmasy hökman girizilmeli'),
  username: Yup.string().trim().lowercase().required('Ulanyjy ady hökmany şekilde girizilmeli'),
  password: Yup.string().required('Açar sözi hökmany şekilde girizilmeli').min(PASSWORD_MIN_LENGTH, `Açar sözi ${PASSWORD_MIN_LENGTH} simwoldan az bolmaly däldir`),
});

function onSubmit(values, {setErrors}) {
  const {high_school_name, abbreviation, username, password} = values;
  console.log(values);
  return highSchoolsStore.put(route.params.id, {high_school_name, abbreviation, username, password}).then(() => {
    highSchoolsStore.getAllAdditional();
    router.push('/high-schools');
  }).catch(error => setErrors({apiError: error}));
};


const breadcrumbPaths = [
  {path: "/high-schools", name: "Ýokary okuw mekdepleri"},
  {path: "/high-schools/edit/", name: "Üýtgetmek", current: true},
]

onMounted(() => {
  highSchoolsStore.get(route.params.id).then(() => {
    highSchoolName.value = highSchoolsStore.highSchool.name;
    highSchoolAbbreviation.value = highSchoolsStore.highSchool.abbreviation;
    usernameF.value = highSchoolsStore.highSchool.manager.user.username;
    passwordF.value = highSchoolsStore.highSchool.manager.password;
  })
})


</script>
