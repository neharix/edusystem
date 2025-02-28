<script setup>
import { Form, Field } from 'vee-validate';
import TheSpinner from '@/components/TheSpinner.vue';
import * as Yup from 'yup';
import TheBreadcrumb from '@/components/TheBreadcrumb.vue';
import { useDiplomasStore } from '@/stores/api.store';
import router from '@/router';
import { onBeforeMount, ref, computed } from 'vue';
import { storeToRefs } from 'pinia';


const diplomasStore = useDiplomasStore();
const { diplomaRequestAdvanced } = storeToRefs(diplomasStore)

const breadcrumbPaths = [
  { path: "/diplomas", name: "Diplomlar" },
  { path: "/diplomas/add", name: "Hasabat döretmek" }
];


const simpleDiplomaCount = ref(0);
const honorDiplomaCount = ref(0)


const schema = Yup.object().shape({
  simple_diploma_count: Yup.number().typeError('Adaty diplom sany hökman girizilmeli').min(0, "San otrisatel bolup bilmez").required('Adaty diplom sany hökman girizilmeli'),
  honor_diploma_count: Yup.number().typeError('"Tapawutlanan" diplom sany hökman girizilmeli').min(0, "San otrisatel bolup bilmez").required('"Tapawutlanan" diplom sany hökman girizilmeli'),
});

onBeforeMount(() => {
  diplomasStore.getDiplomaRequestAdvanced().then(() => {
    if (!(diplomaRequestAdvanced.value.null)) {
      router.push('/diplomas');
    }
  })
})

function onSubmit(values, { setErrors }) {
  const { simple_diploma_count, honor_diploma_count } = values;
  return diplomasStore.create({ simple_diploma_count, honor_diploma_count }).then(() => {
    router.push('/diplomas');
  })
    .catch(error => setErrors({ apiError: error }));
}


const diplomasQuantity = computed(() => {
  return (simpleDiplomaCount.value ? simpleDiplomaCount.value : 0) + (honorDiplomaCount.value ? honorDiplomaCount.value : 0)
})

</script>
<template>
  <the-breadcrumb :paths="breadcrumbPaths"></the-breadcrumb>

  <div class="tile">
    <h3 class="text-xl font-bold mx-2 select-none">Täze diplom hasabatyny hasaba almak</h3>
    <Form @submit="onSubmit" :validation-schema="schema" v-slot="{ errors, isSubmitting, values }"
      :initial-values="{ simple_diploma_count: 0, honor_diploma_count: 0 }" class="space-y-4 my-4">
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

      <div class="block md:hidden">
        <p class="text-center select-none">Diplom sany: {{ diplomasQuantity }}
        </p>
      </div>
      <div class="flex flex-wrap justify-center md:justify-end items-center">
        <p class="mr-8 text-center hidden md:block select-none">Diplom sany: {{ diplomasQuantity }}
        </p>
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
