import { ref } from 'vue';


export default function useConfirmModal() {

  const isModalOpen = ref(false);
  const header = ref('');
  const context = ref('');
  const openModal = (headerValue, text) => {
    isModalOpen.value = true;
    header.value = headerValue;
    context.value = text;
  }

  return {isModalOpen, openModal, header, context};
}
