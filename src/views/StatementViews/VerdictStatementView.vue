<script setup>
import { useStatementsStore, useStudentsStore } from '@/stores/api.store';
import TheBreadcrumb from '@/components/TheBreadcrumb.vue';
import { storeToRefs } from 'pinia';
import { onBeforeMount, reactive } from 'vue';
import { useRoute } from 'vue-router';
import ReinstateInfo from '@/components/StatementInfo/ReinstateInfo.vue';
import ExpulsionInfo from '@/components/StatementInfo/ExpulsionInfo.vue';
import VerdictBtnsGroup from '@/components/VerdictBtnsGroup.vue';
import { useAuthStore } from '@/stores/auth.store';
import router from '@/router';

const route = useRoute();

const authStore = useAuthStore();
const studentsStore = useStudentsStore();
const statementsStore = useStatementsStore();
const { studentInfo } = storeToRefs(studentsStore);
const { statement } = storeToRefs(statementsStore);
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
  statementsStore.get(route.params.id, route.meta.statementType).then(() => {
    statementsStore.markAsViewed(route.params.id, route.meta.statementType).then(() => {
      authStore.fetchUser()
    });
    studentsStore.getNeutralInfo(statement.value.student).then(() => {
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

    })
  });
})

function submitStatement() {
  statementsStore.confirmStatement(route.params.id, route.meta.statementType)
  router.push("/statements");
}


function rejectStatement() {
  statementsStore.rejectStatement(route.params.id, route.meta.statementType)
  router.push("/statements");
}


const breadcrumbPaths = [
  { path: "/statements", name: "Arzalar" },
  { path: "", name: "Karar", current: true },
]

</script>
<template>
  <the-breadcrumb :paths="breadcrumbPaths"></the-breadcrumb>
  <div class="tile">
    <h3 class="text-xl font-bold mx-2 select-none">Talyp barada maglumat</h3>
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
  <div class="tile mt-8">
    <reinstate-info :statement="statement" v-if="route.meta.statementType == 'reinstate'"></reinstate-info>
    <expulsion-info :statement="statement" v-else-if="route.meta.statementType == 'expulsion'"></expulsion-info>
    <verdict-btns-group v-if="statement.status === 'Barlagda'" :statement-type="route.meta.statementType"
      @submit-click="submitStatement" @reject-click="rejectStatement"></verdict-btns-group>
    <div v-else-if="statement.status === 'Kabul edildi'" class="mt-4">
      <h4
        class="px-4 py-2 text-[0.8rem] w-max font-medium bg-emerald-400 hover:bg-emerald-500 transition ease-in hover:ease-out duration-200 text-white dark:bg-emerald-700 border border-gray-200 dark:border-gray-700 rounded-lg select-none">
        Tassyklanyldy
      </h4>
    </div>
    <div v-else-if="statement.status === 'Ret edildi'" class="mt-4">
      <h4
        class="px-4 py-2 text-[0.8rem] w-max font-medium bg-red-400 hover:bg-red-500 transition ease-in hover:ease-out duration-200 text-white dark:bg-pink-900 dark:hover:bg-pink-600 border border-gray-200 rounded-lg  dark:border-gray-700  select-none">
        Ret edildi
      </h4>
    </div>

  </div>
</template>
