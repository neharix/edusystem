<script setup>
import { Form, Field } from 'vee-validate';
import TheSpinner from '@/components/TheSpinner.vue';
import * as Yup from 'yup';
import TheBreadcrumb from '@/components/TheBreadcrumb.vue';
import { useTeacherStatementsStore } from '@/stores/api.store';
import router from '@/router';
import { onBeforeMount } from 'vue';
import { storeToRefs } from 'pinia';


const teacherStatementsStore = useTeacherStatementsStore();
const { teacherStatement } = storeToRefs(teacherStatementsStore)

const breadcrumbPaths = [
  { path: "/teachers", name: "Mugallymlar" },
  { path: "/teachers/add", name: "Hasabat döretmek" }
];



const schema = Yup.object().shape({
  workload_1_25: Yup.number().typeError('Hökman san girizilmeli').min(0, "San otrisatel bolup bilmez").required('Hökman san girizilmeli'),
  workload_1_00: Yup.number().typeError('Hökman san girizilmeli').min(0, "San otrisatel bolup bilmez").required('Hökman san girizilmeli'),
  workload_0_75: Yup.number().typeError('Hökman san girizilmeli').min(0, "San otrisatel bolup bilmez").required('Hökman san girizilmeli'),
  workload_0_50: Yup.number().typeError('Hökman san girizilmeli').min(0, "San otrisatel bolup bilmez").required('Hökman san girizilmeli'),
  doctor_degree: Yup.number().typeError('Hökman san girizilmeli').min(0, "San otrisatel bolup bilmez").required('Hökman san girizilmeli'),
  candidate_degree: Yup.number().typeError('Hökman san girizilmeli').min(0, "San otrisatel bolup bilmez").required('Hökman san girizilmeli'),
  professor: Yup.number().typeError('Hökman san girizilmeli').min(0, "San otrisatel bolup bilmez").required('Hökman san girizilmeli'),
  docent: Yup.number().typeError('Hökman san girizilmeli').min(0, "San otrisatel bolup bilmez").required('Hökman san girizilmeli'),
  department_head: Yup.number().typeError('Hökman san girizilmeli').min(0, "San otrisatel bolup bilmez").required('Hökman san girizilmeli'),
  professor_job: Yup.number().typeError('Hökman san girizilmeli').min(0, "San otrisatel bolup bilmez").required('Hökman san girizilmeli'),
  docent_job: Yup.number().typeError('Hökman san girizilmeli').min(0, "San otrisatel bolup bilmez").required('Hökman san girizilmeli'),
  senior_teachers: Yup.number().typeError('Hökman san girizilmeli').min(0, "San otrisatel bolup bilmez").required('Hökman san girizilmeli'),
  teachers: Yup.number().typeError('Hökman san girizilmeli').min(0, "San otrisatel bolup bilmez").required('Hökman san girizilmeli'),
  intern_teachers: Yup.number().typeError('Hökman san girizilmeli').min(0, "San otrisatel bolup bilmez").required('Hökman san girizilmeli'),
});

onBeforeMount(() => {
  teacherStatementsStore.getTeacherStatementByUser().then(() => {
    if (!(teacherStatement.value.null)) {
      router.push('/teachers');
    }
  })
})

function onSubmit(values, { setErrors }) {
  const { workload_1_25, workload_1_00, workload_0_75, workload_0_50, doctor_degree, candidate_degree, professor, docent, department_head, professor_job, docent_job, senior_teachers, teachers, intern_teachers } = values;
  return teacherStatementsStore.create({ workload_1_25, workload_1_00, workload_0_75, workload_0_50, doctor_degree, candidate_degree, professor, docent, department_head, professor_job, docent_job, senior_teachers, teachers, intern_teachers }).then(() => {
    router.push('/teachers');
  })
    .catch(error => setErrors({ apiError: error }));
}


</script>
<template>
  <the-breadcrumb :paths="breadcrumbPaths"></the-breadcrumb>

  <div class="tile">
    <h3 class="text-xl font-bold mx-2 select-none">Täze mugallym hasabatyny hasaba almak</h3>
    <Form @submit="onSubmit" :validation-schema="schema" v-slot="{ errors, isSubmitting, values }"
      :initial-values="{ workload_1_25: 0, workload_1_00: 0, workload_0_75: 0, workload_0_50: 0, doctor_degree: 0, candidate_degree: 0, professor: 0, docent: 0, department_head: 0, professor_job: 0, docent_job: 0, senior_teachers: 0, teachers: 0, intern_teachers: 0 }"
      class="space-y-4 my-4">
      <h4 class="text-lg font-semibold mx-2 select-none">Professor-mugallymlaryň ýerine ýetirýän iş ýükleriniň möçberi
        barada maglumat</h4>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4">
        <div>
          <label class="info-label" for="workload-1-25">Iş ýüki 1.25</label>
          <Field name="workload_1_25" type="number" id="workload-1-25"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.workload_1_25 }" placeholder="Iş ýüki 1.25"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.workload_1_25 }}
          </div>
        </div>
        <div>
          <label class="info-label" for="workload-1-00">Iş ýüki 1.00</label>
          <Field name="workload_1_00" type="number" id="workload-1-00"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.workload_1_00 }" placeholder="Iş ýüki 1.00"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.workload_1_00 }}
          </div>
        </div>
        <div>
          <label class="info-label" for="workload-0-75">Iş ýüki 0.75</label>
          <Field name="workload_0_75" type="number" id="workload-0-75"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.workload_0_75 }" placeholder="Iş ýüki 0.75"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.workload_0_75 }}
          </div>
        </div>
        <div>
          <label class="info-label" for="workload-0-50">Iş ýüki 0.50</label>
          <Field name="workload_0_50" type="number" id="workload-0-50"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.workload_0_50 }" placeholder="Iş ýüki 0.50"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.workload_0_50 }}
          </div>
        </div>
      </div>
      <h4 class="text-lg font-semibold mx-2 select-none">Ylmy derejeleri boýunça</h4>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4">
        <div>
          <label class="info-label" for="doctor-degree">Ylymlaryň doktory</label>
          <Field name="doctor_degree" type="number" id="doctor-degree"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.doctor_degree }" placeholder="Ylymlaryň doktory"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.doctor_degree }}
          </div>
        </div>
        <div>
          <label class="info-label" for="candidate-degree">Ylymlaryň kandidaty</label>
          <Field name="candidate_degree" type="number" id="candidate-degree"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.candidate_degree }" placeholder="Ylymlaryň kandidaty"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.candidate_degree }}
          </div>
        </div>
      </div>
      <h4 class="text-lg font-semibold mx-2 select-none">Ylmy atlary boýunça</h4>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4">
        <div>
          <label class="info-label" for="professor">Professor</label>
          <Field name="professor" type="number" id="professor"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.professor }" placeholder="Professor"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.professor }}
          </div>
        </div>
        <div>
          <label class="info-label" for="docent">Dosent</label>
          <Field name="docent" type="number" id="docent"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.docent }" placeholder="Dosent"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.docent }}
          </div>
        </div>
      </div>
      <h4 class="text-lg font-semibold mx-2 select-none">Wezipeler boýunça</h4>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="info-label" for="department-head">Kafedra müdiri, professor</label>
          <Field name="department_head" type="number" id="department-head"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.department_head }" placeholder="Kafedra müdiri, professor"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.department_head }}
          </div>
        </div>
        <div>
          <label class="info-label" for="professor-job">Professor</label>
          <Field name="professor_job" type="number" id="professor-job"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.professor_job }" placeholder="Professor"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.professor_job }}
          </div>
        </div>
        <div>
          <label class="info-label" for="docent-job">Dosent</label>
          <Field name="docent_job" type="number" id="docent-job"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.docent_job }" placeholder="Dosent"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.docent_job }}
          </div>
        </div>

        <div>
          <label class="info-label" for="senior-teachers">Uly mugallym</label>
          <Field name="senior_teachers" type="number" id="senior-teachers"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.senior_teachers }" placeholder="Uly mugallym"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.senior_teachers }}
          </div>
        </div>
        <div>
          <label class="info-label" for="teachers">Mugallym</label>
          <Field name="teachers" type="number" id="teachers"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.teachers }" placeholder="Mugallym"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.teachers }}
          </div>
        </div>
        <div>
          <label class="info-label" for="intern-teachers">Mugallym-öwreniji</label>
          <Field name="intern_teachers" type="number" id="intern-teachers"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.intern_teachers }" placeholder="Mugallym-öwreniji"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.intern_teachers }}
          </div>
        </div>
      </div>
      <div class="flex flex-wrap justify-center md:justify-end items-center">
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
