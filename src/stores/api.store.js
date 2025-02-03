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
    highSchoolsResponse: [],
    deleteStatus: null,
    updateStatus: null,
    highSchool: {},
  }),
  actions: {
    async getAll() {
      try {
        const response = await axiosInstance.get('/high-schools/');
        this.highSchoolsResponse = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async getAllAdditional() {
      try {
        const response = await axiosInstance.get('/high-schools-with-additional/');
        this.highSchools = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async create(data) {
      try {
        const response = await axiosInstance.post('/create-high-school/', data);
      } catch (error) {
      }
    },
    async delete(id) {
      try {
        const response = await axiosInstance.delete(`/high-schools/${id}/`);
        this.deleteStatus = 'success';
      } catch (error) {
        this.deleteStatus = 'error';
      }
    },
    async get(id) {
      try {
        const response = await axiosInstance.get(`/high-schools/${id}/`);
        this.highSchool = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async put(id, data) {
      try {
        const response = await axiosInstance.put(`/update-high-school/${id}/`, data);
        this.updateStatus = 'success';
      } catch (error) {
        console.error('Error', error);
        this.updateStatus = 'error';
      }
    }
  }
});
