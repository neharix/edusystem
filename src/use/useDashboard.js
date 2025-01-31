import {storeToRefs} from 'pinia';
import {useDashboardStore} from '@/stores/api.store.js';


export default function useDashboard() {

  const dashboardStore = useDashboardStore();
  const {data} = storeToRefs(dashboardStore);


  dashboardStore.get()
  return {data}
}
