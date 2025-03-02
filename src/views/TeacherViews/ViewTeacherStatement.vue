<script setup>
import GridCell from '@/components/GridCell.vue';
import { useDiplomasStore, useTeacherStatementsStore } from '@/stores/api.store';
import { storeToRefs } from 'pinia';
import { onBeforeMount, watch, ref } from 'vue';
import { Field, Form } from "vee-validate";
import * as Yup from 'yup';
import TheToast from "@/components/TheToast.vue";
import useToast from "@/use/useToast.js";
import { useRoute } from 'vue-router';
import TheBreadcrumb from '@/components/TheBreadcrumb.vue';
import HighSchoolDiplomaReportsDataTable from '@/components/DataTables/HighSchoolDiplomaReportsDataTable.vue';
import HighSchoolDiplomaActionsDataTable from '@/components/DataTables/HighSchoolDiplomaActionsDataTable.vue';
import VerdictBtnsGroup from '@/components/VerdictBtnsGroup.vue';
import { useAuthStore } from '@/stores/auth.store';
import TheSpinner from '@/components/TheSpinner.vue';

const route = useRoute();

const { toasts, addToast } = useToast();

const authStore = useAuthStore()
const teacherStatementsStore = useTeacherStatementsStore()
const { teacherStatement, submitStatus, updateStatus } = storeToRefs(teacherStatementsStore);

const allowingDate = ref(null);

const schema = Yup.object().shape({
  allowed_until: Yup.date(),
});



onBeforeMount(() => {
  teacherStatementsStore.getTeacherStatementById(route.params.id)
  authStore.fetchUser()
})


function update() {
  teacherStatementsStore.getTeacherStatementById(route.params.id)
}


watch(submitStatus, (newVal) => {
  if (submitStatus.value) {
    if (submitStatus.value === 'success') {
      addToast('Hasabat üstünlikli tassyklandy', 'success');
    } else if (submitStatus.value === 'error') {
      addToast('Tassyklama prosesinde ýalňyşlyk ýüze çykdy', 'error');
    }
  }
  submitStatus.value = null;
})


function giveVerdict(id, verdict) {
  teacherStatementsStore.giveVerdictStatement(id, verdict).then(() => {
    update();
  });
}

const breadcrumbPaths = [
  { path: "/teachers", name: "Mugallymlar" },
  { path: "/teachers/view", name: "Görmek", current: true },
]

</script>
<template>
  <the-breadcrumb :paths="breadcrumbPaths"></the-breadcrumb>
  <h3 class="text-xl font-bold mx-2 my-4 select-none">Professor-mugallymlaryň ýerine ýetirýän iş ýükleriniň möçberi
    barada maglumat</h3>
  <div class="grid md:grid-cols-4 sm:grid-cols-2 gap-8">
    <grid-cell label="Iş ýüki 1.25" :data-value="teacherStatement.workload_1_25"
      icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_901_948)">
          <path
            d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        <defs>
          <clipPath id="clip0_901_948">
            <rect width="32" height="32" fill="white" />
          </clipPath>
        </defs>
      </svg>
    </grid-cell>
    <grid-cell label="Iş ýüki 1.00" :data-value="teacherStatement.workload_1_00"
      icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_901_948)">
          <path
            d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        <defs>
          <clipPath id="clip0_901_948">
            <rect width="32" height="32" fill="white" />
          </clipPath>
        </defs>
      </svg>
    </grid-cell>
    <grid-cell label="Iş ýüki 0.75" :data-value="teacherStatement.workload_0_75"
      icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_901_948)">
          <path
            d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        <defs>
          <clipPath id="clip0_901_948">
            <rect width="32" height="32" fill="white" />
          </clipPath>
        </defs>
      </svg>
    </grid-cell>
    <grid-cell label="Iş ýüki 0.50" :data-value="teacherStatement.workload_0_50"
      icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_901_948)">
          <path
            d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        <defs>
          <clipPath id="clip0_901_948">
            <rect width="32" height="32" fill="white" />
          </clipPath>
        </defs>
      </svg>
    </grid-cell>
  </div>
  <h3 class="text-xl font-bold mx-2 my-4 select-none">Ylmy derejeleri boýunça</h3>
  <div class="grid md:grid-cols-4 sm:grid-cols-2 gap-8">
    <grid-cell label="Ylymlaryň doktory" :custom-classes="'md:col-span-2 sm:col-span-1'"
      :data-value="teacherStatement.doctor_degree" icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_901_948)">
          <path
            d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        <defs>
          <clipPath id="clip0_901_948">
            <rect width="32" height="32" fill="white" />
          </clipPath>
        </defs>
      </svg>
    </grid-cell>
    <grid-cell label="Ylymlaryň kandidaty" :custom-classes="'md:col-span-2 sm:col-span-1'"
      :data-value="teacherStatement.candidate_degree" icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_901_948)">
          <path
            d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        <defs>
          <clipPath id="clip0_901_948">
            <rect width="32" height="32" fill="white" />
          </clipPath>
        </defs>
      </svg>
    </grid-cell>
  </div>
  <h3 class="text-xl font-bold mx-2 my-4 select-none">Ylmy atlary boýunça</h3>
  <div class="grid md:grid-cols-4 sm:grid-cols-2 gap-8">
    <grid-cell label="Professor" :custom-classes="'md:col-span-2 sm:col-span-1'"
      :data-value="teacherStatement.professor" icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_901_948)">
          <path
            d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        <defs>
          <clipPath id="clip0_901_948">
            <rect width="32" height="32" fill="white" />
          </clipPath>
        </defs>
      </svg>
    </grid-cell>
    <grid-cell label="Dosent" :custom-classes="'md:col-span-2 sm:col-span-1'" :data-value="teacherStatement.docent"
      icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_901_948)">
          <path
            d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        <defs>
          <clipPath id="clip0_901_948">
            <rect width="32" height="32" fill="white" />
          </clipPath>
        </defs>
      </svg>
    </grid-cell>
  </div>
  <h3 class="text-xl font-bold mx-2 my-4 select-none">Wezipeler boýunça</h3>
  <div class="grid md:grid-cols-4 sm:grid-cols-2 gap-8">
    <grid-cell label="Kafedra müdiri, professor" :data-value="teacherStatement.department_head"
      icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_901_948)">
          <path
            d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        <defs>
          <clipPath id="clip0_901_948">
            <rect width="32" height="32" fill="white" />
          </clipPath>
        </defs>
      </svg>
    </grid-cell>
    <grid-cell label="Professor" :custom-classes="'md:col-span-2 sm:col-span-1'"
      :data-value="teacherStatement.professor_job" icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_901_948)">
          <path
            d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        <defs>
          <clipPath id="clip0_901_948">
            <rect width="32" height="32" fill="white" />
          </clipPath>
        </defs>
      </svg>
    </grid-cell>
    <grid-cell label="Dosent" :data-value="teacherStatement.docent_job"
      icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_901_948)">
          <path
            d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        <defs>
          <clipPath id="clip0_901_948">
            <rect width="32" height="32" fill="white" />
          </clipPath>
        </defs>
      </svg>
    </grid-cell>
    <grid-cell label="Uly mugallym" :data-value="teacherStatement.senior_teachers"
      icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_901_948)">
          <path
            d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        <defs>
          <clipPath id="clip0_901_948">
            <rect width="32" height="32" fill="white" />
          </clipPath>
        </defs>
      </svg>
    </grid-cell>
    <grid-cell label="Mugallym" :custom-classes="'md:col-span-2 sm:col-span-1'" :data-value="teacherStatement.teachers"
      icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_901_948)">
          <path
            d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        <defs>
          <clipPath id="clip0_901_948">
            <rect width="32" height="32" fill="white" />
          </clipPath>
        </defs>
      </svg>
    </grid-cell>
    <grid-cell label="Mugallym-öwreniji" :data-value="teacherStatement.intern_teachers"
      icon-bg-class="bg-green-200 dark:bg-green-500/75">
      <svg class="w-6 stroke-green-500 dark:stroke-green-900" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_901_948)">
          <path
            d="M21 28V2C21 1.447 20.553 1 20 1H2C1.447 1 1 1.447 1 2V31H8V25H14V31H31V8C31 8 31 7 30 7H24M16 6V8M26 12V14M26 18V20M11 6V8M6 6V8M16 12V14M11 12V14M6 12V14M16 18V20M11 18V20M6 18V20"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        <defs>
          <clipPath id="clip0_901_948">
            <rect width="32" height="32" fill="white" />
          </clipPath>
        </defs>
      </svg>
    </grid-cell>
    <div class="md:col-span-4 sm:col-span-1">
      <div class="flex justify-center" v-if="!teacherStatement.verdict">
        <verdict-btns-group class="mb-4" @submit-click="giveVerdict(route.params.id, 'C')"
          @reject-click="giveVerdict(route.params.id, 'R')"></verdict-btns-group>
      </div>
      <div v-else-if="teacherStatement.verdict === 'C'" class="mt-4 flex justify-center">
        <div>
          <h4
            class="px-4 py-2 text-[0.8rem] w-max font-medium bg-emerald-400 hover:bg-emerald-500 transition ease-in hover:ease-out duration-200 text-white dark:bg-emerald-700 border border-gray-200 dark:border-gray-700 rounded-lg select-none">
            Tassyklanyldy
          </h4>
        </div>

      </div>
      <div v-else-if="teacherStatement.verdict === 'R'" class="mt-4 flex justify-center">
        <h4
          class="px-4 py-2 text-[0.8rem] w-max font-medium bg-red-400 hover:bg-red-500 transition ease-in hover:ease-out duration-200 text-white dark:bg-pink-900 dark:hover:bg-pink-600 border border-gray-200 rounded-lg  dark:border-gray-700  select-none">
          Ret edildi
        </h4>
      </div>
    </div>
  </div>
  <teleport to="body">
    <div class="toast-container w-5/6 fixed top-25
       md:top-auto md:bottom-5 right-5 md:w-1/4 flex flex-col-reverse space-y-2">
      <TransitionGroup name="toast">
        <the-toast v-for="toast in toasts" :key="toast.id" :message="toast.message" :type="toast.type"
          :duration="toast.duration" :onClose="() => (toasts = toasts.filter((t) => t.id !== toast.id))"></the-toast>
      </TransitionGroup>
    </div>
  </teleport>
</template>
