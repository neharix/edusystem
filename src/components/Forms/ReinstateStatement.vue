<script setup>
import * as Yup from 'yup';
import { useReinstateRequestsStore } from "@/stores/api.store";
import { useAuthStore } from '@/stores/auth.store';
import { Field, Form } from "vee-validate";
import TheSpinner from "@/components/TheSpinner.vue";
import { useRoute } from "vue-router";
import router from "@/router/index.js";
import { storeToRefs } from 'pinia';

const route = useRoute()
const reinstateRequestsStore = useReinstateRequestsStore();

const authStore = useAuthStore();
const { user } = storeToRefs(authStore);


const schema = Yup.object().shape({
  detail: Yup.string().trim().required('Bellik, buýruk nomer,senesi hökmän görkezilmeli'),
});

function onSubmit(values, { setErrors }) {
  const { detail } = values;
  return reinstateRequestsStore.create({ student: route.params.id, sender: user.value.id, detail }).then(() => {
    router.push("/expelled-students");
  }).catch(error => setErrors({ apiError: error }));
}


</script>
<template>
  <div class="tile my-8">
    <h3 class="text-xl font-bold mx-2 select-none">Talybyň okuwyny dikeltmek barada arza</h3>
    <Form @submit="onSubmit" :validation-schema="schema" v-slot="{ errors, isSubmitting }" class="space-y-4 my-4">
      <div>
        <label for="detail" class="info-label">Okuwyny dikeltmek barada maglumat</label>
        <Field as="textarea" rows="1" name="detail" type="text" id="detail"
          class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
          :class="{ 'is-invalid': errors.detail }"></Field>
        <div class="invalid-feedback select-none text-red-500 mb-2 mx-2 text-sm">{{ errors.detail }}
        </div>
      </div>
      <div class="flex flex-wrap justify-center md:justify-end lg:justify-end">
        <button :disabled="isSubmitting"
          class="flex w-50 px-4 py-2 my-2 justify-center rounded-lg border-none dark:border-violet-500/50 border-1 bg-gradient-to-r from-blue-400 to-blue-500 dark:from-violet-600 dark:to-violet-500 text-white hover:shadow-lg hover:shadow-blue-300/50 hover:ease-in ease-out duration-200 dark:hover:shadow-violet-500/50">
          <the-spinner :class="{ hidden: !isSubmitting }"></the-spinner>
          <span :class="{ hidden: isSubmitting }">Okuwyny dikeltmek</span>
        </button>
      </div>
      <div v-if="errors.apiError" class="text-center text-red-500 mt-3 mb-0 text-sm select-none">{{
        errors.apiError
        }}
      </div>
    </Form>
  </div>
</template>
