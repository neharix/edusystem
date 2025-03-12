<script setup>
import { Field, Form } from 'vee-validate';
import * as Yup from 'yup';
import TheSpinner from "@/components/TheSpinner.vue";

import { useAuthStore } from '@/stores/auth.store.js';
import loginImage from "@/assets/svgs/login.svg";
import SiteTools from "@/components/SiteTools.vue";
import { onMounted, ref } from "vue";
import router from "@/router/index.js";
import { useDashboardStore } from '@/stores/api.store';

const dashboardStore = useDashboardStore();

const schema = Yup.object().shape({
  username: Yup.string().trim().required('Ulanyjy ady hökmany şekilde girizilmeli'),
  password: Yup.string().required('Açar sözi hökmany şekilde girizilmeli'),
});

function onSubmit(values, { setErrors }) {
  const authStore = useAuthStore();
  const { username, password } = values;
  return authStore.login({ username, password }).then(() => {
    router.push('/');
  })
    .catch(error => setErrors({ apiError: error }));
}

const isDark = ref(null)


function toggleTheme() {
  const html = document.documentElement;
  const prevTheme = html.classList.contains('dark') ? 'dark' : 'light'
  html.classList.remove(prevTheme)
  html.classList.add(prevTheme === "dark" ? "light" : "dark")

  localStorage.setItem('theme', html.classList.contains('dark') ? 'dark' : 'light');
  const theme = localStorage.getItem("theme");

  html.classList.add(theme)
  html.classList.remove(theme === "dark" ? "light" : "dark")
  isDark.value = theme === "dark";

}


onMounted(() => {
  dashboardStore.clearData();
  const theme = localStorage.getItem("theme")
  isDark.value = theme === "dark"
})


</script>

<template>
  <div class="hidden lg:flex w-2/3 bg-gray-200 dark:bg-[#1b1829] justify-center items-center">
    <img :src="loginImage" alt="Left Section Image" class="max-w-[80%] max-h-[80%] object-contain dark:opacity-75" />
  </div>
  <!-- Right Section (Login Form) -->
  <div class="flex flex-col justify-center px-8 lg:px-16 bg-white dark:bg-[#171131ef] w-full lg:w-1/3">
    <site-tools class="absolute top-5 right-5" :is-dark="isDark" @toggle-theme="toggleTheme"
      :notifications="false"></site-tools>
    <h2 class="text-3xl font-bold text-gray-800 dark:text-gray-100 mb-4 text-center lg:text-left select-none">Hoş
      geldiňiz! 👋</h2>
    <p class="text-gray-600 dark:text-gray-300 mb-6 text-center lg:text-left select-none">Içeri girmek üçin şahsyňyzy
      tassyklaň</p>
    <Form @submit="onSubmit" :validation-schema="schema" v-slot="{ errors, isSubmitting }" class="space-y-4">
      <div>
        <label for="username" class="block text-gray-700 dark:text-gray-300 text-sm py-2 select-none">Ulanyjy
          adyňyz</label>
        <Field name="username" type="text" id="username"
          class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
          :class="{ 'is-invalid': errors.username }" />
        <div class="invalid-feedback text-red-500 my-2 text-sm select-none">{{ errors.username }}</div>
      </div>
      <div>
        <label for="password" class="block text-gray-700 dark:text-gray-300 text-sm py-2 select-none">Açar sözi</label>
        <Field name="password" type="password" id="password"
          class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
          :class="{ 'is-invalid': errors.password }" />
        <div class="invalid-feedback text-red-500 my-2 text-sm select-none">{{ errors.password }}</div>

      </div>
      <div class="flex flex-wrap justify-center">
        <button :disabled="isSubmitting"
          class="flex justify-center w-50 px-4 py-2 my-2 rounded-lg border-none dark:border-violet-500/50 border-1 bg-gradient-to-r from-blue-400 to-blue-500 dark:from-violet-600 dark:to-violet-500 text-white hover:shadow-lg hover:shadow-blue-300/50 hover:ease-in ease-out duration-200 dark:hover:shadow-violet-500/50">
          <the-spinner :class="{ hidden: !isSubmitting }"></the-spinner><span class="select-none"
            :class="{ hidden: isSubmitting }">Giriş</span>
        </button>
      </div>
      <div v-if="errors.apiError" class="text-center text-red-500 mt-3 mb-0 text-sm">{{ errors.apiError }}</div>
    </Form>
  </div>

</template>

<style scoped></style>
