<script setup>
import { useFilterStore } from '@/stores/api.store';
import TheBreadcrumb from '@/components/TheBreadcrumb.vue';
import GridCell from '@/components/GridCell.vue';
import { storeToRefs } from 'pinia';
import MultipleSelect from '@/components/MultipleSelect.vue';
import { onBeforeMount, ref, watch } from 'vue';

const militaryService = ref(0);


const filterStore = useFilterStore();
const { data, filterOptions } = storeToRefs(filterStore);



const breadcrumbPaths = [
  { path: "/filter", name: "Süzgüç" },
]

watch(data, (newVal) => {
  console.log(newVal);
})


function updateHighSchools(arr) {
  filterOptions.value.high_schools = arr;
  filterStore.post(filterOptions.value);
}
function updateFaculties(arr) {
  filterOptions.value.faculties = arr;
  filterStore.post(filterOptions.value);
}
function updateDepartments(arr) {
  filterOptions.value.departments = arr;
  filterStore.post(filterOptions.value);
}
function updateSpecializations(arr) {
  filterOptions.value.specializations = arr;
  filterStore.post(filterOptions.value);
}
function updateStudyYears(arr) {
  filterOptions.value.study_years = arr;
  filterStore.post(filterOptions.value);
}
function updateDegrees(arr) {
  filterOptions.value.degrees = arr;
  filterStore.post(filterOptions.value);
}
function updatePaymentTypes(arr) {
  filterOptions.value.payment_types = arr;
  filterStore.post(filterOptions.value);
}
function updateGenders(arr) {
  filterOptions.value.genders = arr;
  filterStore.post(filterOptions.value);
}
function updateNationalities(arr) {
  filterOptions.value.nationalities = arr;
  filterStore.post(filterOptions.value);
}
function updateCountries(arr) {
  filterOptions.value.countries = arr;
  filterStore.post(filterOptions.value);
}
function updateRegions(arr) {
  filterOptions.value.regions = arr;
  filterStore.post(filterOptions.value);
}
function updateMilitaryService() {
  filterOptions.value.military_service = militaryService.value;
  filterStore.post(filterOptions.value);
}


onBeforeMount(() => {
  filterOptions.value = {
    high_schools: [],
    faculties: [],
    departments: [],
    specializations: [],
    study_years: [],
    degrees: [],
    payment_types: [],
    genders: [],
    nationalities: [],
    regions: [],

    countries: [],
    military_service: 0,
  }
  sessionStorage.setItem(
    "filterOptions",
    JSON.stringify(filterOptions.value)
  );
})

</script>
<template>
  <the-breadcrumb :paths="breadcrumbPaths"></the-breadcrumb>
  <h3 class="text-xl font-semibold mx-2 my-8 select-none">Talyplar</h3>
  <div class="w-full grid grid-cols-1 md:grid-cols-3 gap-8">
    <grid-cell v-for="item in data.students" :label="item.name" :data-value="item.count"
      :link="`/filter/detail?gender=${item.query}`" icon-bg-class="bg-sky-200 dark:bg-sky-500/75">
      <svg class="w-6 h-8 stroke-sky-500 dark:stroke-sky-900" xmlns="http://www.w3.org/2000/svg" width="14" height="14"
        viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
        stroke-linejoin="round">
        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
        <circle cx="9" cy="7" r="4"></circle>
        <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
        <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
      </svg>
    </grid-cell>
  </div>
  <h3 class="text-xl font-semibold mx-2 my-8 select-none">Welaýatlar boýunça</h3>
  <div class="w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
    <grid-cell v-for="item in data.regions" :label="item.name" :data-value="item.count"
      :link="`/filter/detail?region=${item.id}`" icon-bg-class="bg-red-200 dark:bg-red-500/75">
      <svg class="w-6 h-8 stroke-red-500 dark:stroke-red-900" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
        <circle cx="12" cy="10" r="3"></circle>
      </svg>
    </grid-cell>
  </div>
  <h3 class="text-xl font-semibold mx-2 my-8 select-none">Hünär derejeleri boýunça</h3>
  <div class="w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
    <grid-cell v-for="item in data.degrees_output" :label="item.name" :data-value="item.count"
      icon-bg-class="bg-yellow-200 dark:bg-yellow-500/75">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-6 stroke-yellow-500 dark:stroke-yellow-900" viewBox="0 0 24 24"
        fill="transparent" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="3" width="7" height="7"></rect>
        <rect x="14" y="3" width="7" height="7"></rect>
        <rect x="14" y="14" width="7" height="7"></rect>
        <rect x="3" y="14" width="7" height="7"></rect>
      </svg>
    </grid-cell>
  </div>

  <div class="tile my-8">
    <h3 class="text-xl font-semibold mx-2 mb-4 mt-2 select-none">Gözleg gurallary</h3>
    <hr class="border-gray-200 dark:border-gray-800">
    <div class="my-6">
      <p class="info-label">Ýokary okuw mekdep</p>
      <multiple-select :data="data.high_schools" @update="updateHighSchools"
        empty-label="Maglumat gorunda ýokary okuw mekdep tapylmady"></multiple-select>
    </div>
    <div class="my-6">
      <p class="info-label">Fakultet</p>
      <multiple-select :data="data.faculties" @update="updateFaculties"
        empty-label="Maglumat gorunda fakultet tapylmady"></multiple-select>
    </div>
    <div class="my-6">
      <p class="info-label">Kafedra</p>
      <multiple-select :data="data.departments" @update="updateDepartments"
        empty-label="Maglumat gorunda kafedra tapylmady"></multiple-select>
    </div>
    <div class="my-6">
      <p class="info-label">Hünär</p>
      <multiple-select :data="data.specializations" @update="updateSpecializations"
        empty-label="Maglumat gorunda hünär tapylmady"></multiple-select>
    </div>
    <div class="my-6">
      <p class="info-label">Kursy</p>
      <multiple-select :data="data.study_years" @update="updateStudyYears"
        empty-label="Kurs tapylmady"></multiple-select>
    </div>
    <div class="my-6">
      <p class="info-label">Hünär derejesi</p>
      <multiple-select :data="data.degrees" @update="updateDegrees"
        empty-label="Hünär derejesi tapylmady"></multiple-select>
    </div>
    <div class="my-6">
      <p class="info-label">Töleg görnüşi</p>
      <multiple-select :data="data.payment_types" @update="updatePaymentTypes"
        empty-label="Töleg görnüşi tapylmady"></multiple-select>
    </div>
    <div class="my-6">
      <p class="info-label">Jynsy</p>
      <multiple-select :data="data.genders" @update="updateGenders" empty-label="Jyns tapylmady"></multiple-select>
    </div>
    <div class="my-6">
      <p class="info-label">Millet</p>
      <multiple-select :data="data.nationalities" @update="updateNationalities"
        empty-label="Millet tapylmady"></multiple-select>
    </div>
    <div class="my-6">
      <p class="info-label">Döwlet</p>
      <multiple-select :data="data.countries" @update="updateCountries"
        empty-label="Döwlet tapylmady"></multiple-select>
    </div>
    <div class="my-6">
      <p class="info-label">Welaýat</p>
      <multiple-select :data="data.regions" @update="updateRegions" empty-label="Welaýat tapylmady"></multiple-select>
    </div>
    <div class="my-6">
      <p class="info-label" for="military-service">Harby borç</p>
      <select class="w-full border border-gray-300 rounded-md p-2 focus:outline-none" @change="updateMilitaryService"
        v-model.number="militaryService">
        <option class="text-gray-600 dark:bg-[#171131ef] dark:text-white" :value="0">Saýlanmadyk</option>
        <option class="text-gray-600 dark:bg-[#171131ef] dark:text-white" :value="1">Harby borjuny ýerine ýetiren
        </option>
        <option class="text-gray-600 dark:bg-[#171131ef] dark:text-white" :value="2">Harby borçly</option>
      </select>
    </div>
  </div>
  <div class="h-24"></div>
</template>
