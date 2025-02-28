<script setup>
import { onBeforeMount, ref } from "vue";
import * as Yup from 'yup';
import { useExpulsionReasonsStore, useExpulsionRequestsStore } from "@/stores/api.store";
import { useAuthStore } from "@/stores/auth.store";
import { storeToRefs } from "pinia";
import { Field, Form } from "vee-validate";
import TheSpinner from "@/components/TheSpinner.vue";
import { useRoute } from "vue-router";
import TheToast from "@/components/TheToast.vue";
import useToast from "@/use/useToast.js";


const { toasts, addToast } = useToast();
const route = useRoute()
const expulsionReasonsStore = useExpulsionReasonsStore();
const { expulsionReasons } = storeToRefs(expulsionReasonsStore);
const expulsionRequestsStore = useExpulsionRequestsStore();
const { createStatus } = storeToRefs(expulsionRequestsStore)
const authStore = useAuthStore();
const { user } = storeToRefs(authStore);


const reason = ref(0);

const schema = Yup.object().shape({
  reason: Yup.number().required('Sebäp hökmän girizmeli'),
  detail: Yup.string().trim().required('Bellik, buýruk nomer,senesi hökmän görkezilmeli'),

});

onBeforeMount(() => {
  expulsionReasonsStore.getAll().then(() => {
    if (expulsionReasons.value.length > 0) {
      reason.value = expulsionReasons.value[0].id;
    }
  });
})

function onSubmit(values, { setErrors }) {
  const { reason, detail } = values;
  return expulsionRequestsStore.create({ student: route.params.id, sender: user.value.id, reason, detail }).then(() => {
    if (createStatus.value) {
      if (createStatus.value === 'success') {
        addToast('Arza üstünlikli hasaba alyndy', 'success');
      } else if (createStatus.value === 'error') {
        addToast('Hasaba alma prosesinde ýalňyşlyk ýüze çykdy', 'error');
      }
    }
    createStatus.value = null;
  }).catch(error => setErrors({ apiError: error }));
}


</script>
<template>
  <div class="tile my-8">
    <h3 class="text-xl font-bold mx-2 select-none">Talyby okuwdan boşatmak barada arza</h3>
    <Form @submit="onSubmit" :validation-schema="schema" v-slot="{ errors, isSubmitting }" class="space-y-4 my-4">
      <div>
        <label for="region" class="info-label">Okuwdan boşatmak sebäbi</label>
        <Field as="select" name="reason" id="reason"
          class="w-full border border-gray-300 dark:border-gray-700 rounded-md p-2 focus:outline-none select-none"
          v-model="reason">
          <option class="text-gray-600 dark:bg-[#171131ef] dark:text-white select-none"
            v-for="expulsionReason in expulsionReasons" :value="expulsionReason.id">{{ expulsionReason.name }}</option>
        </Field>
        <div class="invalid-feedback select-none text-red-500 my-2 text-sm">{{ errors.reason }}
        </div>
      </div>
      <div>
        <label for="detail" class="info-label">Okuwdan boşatmak barada (Bellik, buýruk nomer,senesi hökmän
          görkezilmeli)</label>
        <Field as="textarea" rows="1" name="detail" type="text" id="detail"
          class="w-full dark:text-gray-300 bg-transparent px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:ring focus:ring-blue-200 focus:outline-none"
          :class="{ 'is-invalid': errors.detail }"></Field>
        <div class="invalid-feedback select-none text-red-500 mb-2 mx-2 text-sm">{{ errors.detail }}
        </div>
      </div>
      <div class="flex flex-wrap justify-center md:justify-end lg:justify-end">
        <button :disabled="isSubmitting"
          class="flex w-50 px-4 py-2 my-2 justify-center rounded-lg border-none dark:border-violet-500/50 border-1 bg-gradient-to-r from-blue-400 to-blue-500 dark:from-violet-600 dark:to-violet-500 text-white hover:shadow-lg hover:shadow-blue-300/50 hover:ease-in ease-out duration-200 dark:hover:shadow-violet-500/50">
          <the-spinner :class="{ hidden: !isSubmitting }"></the-spinner>
          <span :class="{ hidden: isSubmitting }">Okuwdan boşat</span>
        </button>
      </div>
      <div v-if="errors.apiError" class="text-center text-red-500 mt-3 mb-0 text-sm select-none">{{
        errors.apiError
      }}
      </div>
    </Form>
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
