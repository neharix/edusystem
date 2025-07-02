<script setup>
import GridCell from '@/components/GridCell.vue';
import { useDiplomasStore } from '@/stores/api.store';
import { storeToRefs } from 'pinia';
import { onMounted } from 'vue';
import router from '@/router';
import { useUxStore } from '@/stores/ux.store';
import TheSpinner from '@/components/TheSpinner.vue';



const diplomasStore = useDiplomasStore();
const { diplomaRequestAdvanced, createStatus, updateStatus } = storeToRefs(diplomasStore);
const uxStore = useUxStore();
const { addToast } = storeToRefs(uxStore)

onMounted(() => {
  if (createStatus.value) {
    if (createStatus.value === 'success') {
      addToast('Arza üstünlikli hasaba alyndy', 'success');
    } else if (createStatus.value === 'error') {
      addToast('Hasaba alma prosesinde ýalňyşlyk ýüze çykdy', 'error');
    }
  }
  createStatus.value = null;
  if (updateStatus.value) {
    if (updateStatus.value === 'success') {
      addToast('Hasabat üstünlikli täzelendi. Üýtgeşmeler dolandyryjy tassyklandan soňra işe girer', 'success');
    } else if (updateStatus.value === 'error') {
      addToast('Prosesde ýalňyşlyk ýüze çykdy', 'error');
    }
  }
  updateStatus.value = null;

  uxStore.isLoading = true;
  diplomasStore.getDiplomaRequestAdvanced().then(() => {
    uxStore.isLoading = false;
  });
})


</script>
<template>
  <div v-if="uxStore.isLoading"
    class="flex w-full h-[58vh] items-center justify-center dark:bg-[#171131ef] bg-white rounded-lg border border-gray-200 dark:border-[#36314e]">
    <the-spinner class="w-24"></the-spinner>
  </div>
  <div v-else>
    <div class="bg-yellow-200/50 p-4 rounded-xl border border-yellow-500 dark:border-yellow-300 mb-8"
      v-if="!diplomaRequestAdvanced.null && !diplomaRequestAdvanced.verdict">
      <h4 class="text-yellow-500 dark:text-yellow-300 select-none">Arza heniz dolandyryjy tarapyndan tassyklanylmady
      </h4>
    </div>
    <div class="grid md:grid-cols-4 sm:grid-cols-2 gap-8" v-if="!diplomaRequestAdvanced.null">
      <grid-cell label="Başdaky talap edilen diplom sany" :custom-classes="'md:col-span-2 sm:col-span-1'"
        :data-value="diplomaRequestAdvanced.original_requested_quantity"
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
      <div
        class="bg-white dark:bg-[#171131ef] shadow-md rounded-lg flex justify-between items-center p-4 md:col-span-2 sm:col-span-1">
        <div>
          <div class="text-sm my-2 select-none">
            Umumy talap edilen diplom sany
          </div>

          <div class="mt-2 select-none font-bold text-lg"
            v-if="diplomaRequestAdvanced.original_requested_quantity === diplomaRequestAdvanced.total_requested_quantity">
            {{ diplomaRequestAdvanced.total_requested_quantity }}
          </div>
          <div class="mt-2 select-none" v-else><span class="text-base">{{
            diplomaRequestAdvanced.original_requested_quantity }} +
              {{
                diplomaRequestAdvanced.total_requested_quantity - diplomaRequestAdvanced.original_requested_quantity
              }} = </span><span class="font-bold text-lg">{{ diplomaRequestAdvanced.total_requested_quantity
              }}</span></div>
        </div>
        <div>
          <div class="w-12 h-12 rounded-full flex justify-center items-center bg-green-200 dark:bg-green-500/75">
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
          </div>
        </div>
      </div>
      <grid-cell label='"Tapawutlanan" diplom sany' :custom-classes="'md:col-span-2 sm:col-span-1'"
        :data-value="diplomaRequestAdvanced.honor_diplomas_quantity" icon-bg-class="bg-green-200 dark:bg-green-500/75">
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
      <grid-cell label="Adaty diplom sany" :custom-classes="'md:col-span-2 sm:col-span-1'"
        :data-value="diplomaRequestAdvanced.simple_diplomas_quantity" icon-bg-class="bg-green-200 dark:bg-green-500/75">
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
      <grid-cell label="Iki ýyl iş" :data-value="diplomaRequestAdvanced.two_year_work_off"
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
      <grid-cell label="Ýogalan" :data-value="diplomaRequestAdvanced.died"
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
      <grid-cell label="Daşary ýurda giden" :data-value="diplomaRequestAdvanced.went_abroad"
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
      <grid-cell label="Gaýry sebäpler" :data-value="diplomaRequestAdvanced.other_reasons"
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
      <grid-cell label="Ätiýaçdaky diplomlar" :whole-line="true" :data-value="diplomaRequestAdvanced.spare_diplomas"
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

    <div v-else
      class="flex w-full h-[58vh] items-center justify-center border-dashed border-4 rounded-2xl border-gray-400 bg-gray-200 dark:border-gray-700 dark:bg-[#242035]">
      <div>
        <h2 class="text-lg md:text-2xl font-semibold text-center select-none">Hasabat heniz döredilmedi</h2>
        <div class="flex justify-center my-4">
          <button @click="router.push('/diplomas/add')" class="link-active px-4 py-2 rounded-lg">Hasabat
            döretmek</button>
        </div>
      </div>
    </div>
  </div>
</template>
