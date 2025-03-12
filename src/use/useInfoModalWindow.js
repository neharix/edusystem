import { ref } from "vue";

export default function useInfoModal() {
  const isInfoModalOpen = ref(false);
  const infoHeader = ref("");
  const infoContext = ref("");
  const openInfoModal = (headerValue, text) => {
    isInfoModalOpen.value = true;
    infoHeader.value = headerValue;
    infoContext.value = text;
  };

  return { isInfoModalOpen, openInfoModal, infoHeader, infoContext };
}
