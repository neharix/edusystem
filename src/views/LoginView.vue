<script setup>
import {Form, Field} from 'vee-validate';
import * as Yup from 'yup';
import TheSpinner from "@/components/TheSpinner.vue";

import {useAuthStore} from '@/stores/auth.store.js';

const PASSWORD_MIN_LENGTH = 8;

const schema = Yup.object().shape({
  username: Yup.string().trim().required('Ulanyjy ady hökmany şekilde girizilmeli'),
  password: Yup.string().required('Açar sözi hökmany şekilde girizilmeli').min(PASSWORD_MIN_LENGTH, `Açar sözi ${PASSWORD_MIN_LENGTH} simwoldan az bolmaly däldir`),
});

function onSubmit(values, {setErrors}) {
  const authStore = useAuthStore();
  const {username, password} = values;
  return authStore.login(username, password)
    .catch(error => setErrors({apiError: error}));
}




</script>

<template>
  <h2 class="text-3xl font-bold text-gray-800 dark:text-gray-100 mb-4 text-center lg:text-left">Hoş geldiňiz! 👋</h2>
  <p class="text-gray-600 dark:text-gray-300 mb-6 text-center lg:text-left">Içeri girmek üçin şahsyňyzy tassyklaň</p>
  <Form @submit="onSubmit" :validation-schema="schema" v-slot="{ errors, isSubmitting }" class="space-y-4">
    <div>
      <label for="username" class="block text-gray-700 dark:text-gray-300 text-sm py-2">Ulanyjy adyňyz</label>
      <Field name="username"
             type="text"
             id="username"
             class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
             :class="{ 'is-invalid': errors.username }"/>
      <div class="invalid-feedback text-red-500 my-2 text-sm">{{ errors.username }}</div>
    </div>
    <div>
      <label for="password" class="block text-gray-700 dark:text-gray-300 text-sm py-2">Açar sözi</label>
      <Field name="password"
             type="password"
             id="password"
             class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
             :class="{ 'is-invalid': errors.password }"/>
      <div class="invalid-feedback text-red-500 my-2 text-sm">{{ errors.password }}</div>

    </div>
    <div class="flex flex-wrap justify-center">
      <button :disabled="isSubmitting"
              class="flex justify-center w-50 px-4 py-2 my-2 rounded-lg border-none dark:border-violet-500/50 border-1 bg-gradient-to-r from-blue-400 to-blue-500 dark:from-violet-600 dark:to-violet-500 text-white hover:shadow-lg hover:shadow-blue-300/50 hover:ease-in ease-out duration-200 dark:hover:shadow-violet-500/50">
          <the-spinner :class="{ hidden: !isSubmitting }"></the-spinner><span :class="{ hidden: isSubmitting }">Giriş</span>
      </button>
    </div>
    <div v-if="errors.apiError" class="text-center text-red-500 mt-3 mb-0 text-sm">{{ errors.apiError }}</div>
  </Form>
</template>

<style scoped>

</style>
