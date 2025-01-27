<template>
  <router-link :to="link" v-slot="{ isActive }">
    <div class="block px-4 py-2 my-2 hover:translate-x-2 hover:transition rounded-lg ease-out hover:ease-in duration-200"
         :class="{'border-none dark:border-violet-500/50 border-1 bg-gradient-to-r from-blue-400 to-blue-500 dark:from-violet-600 dark:to-violet-500 text-white shadow-lg shadow-blue-300/50 dark:shadow-violet-500/50': isActive}">
      <slot name="default"></slot>
    </div>
  </router-link>
</template>
<script>
import {reactive, ref} from "vue";

export default {
  props: {
    link: {
      type: String,
      required: true,
    }
  },

  setup() {
    const link = ref(null);
    const linkClasses = reactive({})

    return {}
  }
}
</script>
