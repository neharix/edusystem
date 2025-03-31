<template>
  <the-breadcrumb :paths="breadcrumbPaths">
  </the-breadcrumb>
  <div class="w-full rounded-lg shadow-lg p-4 bg-white dark:bg-[#171131ef]">
    <h3 class="text-xl font-bold mx-2 select-none">Formany barlamak</h3>
    <Form @submit="onSubmit" :validation-schema="schema" v-slot="{ errors, isSubmitting, values }"
      class="space-y-4 my-4">
      <div>
        <div class="mb-4">
          <label for="file" class="block mb-1 select-none">Excel</label>
          <input type="file" id="file" name="file"
            accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
            @change="(event) => handleFileChange(event)"
            class="block w-full px-4 py-2 border-gray-300 dark:border-gray-600text-sm border rounded-md cursor-pointer bg-transparent focus:outline-none dark:placeholder-gray-400">
          <p v-if="fileError" class="text-red-500 text-sm select-none">{{ fileError }}</p>
        </div>
      </div>
      <div class="flex flex-wrap justify-center md:justify-end lg:justify-end">
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
    <div v-if="createSessionMistakes.length > 0" class="space-y-4">
      <h3 class="text-xl font-bold text-red-500 select-none">Üstünlikli ýüklenildi, emma käbir setirlerde näsazlyk ýüze
        çykdy</h3>
      <p v-for="mistake in createSessionMistakes" class="text-red-500 select-none">{{ mistake }}</p>
    </div>
  </div>
</template>

<script setup>

import TheSpinner from "@/components/TheSpinner.vue";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { Form } from "vee-validate";
import * as Yup from 'yup';
import { useHighSchoolsStore, useStudentsStore } from "@/stores/api.store.js";
import router from "@/router/index.js";
import { ref, onBeforeMount } from "vue";
import { storeToRefs } from "pinia";

const highSchoolsStore = useHighSchoolsStore();
const studentsStore = useStudentsStore();


const { createSessionMistakes, createSessionStatus } = storeToRefs(studentsStore);
const highSchoolId = ref(0);
const fileObj = ref(null);
const fileError = ref(null);

const schema = Yup.object().shape({
  high_school: Yup.number(),
});


const handleFileChange = (event) => {
  fileObj.value = event.target.files[0];
};

// FIXME
const onSubmit = async (values) => {
  if (fileObj.value !== null) {
    fileError.value = null;
    const formData = new FormData();
    formData.append('excel', fileObj.value);

    return studentsStore.validate(formData).then(() => {
      if (createSessionStatus.value) {
        router.push('/students');
      }
    }).catch(error => {
      setErrors({ apiError: error });
    })
  } else {
    fileError.value = 'Excel faýlyny hökmän girizmeli'
  }
}

onBeforeMount(() => {
  highSchoolsStore.getAll().then(() => {
    if (highSchoolsStore.highSchoolsResponse.length != 0) {
      highSchoolId.value = highSchoolsStore.highSchoolsResponse[0].id;
    }
  });
})

const breadcrumbPaths = [
  { path: "/students", name: "Talyplar" },
  { path: "/students/validate", name: "Walidator" },
]


</script>
