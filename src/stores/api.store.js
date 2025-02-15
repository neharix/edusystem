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
    createStatus: null,
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
        this.createStatus = 'success';
      } catch (error) {
        this.createStatus = 'error';
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
    faculties: [],
    facultiesAdditional: [],
    createStatus: null,
    createHighSchoolFacultiesStatus: null,
    updateStatus: null,
    deleteStatus: null,
    highSchoolFaculties: [],
    highSchoolExcFaculties: [],
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
    async getAll() {
      try {
        const response = await axiosInstance.get('/faculties/');
        this.faculties = response.data;
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
        this.createStatus = 'success';
      } catch (error) {
        this.createStatus = 'error';
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
        const response = await axiosInstance.get(`/high-school-faculties/${highSchoolId}/inc/`);
        this.highSchoolFaculties = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async getHighSchoolExcFaculties(highSchoolId) {
      try {
        const response = await axiosInstance.get(`/high-school-faculties/${highSchoolId}/exc/`);
        this.highSchoolExcFaculties = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async createHighSchoolFaculty(data) {
      try {
        const response = await axiosInstance.post("/create-high-school-faculties/", data);
        this.createHighSchoolFacultiesStatus = 'success';
      } catch (error) {
        this.createHighSchoolFacultiesStatus = 'error';
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
        const response = await axiosInstance.put(`/faculties/${id}/`, data);
        this.updateStatus = 'success';
      } catch (error) {
        console.error('Error', error);
        this.updateStatus = 'error';
      }
    },
  }
});



export const useDepartmentsStore =  defineStore({
  id: 'departments',
  state: () => ({
    department: {},
    departments: [],
    departmentsAdditional: [],
    createStatus: null,
    deleteStatus: null,
    removeStatus: null,
    updateStatus: null,
    createFacultyDepartmentsStatus: null,
    highSchoolDepartments: [],
    highSchoolExcDepartments: [],
  }),
  actions: {
    async get(id) {
      try {
        const response = await axiosInstance.get(`/departments/${id}/`);
        this.department = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async getAll() {
      try {
        const response = await axiosInstance.get('/departments/');
        this.departments = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async getAllAdditional() {
      try {
        const response = await axiosInstance.get('/departments-with-additional/');
        this.departmentsAdditional = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async create(data) {
      try {
        const response = await axiosInstance.post('/departments/', data);
        this.createStatus = 'success';
      } catch (error) {
        this.createStatus = 'error';
      }
    },
    async delete(id) {
      try {
        const response = await axiosInstance.delete(`/departments/${id}/`);
        this.deleteStatus = 'success';
      } catch (error) {
        this.deleteStatus = 'error';
      }
    },
    async put(id, data) {
      try {
        const response = await axiosInstance.put(`/departments/${id}/`, data);
        this.updateStatus = 'success';
      } catch (error) {
        console.error('Error', error);
        this.updateStatus = 'error';
      }
    },
    async getHighSchoolDepartments(highSchoolId) {
      try {
        const response = await axiosInstance.get(`/high-school-departments/${highSchoolId}/inc/`);
        this.highSchoolDepartments = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async getHighSchoolExcDepartments(highSchoolId) {
      try {
        const response = await axiosInstance.get(`/high-school-departments/${highSchoolId}/exc/`);
        this.highSchoolExcDepartments = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async createFacultyDepartment(data) {
      try {
        const response = await axiosInstance.post("/create-faculty-departments/", data);
        this.createFacultyDepartmentsStatus = 'success';
      } catch (error) {
        this.createFacultyDepartmentsStatus = 'error';
      }
    },
    async removeDepartment(facultyDepartmentId) {
      try {
        const response = await axiosInstance.get(`/remove/faculty-department/${facultyDepartmentId}/`);
        this.removeStatus = 'success';
      } catch (error) {
        console.error('Error', error);
        this.removeStatus = 'error';
      }
    }
  }
});



export const useSpecializationsStore =  defineStore({
  id: 'specializations',
  state: () => ({
    specialization: {},
    specializationsAdditional: [],
    createStatus: null,
    deleteStatus: null,
    removeStatus: null,
    updateStatus: null,
    createDepartmentSpecializationsStatus: null,
    highSchoolSpecializations: [],
    highSchoolExcSpecializations: [],
  }),
  actions: {
    async get(id) {
      try {
        const response = await axiosInstance.get(`/specializations/${id}/`);
        this.specialization = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async getAllAdditional() {
      try {
        const response = await axiosInstance.get('/specializations-with-additional/');
        this.specializationsAdditional = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async create(data) {
      let formData = {};
      if (data.classificator === 0) {
        formData = {name: data.name, abbreviation: data.abbreviation, classificator: null, degree: data.degree};
      } else {
        formData = {name: data.name, abbreviation: data.abbreviation, classificator: data.classificator, degree: data.degree};
      }
      try {
        const response = await axiosInstance.post('/specializations/', formData);
        this.createStatus = 'success';
      } catch (error) {
        this.createStatus = 'error';
        console.error('Error', error);
      }
    },
    async delete(id) {
      try {
        const response = await axiosInstance.delete(`/specializations/${id}/`);
        this.deleteStatus = 'success';
      } catch (error) {
        this.deleteStatus = 'error';
      }
    },
    async put(id, data) {
      let formData = {};
      if (data.classificator === 0) {
        formData = {name: data.name, abbreviation: data.abbreviation, degree: data.degree};
      } else {
        formData = {name: data.name, abbreviation: data.abbreviation, classificator: data.classificator, degree: data.degree};
      }

      try {
        const response = await axiosInstance.put(`/update-specialization/${id}/`, formData);
        this.updateStatus = 'success';
      } catch (error) {
        console.error('Error', error);
        this.updateStatus = 'error';
      }
    },
    async getHighSchoolSpecializations(highSchoolId) {
      try {
        const response = await axiosInstance.get(`/high-school-specializations/${highSchoolId}/inc/`);
        this.highSchoolSpecializations = response.data;
        console.log(response.data);
      } catch (error) {
        console.error('Error', error);
      }
    },
    async getHighSchoolExcSpecializations(highSchoolId) {
      try {
        const response = await axiosInstance.get(`/high-school-specializations/${highSchoolId}/exc/`);
        this.highSchoolExcSpecializations = response.data;
        console.log(response.data);
      } catch (error) {
        console.error('Error', error);
      }
    },
    async createDepartmentSpecialization(data) {
      try {
        const response = await axiosInstance.post("/create-department-specializations/", data);
        this.createDepartmentSpecializationsStatus = 'success';
      } catch (error) {
        this.createDepartmentSpecializationsStatus = 'error';
      }
    },
    async removeSpecialization(departmentSpecializationId) {
      try {
        const response = await axiosInstance.get(`/remove/department-specialization/${departmentSpecializationId}/`);
        this.removeStatus = 'success';
      } catch (error) {
        console.error('Error', error);
        this.removeStatus = 'error';
      }
    }
  }
});


export const useNationalizationsStore =  defineStore({
  id: 'nationalizations',
  state: () => ({
    nationalization: {},
    nationalizationsAdditional: [],
    createStatus: null,
    deleteStatus: null,
    updateStatus: null,
  }),
  actions: {
    async get(id) {
      try {
        const response = await axiosInstance.get(`/nationalities/${id}/`);
        this.nationalization = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async getAllAdditional() {
      try {
        const response = await axiosInstance.get('/nationalizations-with-additional/');
        this.nationalizationsAdditional = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async create(data) {
      try {
        const response = await axiosInstance.post('/nationalities/', data);
        this.createStatus = 'success';
      } catch (error) {
        this.createStatus = 'error';
        console.error('Error', error);
      }
    },
    async delete(id) {
      try {
        const response = await axiosInstance.delete(`/nationalities/${id}/`);
        this.deleteStatus = 'success';
      } catch (error) {
        this.deleteStatus = 'error';
      }
    },
    async put(id, data) {
      try {
        const response = await axiosInstance.put(`/nationalities/${id}/`, data);
        this.updateStatus = 'success';
      } catch (error) {
        console.error('Error', error);
        this.updateStatus = 'error';
      }
    },
  }
});


export const useCountriesStore =  defineStore({
  id: 'countries',
  state: () => ({
    country: {},
    countriesAdditional: [],
    createStatus: null,
    deleteStatus: null,
    updateStatus: null,
  }),
  actions: {
    async get(id) {
      try {
        const response = await axiosInstance.get(`/countries/${id}/`);
        this.country = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async getAllAdditional() {
      try {
        const response = await axiosInstance.get('/countries-with-additional/');
        this.countriesAdditional = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async create(data) {
      try {
        const response = await axiosInstance.post('/countries/', data);
        this.createStatus = 'success';
      } catch (error) {
        this.createStatus = 'error';
        console.error('Error', error);
      }
    },
    async delete(id) {
      try {
        const response = await axiosInstance.delete(`/countries/${id}/`);
        this.deleteStatus = 'success';
      } catch (error) {
        this.deleteStatus = 'error';
      }
    },
    async put(id, data) {
      try {
        const response = await axiosInstance.put(`/countries/${id}/`, data);
        this.updateStatus = 'success';
      } catch (error) {
        console.error('Error', error);
        this.updateStatus = 'error';
      }
    },
  }
});


export const useClassificatorsStore = defineStore({
  id: 'classificators',
  state: () => ({
    classificators: [],
    classificator: {},
    classificatorsAdditional: [],
    createStatus: null,
    deleteStatus: null,
    updateStatus: null,
  }),
  actions: {
    async get(id) {
      try {
        const response = await axiosInstance.get(`/classificators/${id}/`);
        this.classificator = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async getAll() {
      try {
        const response = await axiosInstance.get(`/classificators/`);
        this.classificators = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async getAllAdditional() {
      try {
        const response = await axiosInstance.get('/classificators-with-additional/');
        this.classificatorsAdditional = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async create(data) {
      try {
        const response = await axiosInstance.post('/classificators/', data);
        this.createStatus = 'success';
      } catch (error) {
        this.createStatus = 'error';
        console.error('Error', error);
      }
    },
    async delete(id) {
      try {
        const response = await axiosInstance.delete(`/classificators/${id}/`);
        this.deleteStatus = 'success';
      } catch (error) {
        this.deleteStatus = 'error';
      }
    },
    async put(id, data) {
      try {
        const response = await axiosInstance.put(`/classificators/${id}/`, data);
        this.updateStatus = 'success';
      } catch (error) {
        console.error('Error', error);
        this.updateStatus = 'error';
      }
    },
  }
});

export const useDegreesStore =  defineStore({
  id: 'degrees',
  state: () => ({
    degrees: [],
    degreesAdditional: [],
    degree: {},
    createStatus: null,
    deleteStatus: null,
    updateStatus: null,
  }),
  actions: {
    async get(id) {
      try {
        const response = await axiosInstance.get(`/degrees/${id}/`);
        this.degree = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async getAll() {
      try {
        const response = await axiosInstance.get(`/degrees/`);
        this.degrees = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async getAllAdditional() {
      try {
        const response = await axiosInstance.get('/degrees-with-additional/');
        this.degreesAdditional = response.data;
      } catch (error) {
        console.error('Error', error);
      }
    },
    async create(data) {
      try {
        const response = await axiosInstance.post('/degrees/', data);
        this.createStatus = 'success';
      } catch (error) {
        this.createStatus = 'error';
        console.error('Error', error);
      }
    },
    async delete(id) {
      try {
        const response = await axiosInstance.delete(`/degrees/${id}/`);
        this.deleteStatus = 'success';
      } catch (error) {
        this.deleteStatus = 'error';
      }
    },
    async put(id, data) {
      try {
        const response = await axiosInstance.put(`/degrees/${id}/`, data);
        this.updateStatus = 'success';
      } catch (error) {
        console.error('Error', error);
        this.updateStatus = 'error';
      }
    },
  }
});
