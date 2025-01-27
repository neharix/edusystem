<template>
  <component :is="layout + '-layout'"></component>
</template>

<script>
import { computed } from "vue";
import MainLayout from "./layouts/MainLayout.vue";
import { useRoute } from "vue-router";

export default {
  setup() {
    const route = useRoute();
    return { layout: computed(() => route.meta.layout) };
  },
  components: {
    MainLayout,
  },
};


</script>

<style scoped></style>
