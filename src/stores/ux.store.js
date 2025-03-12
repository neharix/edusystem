import { defineStore } from "pinia";

export const useUxStore = defineStore("ux", {
  state: () => ({
    theme: localStorage.getItem("theme") || "light",
    sidebarExpand: localStorage.getItem("sidebarExpanded") || "1",
    sidebarHover: false,
    isLoading: false,
  }),
  actions: {
    toggleSidebar() {
      this.sidebarExpand = this.sidebarExpand === "1" ? "0" : "1";
      localStorage.setItem(
        "sidebarExpanded",
        String(Number(this.sidebarExpand))
      );
    },
    minimizeSidebar() {
      this.sidebarExpand = "0";
      localStorage.setItem(
        "sidebarExpanded",
        String(Number(this.sidebarExpand))
      );
    },
    expandSidebar() {
      this.sidebarExpand = "1";
      localStorage.setItem(
        "sidebarExpanded",
        String(Number(this.sidebarExpand))
      );
    },
    mouseOverSidebar() {
      this.sidebarHover = true;
    },
    mouseLeaveSidebar() {
      this.sidebarHover = false;
    },
  },
  getters: {
    sidebarExpanded: (state) => state.sidebarExpand === "1",
  },
});
