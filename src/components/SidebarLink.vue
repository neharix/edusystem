<template>
  <router-link :to="link" v-slot="{ isActive }">
    <div class="flex items-center space-x-2 text-sm px-4 py-2 my-2 rounded-lg select-none"
         :class="{'border-none dark:border-violet-500/50 border-1 bg-gradient-to-r from-blue-400 to-blue-500 dark:from-violet-600 dark:to-violet-500 text-white shadow-md shadow-blue-300/50 dark:shadow-violet-500/50': isActive,
         'hover:dark:bg-violet-500 hover:bg-blue-300 hover:text-white transition duration-200 ease-in': !isActive }">
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
