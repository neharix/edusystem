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
const authStore = useAuthStore();

const schema = Yup.object().shape({
  username: Yup.string().trim().required('Ulanyjy ady hökmany şekilde girizilmeli'),
  password: Yup.string().required('Açar sözi hökmany şekilde girizilmeli'),
});

function onSubmit(values, { setErrors }) {
  const authStore = useAuthStore();
  const { username, password } = values;
  return authStore.login({ username, password }).then(() => {
    if (authStore.isLoginSuccessfully === 'success') {
      router.push('/');
    }
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

function togglePwdVisibility() {
  let pwdField = document.querySelector('#password');
  if (pwdField.getAttribute('type') === "password") {
    pwdField.setAttribute('type', 'text')
  } else {
    pwdField.setAttribute('type', 'password')
  }
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
      <div class="relative">
        <Field name="username" type="text" id="username" class="peer text-input" placeholder="Ulanyjy ady"
          :class="{ 'is-invalid': errors.username }" />
        <label for="username" class="text-input-placeholder">
          Ulanyjy ady
        </label>
        <div class="invalid-feedback text-red-500 my-2 text-sm select-none">{{ errors.username }}</div>
      </div>
      <div class="relative">
        <Field name="password" type="password" id="password" placeholder="Açar sözi" class="peer text-input"
          :class="{ 'is-invalid': errors.password }" />
        <div class="absolute top-0 right-0 p-4" @click="togglePwdVisibility">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6 text-gray-500" viewBox="0 0 24 24" fill="none">
            <path fill-rule="evenodd" clip-rule="evenodd"
              d="M12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9ZM11 12C11 11.4477 11.4477 11 12 11C12.5523 11 13 11.4477 13 12C13 12.5523 12.5523 13 12 13C11.4477 13 11 12.5523 11 12Z"
              fill="currentColor" />
            <path fill-rule="evenodd" clip-rule="evenodd"
              d="M21.83 11.2807C19.542 7.15186 15.8122 5 12 5C8.18777 5 4.45796 7.15186 2.17003 11.2807C1.94637 11.6844 1.94361 12.1821 2.16029 12.5876C4.41183 16.8013 8.1628 19 12 19C15.8372 19 19.5882 16.8013 21.8397 12.5876C22.0564 12.1821 22.0536 11.6844 21.83 11.2807ZM12 17C9.06097 17 6.04052 15.3724 4.09173 11.9487C6.06862 8.59614 9.07319 7 12 7C14.9268 7 17.9314 8.59614 19.9083 11.9487C17.9595 15.3724 14.939 17 12 17Z"
              fill="currentColor" />
          </svg>
        </div>
        <label for="password" class="text-input-placeholder">
          Açar sözi
        </label>
        <div class="invalid-feedback text-red-500 my-2 text-sm select-none">{{ errors.password }}</div>
      </div>
      <div class="flex flex-wrap justify-center">
        <button :disabled="isSubmitting"
          class="flex justify-center w-50 px-4 py-2 my-2 rounded-lg border-none dark:border-violet-500/50 border-1 bg-gradient-to-r from-blue-400 to-blue-500 dark:from-violet-600 dark:to-violet-500 text-white hover:shadow-md hover:shadow-blue-300/50 hover:ease-in ease-out duration-200 dark:hover:shadow-violet-500/50">
          <the-spinner :class="{ hidden: !isSubmitting }"></the-spinner><span class="select-none"
            :class="{ hidden: isSubmitting }">Giriş</span>
        </button>
      </div>
      <div v-if="authStore.isLoginSuccessfully === 'failed'" class="text-center text-red-500 mt-3 mb-0 text-sm">Ulanyjy
        adyňyz ýa-da açar sözüňiz ýalňyş</div>
      <div v-if="errors.apiError" class="text-center text-red-500 mt-3 mb-0 text-sm">{{ errors.apiError }}</div>
    </Form>
  </div>

</template>

<style scoped></style>
