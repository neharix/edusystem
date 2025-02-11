<template>
  <the-breadcrumb :paths="breadcrumbPaths"></the-breadcrumb>
  <div class="w-full rounded-lg shadow-lg p-4 bg-white dark:bg-[#171131ef]">
    <h3 class="text-xl font-bold mx-2 select-none">Kafedrany üýtgetmek</h3>
    <Form @submit="onSubmit" :validation-schema="schema" v-slot="{ errors, isSubmitting }" class="space-y-4 my-4">
      <div class="grid lg:grid-cols-3 md:grid-cols-3 sm:grid-cols-1 gap-4">
        <div class="lg:col-span-2 md:col-span-2 lg:col-span-1">
          <Field name="name" type="text" id="name" v-model="departmentName"
                 class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
                 :class="{ 'is-invalid': errors.name }"
                 placeholder="Kafedranyň ady"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.name }}
          </div>
        </div>
        <div>
          <Field name="abbreviation" type="text" id="abbreviation" v-model="departmentAbbreviation"
                 class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
                 :class="{ 'is-invalid': errors.abbreviation }"
                 placeholder="Kafedranyň gysgaltmasy"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.abbreviation }}
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
import {Field, Form} from "vee-validate";
import * as Yup from 'yup';
import {useDepartmentsStore} from "@/stores/api.store.js";
import {useRoute} from "vue-router";
import router from "@/router/index.js";
import {onMounted, ref} from "vue";

const route = useRoute();

const departmentsStore = useDepartmentsStore();

const departmentName = ref('');
const departmentAbbreviation = ref('');




const schema = Yup.object().shape({
  name: Yup.string().trim().required('Kafedranyň ady hökman girizilmeli'),
  abbreviation: Yup.string().trim().required('Kafedranyň gysgaltmasy hökman girizilmeli'),
});

function onSubmit(values, {setErrors}) {
  const {name, abbreviation} = values;
  return departmentsStore.put(route.params.id, {name, abbreviation}).then(() => {
    router.go(-1);
  }).catch(error => setErrors({apiError: error}));
};


const breadcrumbPaths = [
  {path: "/departments", name: "Kafedralar"},
  {path: "/departments/edit", name: "Üýtgetmek"},
]

onMounted(() => {
  departmentsStore.get(route.params.id).then(() => {
    departmentName.value = departmentsStore.department.name;
    departmentAbbreviation.value = departmentsStore.department.abbreviation;
  })
})


</script>
