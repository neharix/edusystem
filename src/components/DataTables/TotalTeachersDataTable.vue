<script setup>
import { computed } from 'vue';


const props = defineProps(["data"])

const workload125 = computed(() => {
  let value = 0;
  for (let item of props.data) {
    value += item.workload_1_25
  }
  return value;
})

const workload100 = computed(() => {
  let value = 0;
  for (let item of props.data) {
    value += item.workload_1_00
  }
  return value;
})

const workload075 = computed(() => {
  let value = 0;
  for (let item of props.data) {
    value += item.workload_0_75
  }
  return value;
})

const workload050 = computed(() => {
  let value = 0;
  for (let item of props.data) {
    value += item.workload_0_50
  }
  return value;
})

const doctorDegree = computed(() => {
  let value = 0;
  for (let item of props.data) {
    value += item.doctor_degree
  }
  return value;
})

const candidateDegree = computed(() => {
  let value = 0;
  for (let item of props.data) {
    value += item.candidate_degree
  }
  return value;
})

const professor = computed(() => {
  let value = 0;
  for (let item of props.data) {
    value += item.professor
  }
  return value;
})

const docent = computed(() => {
  let value = 0;
  for (let item of props.data) {
    value += item.docent
  }
  return value;
})

const departmentHead = computed(() => {
  let value = 0;
  for (let item of props.data) {
    value += item.department_head
  }
  return value;
})

const professorJob = computed(() => {
  let value = 0;
  for (let item of props.data) {
    value += item.professor_job
  }
  return value;
})

const docentJob = computed(() => {
  let value = 0;
  for (let item of props.data) {
    value += item.docent_job
  }
  return value;
})

const seniorTeachers = computed(() => {
  let value = 0;
  for (let item of props.data) {
    value += item.senior_teachers
  }
  return value;
})

const teachers = computed(() => {
  let value = 0;
  for (let item of props.data) {
    value += item.teachers
  }
  return value;
})

const internTeachers = computed(() => {
  let value = 0;
  for (let item of props.data) {
    value += item.intern_teachers
  }
  return value;
})



</script>
<template>
  <div class="w-full mt-8">
    <div class="w-full overflow-x-auto border border-gray-300 dark:border-[#32237cef]">
      <table class="t-base table-auto w-full bg-white dark:bg-[#171131ef]">
        <thead>
          <tr>
            <th colspan="1" col="1">ÝOM</th>
            <th colspan="4" col="2">Iş ýüki</th>
            <th colspan="2" col="3"> Ylmy derejesi</th>
            <th colspan="2" col="3"> Ylmy ady</th>
            <th colspan="6" col="3"> Wezipesi</th>
          </tr>
          <tr class="lr">
            <th><span>Ýokary okuw mekdebi</span></th>
            <th><span>1.25</span></th>
            <th><span>1</span></th>
            <th><span>0.75</span> </th>
            <th><span>0.5</span> </th>
            <th><span>Ylymlaryň doktory</span></th>
            <th><span>Ylymlaryň kandidaty</span></th>
            <th><span>Professor</span></th>
            <th><span>Dosent</span></th>
            <th><span>Kafedra müdiri, professor</span></th>
            <th><span>Professor</span></th>
            <th><span>Dosent</span></th>
            <th><span>Uly mugallym</span></th>
            <th><span>Mugallym</span></th>
            <th><span>Mugallym-öwreniji</span></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in props.data" :key="item.id">
            <th class="text-wrap">{{ item.sender_abbr }}</th>
            <td>{{ item.workload_1_25 }}</td>
            <td>{{ item.workload_1_00 }}</td>
            <td>{{ item.workload_0_75 }}</td>
            <td>{{ item.workload_0_50 }}</td>
            <td>{{ item.doctor_degree }}</td>
            <td>{{ item.candidate_degree }}</td>
            <td>{{ item.professor }}</td>
            <td>{{ item.docent }}</td>
            <td>{{ item.department_head }}</td>
            <td>{{ item.professor_job }}</td>
            <td>{{ item.docent_job }}</td>
            <td>{{ item.senior_teachers }}</td>
            <td>{{ item.teachers }}</td>
            <td>{{ item.intern_teachers }}</td>
          </tr>
          <tr>
            <th><strong>Jemi</strong></th>
            <td><strong>{{ workload125 }}</strong></td>
            <td><strong>{{ workload100 }}</strong></td>
            <td><strong>{{ workload075 }}</strong></td>
            <td><strong>{{ workload050 }}</strong></td>
            <td><strong>{{ doctorDegree }}</strong></td>
            <td><strong>{{ candidateDegree }}</strong></td>
            <td><strong>{{ professor }}</strong></td>
            <td><strong>{{ docent }}</strong></td>
            <td><strong>{{ departmentHead }}</strong></td>
            <td><strong>{{ professorJob }}</strong></td>
            <td><strong>{{ docentJob }}</strong></td>
            <td><strong>{{ seniorTeachers }}</strong></td>
            <td><strong>{{ teachers }}</strong></td>
            <td><strong>{{ internTeachers }}</strong></td>
          </tr>

        </tbody>
      </table>
    </div>
  </div>
</template>
