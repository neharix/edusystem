<template>
  <the-breadcrumb :paths="breadcrumbPaths"></the-breadcrumb>
  <div class="w-full rounded-lg shadow-lg p-4 bg-white dark:bg-[#171131ef]">
    <h3 class="text-xl font-bold mx-2 select-none">Talyp barada maglumatlary üýtgetmek</h3>
    <Form @submit="onSubmit" :validation-schema="schema" v-slot="{ errors, isSubmitting }" class="space-y-4 my-4">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-2">
        <div>
          <label for="fullName" class="info-label">Talybyň ady, familiýasy, atasynyň ady</label>
          <Field name="full_name" type="text" id="fullName" v-model="fullName"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.full_name }" placeholder="F.A.Aa"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.full_name }}
          </div>
        </div>
        <div>
          <label for="birthDate" class="info-label">Doglan senesi</label>
          <Field name="birth_date" type="date" id="birthDate" v-model="birthDate"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.birth_date }" placeholder="Doglan senesi"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.birth_date }}
          </div>
        </div>
        <div>
          <label for="gender" class="info-label">Jynsy</label>
          <Field as="select" name="gender" id="gender"
            class="w-full border border-gray-300 dark:border-gray-700 rounded-md p-2 focus:outline-none"
            v-model="gender">
            <option class="text-gray-600 dark:bg-[#171131ef] dark:text-white" value="M">Oglan</option>
            <option class="text-gray-600 dark:bg-[#171131ef] dark:text-white" value="F">Gyz</option>
          </Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.gender }}
          </div>
        </div>
        <div>
          <label for="nationality" class="info-label">Milleti</label>
          <Field as="select" name="nationality" id="nationality"
            class="w-full border border-gray-300 dark:border-gray-700 rounded-md p-2 focus:outline-none"
            v-model="nationality">
            <option class="text-gray-600 dark:bg-[#171131ef] dark:text-white" v-for="nationalityObj in nationalizations"
              :value="nationalityObj.id">{{ nationalityObj.name }}</option>
          </Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.nationality }}
          </div>
        </div>
        <div>
          <label for="country" class="info-label">Ýurdy</label>
          <Field as="select" name="country" id="country"
            class="w-full border border-gray-300 dark:border-gray-700 rounded-md p-2 focus:outline-none"
            v-model="country">
            <option class="text-gray-600 dark:bg-[#171131ef] dark:text-white" v-for="countryObj in countries"
              :value="countryObj.id">{{ countryObj.name }}</option>
          </Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.country }}
          </div>
        </div>
        <div>
          <label for="registeredPlace" class="info-label">Ýazgyda duran salgysy</label>
          <Field as="textarea" rows="1" name="registered_place" type="text" id="registeredPlace"
            v-model="registeredPlace"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.registered_place }" placeholder="Ýazgyda duran salgysy"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.registered_place }}
          </div>
        </div>
        <div>
          <label for="passport" class="info-label">Passport</label>
          <Field name="passport" type="text" id="passport" v-model="passport"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.passport }" placeholder="Passport maglumatlary"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.passport }}
          </div>
        </div>
        <div>
          <label for="phoneNumber" class="info-label">Telefon belgisi</label>
          <Field name="phone_number" type="text" id="phoneNumber" v-model="phoneNumber"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.phone_number }" placeholder="Telefon belgisi"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.phone_number }}
          </div>
        </div>
        <div>
          <label for="region" class="info-label">Welaýaty</label>
          <Field as="select" name="region" id="region"
            class="w-full border border-gray-300 dark:border-gray-700 rounded-md p-2 focus:outline-none"
            v-model="region">
            <option class="text-gray-600 dark:bg-[#171131ef] dark:text-white" v-for="regionObj in regions"
              :value="regionObj.id">{{ regionObj.name }}</option>
          </Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.region }}
          </div>
        </div>
        <div>
          <label for="specialization" class="info-label">Hünäri</label>
          <Field as="select" name="specialization" id="specialization"
            class="w-full border border-gray-300 dark:border-gray-700 rounded-md p-2 focus:outline-none"
            v-model="specialization">
            <option class="text-gray-600 dark:bg-[#171131ef] dark:text-white"
              v-for="specializationObj in highSchoolSpecializations" :value="specializationObj.instance_id">{{
                specializationObj.name }}</option>
          </Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.specialization }}
          </div>
        </div>
        <div>
          <label for="admissionDate" class="info-label">Okuwa giren senesi</label>
          <Field name="admission_date" type="date" id="admissionDate" v-model="admissionDate"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.admission_date }" placeholder="Okuwa giren senesi"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.admission_date }}
          </div>
        </div>
        <div>
          <label for="paymentType" class="info-label">Töleg görnüşi</label>
          <Field as="select" name="payment_type" id="paymentType"
            class="w-full border border-gray-300 dark:border-gray-700 rounded-md p-2 focus:outline-none"
            v-model="paymentType">
            <option class="text-gray-600 dark:bg-[#171131ef] dark:text-white" value="P">Tölegli</option>
            <option class="text-gray-600 dark:bg-[#171131ef] dark:text-white" value="B">Býudjet</option>
          </Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.payment_type }}
          </div>
        </div>
        <div>
          <label for="familyStutus" class="info-label">Maşgala ýagdaýy</label>
          <Field as="select" name="family_status" id="familyStatus"
            class="w-full border border-gray-300 dark:border-gray-700 rounded-md p-2 focus:outline-none"
            v-model="familyStatus">
            <option class="text-gray-600 dark:bg-[#171131ef] dark:text-white" value="FR">Hossarly</option>
            <option class="text-gray-600 dark:bg-[#171131ef] dark:text-white" value="HO">Ýarym ýetim</option>
            <option class="text-gray-600 dark:bg-[#171131ef] dark:text-white" value="CO">Doly ýetim</option>
            <option class="text-gray-600 dark:bg-[#171131ef] dark:text-white" value="OE">Ýetimler öýünde ösen</option>
          </Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.family_status }}
          </div>
        </div>
        <div v-if="gender === 'M'">
          <label for="militaryService" class="info-label">Harby borç</label>
          <Field name="military_service" type="text" id="militaryService" v-model="militaryService"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.military_service }" placeholder="Harby borç"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.military_service }}
          </div>
        </div>
        <div>
          <label for="label" class="info-label">Bellik</label>
          <Field as="textarea" rows="1" name="label" type="text" id="label" v-model="label"
            class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
            :class="{ 'is-invalid': errors.label }" placeholder="Bellik"></Field>
          <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.label }}
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
      <div v-if="errors.apiError" class="text-center text-red-500 mt-3 mb-0 text-sm select-none">{{
        errors.apiError
      }}
      </div>
    </Form>
  </div>

</template>

<script setup>

import TheSpinner from "@/components/TheSpinner.vue";
import TheBreadcrumb from "@/components/TheBreadcrumb.vue";
import { Field, Form } from "vee-validate";
import * as Yup from 'yup';
import { useStudentsStore, useNationalizationsStore, useCountriesStore, useRegionsStore, useSpecializationsStore } from "@/stores/api.store.js";
import { useRoute } from "vue-router";
import router from "@/router/index.js";
import { onBeforeMount, watch, ref } from "vue";
import { storeToRefs } from 'pinia';


const route = useRoute();

const studentsStore = useStudentsStore();
const nationalizationsStore = useNationalizationsStore();
const countriesStore = useCountriesStore();
const regionsStore = useRegionsStore();
const specializationsStore = useSpecializationsStore();
const { student } = storeToRefs(studentsStore);
const { nationalizations } = storeToRefs(nationalizationsStore);
const { countries } = storeToRefs(countriesStore);
const { regions } = storeToRefs(regionsStore);
const { highSchoolSpecializations } = storeToRefs(specializationsStore);

const fullName = ref('');
const nationality = ref(null);
const country = ref(null);
const region = ref(null);
const specialization = ref(null);
const gender = ref(null);
const familyStatus = ref(null);
const paymentType = ref(null);
const birthDate = ref(null);
const admissionDate = ref(null);
const registeredPlace = ref('');
const studyYear = ref(1);
const phoneNumber = ref('');
const passport = ref('');
const militaryService = ref('');
const label = ref('');


const schema = Yup.object().shape({
  full_name: Yup.string().trim().required('Talybyň F.A.Aa-sy hökman girizilmeli').max(400, "400 simwoldan köp girizmek mümkin däl"),
  birth_date: Yup.date().max(new Date(), 'Geljekki wagt görkezilip bilinmez'),
  gender: Yup.string().required('Jynsy hökmän girizmeli'),
  nationality: Yup.number().required('Milleti hökmän girizmeli'),
  country: Yup.number().required('Ýurdy hökmän girizmeli'),
  registered_place: Yup.string().trim().required('Ýazgyda duran salgysy hökman girizilmeli'),
  passport: Yup.string().trim().required('Passport maglumatlary hökman girizilmeli').max(20, "20 simwoldan köp girizmek mümkin däl"),
  phone_number: Yup.string().trim().required('Telefon belgisi hökman girizilmeli').max(20, "20 simwoldan köp girizmek mümkin däl"),
  region: Yup.number().required('Welaýaty hökmän girizmeli'),
  specialization: Yup.number().required('Hünäri hökmän girizmeli'),
  admission_date: Yup.date().max(new Date(), 'Geljekki wagt görkezilip bilinmez'),
  family_status: Yup.string().required('Maşgala ýagdaýy hökmän girizmeli'),
  payment_type: Yup.string().required('Töleg görnüşi hökmän girizmeli'),
  military_service: Yup.string().trim().max(20, "20 simwoldan köp girizmek mümkin däl"),
  label: Yup.string().trim(),
});

function onSubmit(values, { setErrors }) {
  const { full_name, birth_date, gender, nationality, country, registered_place, passport, phone_number, region, specialization, admission_date, family_status, payment_type, military_service, label } = values;
  return studentsStore.put(route.params.id, { full_name, birth_date, gender, nationality, country, registered_place, passport, phone_number, region, specialization, admission_date, family_status, payment_type, military_service, label }).then(() => {
    router.go(-1);
  }).catch(error => setErrors({ apiError: error }));
}

watch(gender, (newVal) => {
  if (newVal === "F") {
    militaryService.value = '';
  }
})

onBeforeMount(() => {
  nationalizationsStore.getAll();
  countriesStore.getAll();
  regionsStore.getAll();
  studentsStore.get(route.params.id).then(() => {
    if (student.value.active) {
      specializationsStore.getHighSchoolSpecializations(student.value.high_school);
      fullName.value = student.value.full_name;
      nationality.value = student.value.nationality;
      country.value = student.value.country;
      region.value = student.value.region;
      registeredPlace.value = student.value.registered_place;
      phoneNumber.value = student.value.phone_number;
      passport.value = student.value.passport;
      specialization.value = student.value.specialization;
      gender.value = student.value.gender;
      paymentType.value = student.value.payment_type;
      familyStatus.value = student.value.family_status;
      if (student.value.military_service) {
        militaryService.value = student.value.military_service;
      }
      if (student.value.label) {
        label.value = student.value.label;
      }
      birthDate.value = student.value.birth_date;
      admissionDate.value = student.value.admission_date;

    }
    else {
      router.push('/403');
    }
  })
})

const breadcrumbPaths = [
  { path: "/students", name: "Talyplar" },
  { path: "/students/edit", name: "Üýtgetmek", current: true },
]

</script>
