<template>
  <VForm @submit="submitForm">
    <VField
      name="file"
      type="file"
      @change="handleFileChange"
      v-slot="{ field, errors }"
    >
      <input v-bind="field" type="file" @change="handleFileChange" accept=".xlsx" />
      <span v-if="errors.length">{{ errors[0] }}</span>
    </VField>
    <button type="submit">Отправить</button>
  </VForm>
</template>

<script setup>
import { ref } from "vue";
import { useForm, useField } from "vee-validate";
import * as yup from "yup";

const schema = yup.object({
  file: yup
    .mixed()
    .required("Файл обязателен")
    .test("fileType", "Только .xlsx файлы", (value) => {
      return value && value[0] && value[0].type === "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
    }),
});

const { handleSubmit } = useForm({ validationSchema: schema });
const { value: file, handleChange: handleFileChange } = useField("file");

const submitForm = handleSubmit(async () => {
  if (!file.value[0]) return;

  const formData = new FormData();
  formData.append("file", file.value[0]);

  try {
    const response = await fetch("https://your-api.com/upload", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error("Ошибка загрузки файла");

    console.log("Файл загружен:", await response.json());
  } catch (error) {
    console.error(error);
  }
});
</script>
