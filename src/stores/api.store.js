import {defineStore} from 'pinia';
import axiosInstance from "@/api/axiosInstance.js";


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
    highSchools: [],
    deleteStatus: null,

  }),
  actions: {
    async getAdditional() {
      try {
        const response = await axiosInstance.get('/high-schools-with-additional/');
        this.highSchools = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async createHighSchool(data) {
      try {
        const response = await axiosInstance.post('/create-high-school/', data);
      } catch (error) {
      }
    },
    async deleteHighSchool(id) {
      try {
        const response = await axiosInstance.delete(`/high-schools/${id}/`);
        this.deleteStatus = 'success';
      } catch (error) {
        this.deleteStatus = 'error';
      }
    }
  }
});
