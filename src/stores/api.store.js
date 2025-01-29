import { defineStore } from 'pinia';
import baseUrl from "@/helpers/base.js";
import { fetchWrapper } from '@/helpers/fetch-wrapper.js';

const url = baseUrl + "v1/";

export const useDashboardStore =  defineStore({
  id: 'root',
  state: () => ({
    data: {}
  }),
  actions: {
    async get() {
      this.data = { loading: true };
      fetchWrapper.get(url + "root-dashboard/")
        .then(data => {
          console.log(data);
          this.data = data
        })
        .catch(error => this.data = { error })
    }
  }
});
