import { storeToRefs } from "pinia";
import { useDashboardStore } from "@/stores/api.store.js";
import { useUxStore } from "@/stores/ux.store";

export default function useDashboard() {
  const dashboardStore = useDashboardStore();
  const { data } = storeToRefs(dashboardStore);
  const uxStore = useUxStore();
  const { isLoading } = storeToRefs(uxStore);

  isLoading.value = true;
  dashboardStore.get().then(() => {
    isLoading.value = false;
  });
  return { data };
}
