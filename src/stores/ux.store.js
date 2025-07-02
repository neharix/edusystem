import { defineStore } from "pinia";
import { computed, ref } from "vue";

export const useUxStore = defineStore("ux", () => {
  const theme = ref(localStorage.getItem("theme") || "light");
  const sidebarExpand = ref(localStorage.getItem("sidebarExpanded") || "1");
  const sidebarHover = ref(false);
  const isLoading = ref(false);
  const toasts = ref([]);

  function toggleSidebar() {
    sidebarExpand.value = sidebarExpand.value === "1" ? "0" : "1";
    localStorage.setItem(
      "sidebarExpanded",
      String(Number(sidebarExpand.value))
    );
  }
  function minimizeSidebar() {
    sidebarExpand.value = "0";
    localStorage.setItem(
      "sidebarExpanded",
      String(Number(sidebarExpand.value))
    );
  }
  function expandSidebar() {
    sidebarExpand.value = "1";
    localStorage.setItem(
      "sidebarExpanded",
      String(Number(sidebarExpand.value))
    );
  }
  function mouseOverSidebar() {
    sidebarHover.value = true;
  }
  function mouseLeaveSidebar() {
    sidebarHover.value = false;
  }
  const sidebarExpanded = computed(() => {
    return sidebarExpand.value === "1";
  });

  function addToast(message, _type) {
    const id = toasts.value.length;
    toasts.value.push({ id, message, _type });
    setTimeout(() => {
      try {
        toasts.value.splice(
          toasts.value[
            toasts.value.indexOf(toasts.value.find((obj) => obj.id === id))
          ],
          1
        );
      } catch (e) {
        console.warn(e);
      }
    }, 5000);
  }
  function deleteToast(id) {
    toasts.value.splice(
      toasts.value[
        toasts.value.indexOf(toasts.value.find((obj) => obj.id === id))
      ],
      1
    );
  }

  return {
    theme,
    sidebarExpand,
    sidebarExpanded,
    sidebarHover,
    isLoading,
    toasts,
    toggleSidebar,
    minimizeSidebar,
    expandSidebar,
    mouseLeaveSidebar,
    mouseOverSidebar,
    addToast,
    deleteToast,
  };
});
