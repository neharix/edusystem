<script setup>
import { useStudentsStore } from '@/stores/api.store';
import TheBreadcrumb from '@/components/TheBreadcrumb.vue';
import { storeToRefs } from 'pinia';
import { computed, onBeforeMount, reactive } from 'vue';
import { useRoute } from 'vue-router';
import router from '@/router';
import ExpulsionStatement from '@/components/Forms/ExpulsionStatement.vue';
import { useAuthStore } from '@/stores/auth.store';
import { useUxStore } from '@/stores/ux.store';
import TheSpinner from '@/components/TheSpinner.vue';

const uxStore = useUxStore();

const authStore = useAuthStore();
const { user } = storeToRefs(authStore);

const expulsionStatementVisibility = computed(() => {
  try {
    return !user.value.is_superuser;
  }
  catch {
    return false;
  }
})

const route = useRoute();


const studentsStore = useStudentsStore();
const { studentInfo } = storeToRefs(studentsStore);
const student = reactive({
  fullName: '',
  highSchool: '',
  nationality: '',
  country: '',
  region: '',
  specialization: '',
  department: '',
  faculty: '',
  gender: '',
  familyStatus: '',
  paymentType: '',
  birthDate: '',
  admissionDate: '',
  registeredPlace: '',
  studyYear: '',
  phoneNumber: '',
  passport: '',
  militaryService: null,
  label: null,
});

onBeforeMount(() => {
  uxStore.isLoading = true;
  studentsStore.getInfo(route.params.id).then(() => {
    if (studentInfo.value.active) {
      student.fullName = studentInfo.value.full_name;
      student.nationality = studentInfo.value.nationality.name;
      student.country = studentInfo.value.country.name;
      student.region = studentInfo.value.region.name;
      student.highSchool = studentInfo.value.high_school.name;
      student.faculty = studentInfo.value.specialization.faculty_department.high_school_faculty.faculty.name;
      student.department = studentInfo.value.specialization.faculty_department.department.name;
      student.specialization = `${studentInfo.value.specialization.specialization.name} (${studentInfo.value.specialization.specialization.degree.name} ${studentInfo.value.specialization.specialization.degree.duration} ýyl)`;
      student.registeredPlace = studentInfo.value.registered_place;
      student.phoneNumber = studentInfo.value.phone_number;
      student.passport = studentInfo.value.passport;

      switch (studentInfo.value.gender) {
        case 'F':
          student.gender = "Gyz";
          break;
        case 'M':
          student.gender = "Oglan";
          break;
      }

      switch (studentInfo.value.payment_type) {
        case 'P':
          student.paymentType = "Tölegli";
          break;
        case 'B':
          student.paymentType = "Býudjet";
          break;
      }

      switch (studentInfo.value.family_status) {
        case 'FR':
          student.familyStatus = "Hossarly";
          break;
        case 'HO':
          student.familyStatus = "Ýarym ýetim";
          break;
        case 'CO':
          student.familyStatus = "Doly ýetim";
          break;
        case 'OE':
          student.familyStatus = "Ýetimler öýünde ösen";
          break;
      }

      if (studentInfo.value.label) {
        student.label = studentInfo.value.label;
      }
      if (studentInfo.value.military_service) {
        student.militaryService = studentInfo.value.military_service;
      }

      let birthDate = new Date(studentInfo.value.birth_date);
      student.birthDate = birthDate.toLocaleDateString();
      let admissionDate = new Date(studentInfo.value.admission_date);
      student.admissionDate = admissionDate.toLocaleDateString();
      uxStore.isLoading = false;
    }
    else {
      uxStore.isLoading = false;
      router.push('/403');
    }
  })
})

const breadcrumbPaths = [
  { path: "/students", name: "Talyplar" },
  { path: "/students/view", name: "Görmek", current: true },
]

</script>
<template>
  <the-breadcrumb :paths="breadcrumbPaths"></the-breadcrumb>
  <div class="tile">
    <div class="flex justify-between">
      <h3 class="text-base md:text-xl font-bold mx-2 select-none">Talyp barada maglumat</h3>
      <the-spinner v-if="uxStore.isLoading"></the-spinner>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-2">
      <div>
        <p class="info-label">Talybyň ady, familiýasy, atasynyň ady</p>
        <p class="info-content">{{
          student.fullName }}
        </p>
      </div>
      <div>
        <p class="info-label">Doglan senesi</p>
        <p class="info-content">{{ student.birthDate }}</p>
      </div>
      <div>
        <p class="info-label">Jynsy</p>
        <p class="info-content">{{ student.gender }}</p>
      </div>
      <div>
        <p class="info-label">Milleti</p>
        <p class="info-content">{{ student.nationality }}</p>
      </div>
      <div>
        <p class="info-label">Ýurdy</p>
        <p class="info-content">{{ student.country }}</p>
      </div>
      <div>
        <p class="info-label">Ýazgyda duran salgysy</p>
        <p class="info-content">{{ student.registeredPlace }}</p>
      </div>
      <div>
        <p class="info-label">Passport</p>
        <p class="info-content">{{ student.passport }}</p>
      </div>
      <div>
        <p class="info-label">Telefon belgisi</p>
        <p class="info-content">{{ student.phoneNumber }}</p>
      </div>
      <div>
        <p class="info-label">Welaýaty</p>
        <p class="info-content">{{ student.region }}</p>
      </div>
      <div>
        <p class="info-label">Ýokary okuw mekdebi</p>
        <p class="info-content">{{ student.highSchool }}</p>
      </div>
      <div>
        <p class="info-label">Fakulteti</p>
        <p class="info-content">{{ student.faculty }}</p>
      </div>
      <div>
        <p class="info-label">Kafedrasy</p>
        <p class="info-content">{{ student.department }}</p>
      </div>
      <div>
        <p class="info-label">Hünäri</p>
        <p class="info-content">{{ student.specialization }}</p>
      </div>
      <div>
        <p class="info-label">Okuwa giren senesi</p>
        <p class="info-content">{{ student.admissionDate }}</p>
      </div>
      <div>
        <p class="info-label">Töleg görnüşi</p>
        <p class="info-content">{{ student.paymentType }}</p>
      </div>
      <div>
        <p class="info-label">Maşgala ýagdaýy</p>
        <p class="info-content">{{ student.familyStatus }}</p>
      </div>

      <div v-if="student.gender === 'Oglan'">
        <p class="info-label">Harby borç</p>
        <p class="info-content" :class="{ 'text-yellow-500 dark:text-amber-200': !student.militaryService }">{{
          student.militaryService ?
            student.militaryService :
            'Heniz harby borjyny ýerine ýetirmedik' }}</p>
      </div>
      <div v-if="student.label">
        <p class="info-label">Bellik</p>
        <p class="info-content">{{ student.label }}</p>
      </div>

    </div>
  </div>
  <expulsion-statement v-if="expulsionStatementVisibility"></expulsion-statement>
</template>
