<script setup>
const props = defineProps({
  statement: {
    type: Object,
    required: true,
  },
});
</script>
<template>
  <div class="space-y-4">
    <h3 class="text-xl font-bold mx-2 select-none">Talybyň okuwyny dikeltmek barada arza</h3>
    <div>
      <p class="info-label">Barada</p>
      <p class="info-content">{{
        statement.detail }}
      </p>
    </div>
  </div>
</template>
