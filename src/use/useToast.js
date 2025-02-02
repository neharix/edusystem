import { ref } from 'vue';


export default function useToast() {
  const toasts = ref([]);


  const addToast = (message, type = "info", duration = 3000) => {
    const id = Date.now();
    toasts.value.push({id, message, type, duration});

    setTimeout(() => {
      toasts.value = toasts.value.filter((t) => t.id !== id);
    }, duration + 300);
  };


  return {toasts, addToast};
}
