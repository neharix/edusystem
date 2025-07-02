<template>
  <component :is="layout"></component>
  <toast-container></toast-container>
</template>

<script setup>
import { defineAsyncComponent, onBeforeMount, onMounted, ref, shallowRef, watch } from "vue";
import { useRoute } from "vue-router";
import LoaderLayout from "@/layouts/LoaderLayout.vue";
import { useAuthStore } from "@/stores/auth.store.js";
import router from "@/router/index.js";
import ToastContainer from "./components/ToastContainer.vue";

const layout = shallowRef(LoaderLayout)
const layoutName = ref('LoaderLayout');

const route = useRoute();
watch(route, (newValue, oldValue) => {
  if (newValue.meta.layout !== layoutName.value) {
    layoutName.value = newValue.meta.layout ?? 'LoaderLayout';

    layout.value = defineAsyncComponent(
      () =>
        import(`@/layouts/${layoutName.value}.vue`)
    );
  }
});

const authStore = useAuthStore();

onBeforeMount(() => {
  if (!localStorage.getItem("sidebarExpanded")) {
    localStorage.setItem("sidebarExpanded", "1");
  }
  if (!localStorage.getItem("rowsPerPage")) {
    localStorage.setItem("rowsPerPage", "10");
  }
})

onMounted(() => {
  if (authStore.token) {
    if (!authStore.user) {
      authStore.fetchUser();
    }
  } else {
    router.push("/login");
  }

});

</script>

<style>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type=number] {
  appearance: textfield;
}
</style>
