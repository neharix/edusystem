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
    highSchoolAbout: {},
    deleteStatus: null,
    updateStatus: null,
    facultyRemoveStatus: null,
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
    async getAbout(id) {
      try {
        const response = await axiosInstance.get(`/high-school-about/${id}/`);
        this.highSchoolAbout = response.data;
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
    },
  }
});


export const useFacultiesStore =  defineStore({
  id: 'faculties',
  state: () => ({
    removeStatus: null,
    faculty: {},
    facultiesAdditional: [],
    updateStatus: null,
    deleteStatus: null,
    highSchoolFaculties: [],
  }),
  actions: {
    async get(id) {
      try {
        const response = await axiosInstance.get(`/faculties/${id}/`);
        this.faculty = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async getAllAdditional() {
      try {
        const response = await axiosInstance.get('/faculties-with-additional/');
        this.facultiesAdditional = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async create(data) {
      try {
        const response = await axiosInstance.post('/faculties/', data);
      } catch (error) {
      }
    },
    async delete(id) {
      try {
        const response = await axiosInstance.delete(`/faculties/${id}/`);
        this.deleteStatus = 'success';
      } catch (error) {
        this.deleteStatus = 'error';
      }
    },
    async getHighSchoolFaculties(highSchoolId) {
      try {
        const response = await axiosInstance.get(`/high-school-faculties/${highSchoolId}/`);
        this.highSchoolFaculties = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async removeFaculty(highSchoolId, facultyId) {
      try {
        const response = await axiosInstance.get(`/high-school/${highSchoolId}/faculty/${facultyId}/remove/`);
        this.removeStatus = 'success';
      } catch (error) {
        console.error('Error', error);
        this.removeStatus = 'error';
      }
    },
    async put(id, data) {
      try {
        const response = await axiosInstance.put(`/update-faculty/${id}/`, data);
        this.updateStatus = 'success';
      } catch (error) {
        console.error('Error', error);
        this.updateStatus = 'error';
      }
    },
  }
});
