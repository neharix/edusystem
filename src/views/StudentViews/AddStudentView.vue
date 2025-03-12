<template>
  <the-breadcrumb :paths="breadcrumbPaths">
  </the-breadcrumb>
  <div class="w-full rounded-lg shadow-lg p-4 bg-white dark:bg-[#171131ef]">
    <h3 class="text-xl font-bold mx-2 select-none">Talyplary hasaba almak</h3>
    <Form @submit="onSubmit" :validation-schema="schema" v-slot="{ errors, isSubmitting, values }"
      :initial-values="{ high_school: 0 }" class="space-y-4 my-4">
      <div class="w-full flex">
        <div class="w-full">
          <Field as="select" name="high_school" id="high_school" v-model="highSchoolId"
            class="w-full border border-gray-300 dark:border-gray-700 rounded-l-md p-2 focus:outline-none select-none">
            <option class="text-gray-600 dark:bg-[#171131ef] dark:text-white select-none"
              v-for="highSchool in highSchoolsResponse" :value="highSchool.id">{{ highSchool.name }}
            </option>
          </Field>

        </div>
        <div>
          <button @click="getExcel" class="btn-active rounded-e-md h-full px-2 lg:px-6">
            <the-spinner v-if="uxStore.isLoading"></the-spinner>
            <svg v-else xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="w-12 h-6"
              version="1.1" id="Capa_1" viewBox="0 0 26 26" xml:space="preserve">
              <g>
                <path fill="currentColor"
                  d="M25.162,3H16v2.984h3.031v2.031H16V10h3v2h-3v2h3v2h-3v2h3v2h-3v3h9.162   C25.623,23,26,22.609,26,22.13V3.87C26,3.391,25.623,3,25.162,3z M24,20h-4v-2h4V20z M24,16h-4v-2h4V16z M24,12h-4v-2h4V12z M24,8   h-4V6h4V8z" />
                <path fill="currentColor"
                  d="M0,2.889v20.223L15,26V0L0,2.889z M9.488,18.08l-1.745-3.299c-0.066-0.123-0.134-0.349-0.205-0.678   H7.511C7.478,14.258,7.4,14.494,7.277,14.81l-1.751,3.27H2.807l3.228-5.064L3.082,7.951h2.776l1.448,3.037   c0.113,0.24,0.214,0.525,0.304,0.854h0.028c0.057-0.198,0.163-0.492,0.318-0.883l1.61-3.009h2.542l-3.037,5.022l3.122,5.107   L9.488,18.08L9.488,18.08z" />
              </g>
            </svg>
          </button>
        </div>
      </div>
      <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.high_school }}
      </div>
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
import { Field, Form } from "vee-validate";
import * as Yup from 'yup';
import { useHighSchoolsStore, useStudentsStore } from "@/stores/api.store.js";
import router from "@/router/index.js";
import { ref, onBeforeMount } from "vue";
import { storeToRefs } from "pinia";
import { useUxStore } from "@/stores/ux.store";

const uxStore = useUxStore();
const highSchoolsStore = useHighSchoolsStore();
const studentsStore = useStudentsStore();


const { createSessionMistakes, createSessionStatus } = storeToRefs(studentsStore);
const { highSchoolsResponse } = storeToRefs(highSchoolsStore);
const highSchoolId = ref(0);
const fileObj = ref(null);
const fileError = ref(null);
const hasMistake = ref(false);

const schema = Yup.object().shape({
  high_school: Yup.number(),
});


const handleFileChange = (event) => {
  fileObj.value = event.target.files[0];
};

function getExcel() {
  uxStore.isLoading = true;
  studentsStore.getForm(highSchoolId.value, 10).then(() => {
    const blob = new Blob([studentsStore.excelForm], { type: studentsStore.excelFormContentType })
    console.log(blob)
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.target = "_blank";
    link.download = "form.xlsx";
    link.classList.add('hidden');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    studentsStore.resetExcelFormStates();
    uxStore.isLoading = false;
  })
}
// FIXME
const onSubmit = async (values) => {
  if (fileObj.value !== null) {
    fileError.value = null;
    const formData = new FormData();
    formData.append('excel', fileObj.value);
    formData.append("high_school_id", values.high_school)

    return studentsStore.create(formData).then(() => {
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
  { path: "/students/add", name: "Goşmak" },
]


</script>
