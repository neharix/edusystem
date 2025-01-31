import {defineStore} from 'pinia';
import baseUrl from "@/helpers/base.js";
import axiosInstance from "@/api/axiosInstance.js";

const url = baseUrl + "v1/";




export const useDashboardStore =  defineStore({
  id: 'root',
  state: () => ({
    data: {}
  }),
  actions: {
    async get() {
      try {
        const response = await axiosInstance.get('/dashboard/');
        this.data = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    }
  }
});



export const useHighSchoolsStore =  defineStore({
  id: 'high-schools',
  state: () => ({
    highSchools: []
  }),
  actions: {
    async getAdditional() {
      try {
        const response = await axiosInstance.get('/high-schools-with-additional/');
        this.highSchools = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    }
  }
});
