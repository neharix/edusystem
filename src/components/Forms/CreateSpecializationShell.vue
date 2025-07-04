<template>
  <teleport to="#modals">
    <transition name="fade">
      <div v-if="isOpen" class="absolute z-[calc(100+1)] inset-0 flex items-center justify-center bg-black/75"
        @click.self="close">
        <transition name="modal">
          <div v-if="isOpen" class="bg-white dark:bg-[#171131] p-6 rounded-2xl shadow-xl w-1/2 relative">
            <button class="absolute right-5 top-5" @click="close"><svg xmlns="http://www.w3.org/2000/svg" class="w-6"
                viewBox="0 0 24 24">
                <rect width="24" height="24" fill="none" />
                <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M18 6L6 18M6 6l12 12" />
              </svg>
            </button>
            <h2 class="select-none dark:text-white mb-3 text-xl font-bold">Hünärleri birikdirme</h2>
            <Form @submit="onSubmit" :validation-schema="schema" v-slot="{ errors, isSubmitting }"
              class="space-y-4 my-4">
              <div>
                <label for="name" class="info-label">Ady</label>
                <Field name="name" type="name" id="name"
                  class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
                  :class="{ 'is-invalid': errors.name }"></Field>
                <div class="invalid-feedback select-none text-red-500 mb-2 mx-2 text-sm">{{ errors.name }}
                </div>
              </div>
              <div class="flex flex-wrap justify-center md:justify-end lg:justify-end">
                <button :disabled="isSubmitting"
                  class="flex w-50 px-4 py-2 my-2 justify-center rounded-lg border-none dark:border-violet-500/50 border-1 bg-gradient-to-r from-blue-400 to-blue-500 dark:from-violet-600 dark:to-violet-500 text-white hover:ease-in ease-out duration-200">
                  <the-spinner :class="{ hidden: !isSubmitting }"></the-spinner>
                  <span :class="{ hidden: isSubmitting }">Birleşdirmek</span>
                </button>
              </div>
              <div v-if="errors.apiError" class="text-center text-red-500 mt-3 mb-0 text-sm select-none">{{
                errors.apiError
                }}
              </div>
            </Form>
          </div>
        </transition>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
import * as Yup from 'yup';
import { useSpecializationsStore } from "@/stores/api.store";
import { storeToRefs } from "pinia";
import { Field, Form } from "vee-validate";
import TheSpinner from "@/components/TheSpinner.vue";
import { useUxStore } from "@/stores/ux.store";

const uxStore = useUxStore();
const specializationsStore = useSpecializationsStore();
const { joinStatus } = storeToRefs(specializationsStore);


const props = defineProps({
  isOpen: Boolean,
  specializations: Array,
});

const emit = defineEmits(['close', 'submit']);

const close = () => {
  emit('close');
};

const schema = Yup.object().shape({
  name: Yup.string().trim().required('Ady hökmän girizmeli'),
});

function onSubmit(values, { setErrors }) {
  const { name } = values;
  if (props.specializations.length > 1) {
    return specializationsStore.join({ name, specializations: props.specializations }).then(() => {
      if (joinStatus.value) {
        if (joinStatus.value === 'success') {
          uxStore.addToast('Umumy hünär üstünlikli hasaba alyndy', 'success');
        } else if (joinStatus.value === 'error') {
          uxStore.addToast('Birikdirme prosesinde ýalňyşlyk ýüze çykdy', 'error');
        }
      }
      joinStatus.value = null;
      emit('submit');
    }).catch(error => setErrors({ apiError: error }));
  } else {
    setErrors({ apiError: 'Birleşdirmeli hünär sany 1-den köp bolmaly' })
    return 0
  }
}

</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.modal-enter-active,
.modal-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: scale(0.9);
}
</style>
