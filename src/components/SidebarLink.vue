<template>
  <router-link :to="link" class="block px-4 py-2 rounded hover:bg-gray-100">
    <slot name="default"></slot>
  </router-link>
</template>
<script>
export default {
  props: {
    link: {
      type: String,
      required: true,
    }
  }
}
</script>
