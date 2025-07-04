// eslint-disable no-extra-boolean-cast
// eslint-disable no-unused-vars
import { defineStore } from "pinia";
import axiosInstance from "@/api/axiosInstance.js";
import { reactive, ref } from "vue";
import { useRoute } from "vue-router";

export const useSpecialFunctionsStore = defineStore("special-functions", () => {
  const dump = ref(null);
  const dumpContentType = ref(null);
  async function getDump() {
    const response = await axiosInstance.get(`dumpdata/`, {
      responseType: "blob",
    });
    dump.value = response.data;
    dumpContentType.value = response.headers["Content-Type"];
  }

  return { getDump, dump, dumpContentType };
});

export const useDashboardStore = defineStore({
  id: "root",
  state: () => ({
    data: {},
    isLoading: false,
  }),
  actions: {
    clearData() {
      this.data = {};
    },
    async get() {
      try {
        const response = await axiosInstance.get("/dashboard/");
        this.data = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
  },
});

export const useHighSchoolsStore = defineStore({
  id: "high-schools",
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
        const response = await axiosInstance.get("/high-schools/");
        this.highSchoolsResponse = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async getAllAdditional() {
      try {
        const response = await axiosInstance.get(
          "/high-schools-with-additional/"
        );
        this.highSchools = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async create(data) {
      try {
        const response = await axiosInstance.post("/create-high-school/", data);
        this.createStatus = "success";
      } catch (error) {
        this.createStatus = "error";
      }
    },
    async delete(id) {
      try {
        const response = await axiosInstance.delete(`/high-schools/${id}/`);
        this.deleteStatus = "success";
      } catch (error) {
        this.deleteStatus = "error";
      }
    },
    async get(id) {
      try {
        const response = await axiosInstance.get(`/high-schools/${id}/`);
        this.highSchool = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async getAbout(id) {
      try {
        const response = await axiosInstance.get(`/high-school-about/${id}/`);
        this.highSchoolAbout = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async put(id, data) {
      try {
        const response = await axiosInstance.put(
          `/update-high-school/${id}/`,
          data
        );
        this.updateStatus = "success";
      } catch (error) {
        console.error("Error", error);
        this.updateStatus = "error";
      }
    },
  },
});

export const useFacultiesStore = defineStore({
  id: "faculties",
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
        console.error("Error", error);
      }
    },
    async getAll() {
      try {
        const response = await axiosInstance.get("/faculties/");
        this.faculties = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },

    async getAllViaUser() {
      try {
        const response = await axiosInstance.get(
          "/high-school-faculties-via-user/"
        );
        this.highSchoolFaculties = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async getAllAdditional() {
      try {
        const response = await axiosInstance.get("/faculties-with-additional/");
        this.facultiesAdditional = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async create(data) {
      try {
        const response = await axiosInstance.post("/faculties/", data);
        this.createStatus = "success";
      } catch (error) {
        this.createStatus = "error";
      }
    },
    async delete(id) {
      try {
        const response = await axiosInstance.delete(`/faculties/${id}/`);
        this.deleteStatus = "success";
      } catch (error) {
        this.deleteStatus = "error";
      }
    },
    async getHighSchoolFaculties(highSchoolId) {
      try {
        const response = await axiosInstance.get(
          `/high-school-faculties/${highSchoolId}/inc/`
        );
        this.highSchoolFaculties = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async getHighSchoolExcFaculties(highSchoolId) {
      try {
        const response = await axiosInstance.get(
          `/high-school-faculties/${highSchoolId}/exc/`
        );
        this.highSchoolExcFaculties = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async createHighSchoolFaculty(data) {
      try {
        const response = await axiosInstance.post(
          "/create-high-school-faculties/",
          data
        );
        this.createHighSchoolFacultiesStatus = "success";
      } catch (error) {
        this.createHighSchoolFacultiesStatus = "error";
      }
    },
    async removeFaculty(highSchoolId, facultyId) {
      try {
        const response = await axiosInstance.get(
          `/high-school/${highSchoolId}/faculty/${facultyId}/remove/`
        );
        this.removeStatus = "success";
      } catch (error) {
        console.error("Error", error);
        this.removeStatus = "error";
      }
    },
    async put(id, data) {
      try {
        const response = await axiosInstance.put(`/faculties/${id}/`, data);
        this.updateStatus = "success";
      } catch (error) {
        console.error("Error", error);
        this.updateStatus = "error";
      }
    },
  },
});

export const useDepartmentsStore = defineStore({
  id: "departments",
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
        console.error("Error", error);
      }
    },
    async getAll() {
      try {
        const response = await axiosInstance.get("/departments/");
        this.departments = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async getAllViaUser() {
      try {
        const response = await axiosInstance.get(
          "/high-school-departments-via-user/"
        );
        this.highSchoolDepartments = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async getAllAdditional() {
      try {
        const response = await axiosInstance.get(
          "/departments-with-additional/"
        );
        this.departmentsAdditional = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async create(data) {
      try {
        const response = await axiosInstance.post("/departments/", data);
        this.createStatus = "success";
      } catch (error) {
        this.createStatus = "error";
      }
    },
    async delete(id) {
      try {
        const response = await axiosInstance.delete(`/departments/${id}/`);
        this.deleteStatus = "success";
      } catch (error) {
        this.deleteStatus = "error";
      }
    },
    async put(id, data) {
      try {
        const response = await axiosInstance.put(`/departments/${id}/`, data);
        this.updateStatus = "success";
      } catch (error) {
        console.error("Error", error);
        this.updateStatus = "error";
      }
    },
    async getHighSchoolDepartments(highSchoolId) {
      try {
        const response = await axiosInstance.get(
          `/high-school-departments/${highSchoolId}/inc/`
        );
        this.highSchoolDepartments = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async getHighSchoolExcDepartments(highSchoolId) {
      try {
        const response = await axiosInstance.get(
          `/high-school-departments/${highSchoolId}/exc/`
        );
        this.highSchoolExcDepartments = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async createFacultyDepartment(data) {
      try {
        const response = await axiosInstance.post(
          "/create-faculty-departments/",
          data
        );
        this.createFacultyDepartmentsStatus = "success";
      } catch (error) {
        this.createFacultyDepartmentsStatus = "error";
      }
    },
    async removeDepartment(facultyDepartmentId) {
      try {
        const response = await axiosInstance.get(
          `/remove/faculty-department/${facultyDepartmentId}/`
        );
        this.removeStatus = "success";
      } catch (error) {
        console.error("Error", error);
        this.removeStatus = "error";
      }
    },
  },
});

export const useSpecializationsStore = defineStore("specializations", () => {
  const route = useRoute();

  const specialization = ref({});
  const specializationsAdditional = ref([]);
  const createStatus = ref(null);
  const deleteStatus = ref(null);
  const removeStatus = ref(null);
  const updateStatus = ref(null);
  const joinStatus = ref(null);
  const dataTablePageCount = ref(1);
  const createDepartmentSpecializationsStatus = ref(null);
  const highSchoolSpecializations = ref([]);
  const highSchoolExcSpecializations = ref([]);
  const currentPage = ref(1);
  const objectsCount = ref(0);

  async function get(id) {
    try {
      const response = await axiosInstance.get(`/specializations/${id}/`);
      specialization.value = response.data;
    } catch (error) {
      console.error("Error", error);
    }
  }
  async function getAllAdditional() {
    try {
      let order = route.query.order ? route.query.order : "asc";
      let column = route.query.column ? route.query.column : "name";
      let search = route.query.search ? route.query.search : false;

      let page = route.query.page ? route.query.page : 1;
      let pageSize = localStorage.getItem("rowsPerPage");
      let response = null;
      if (search) {
        response = await axiosInstance.get(
          "/specializations-with-additional/",
          {
            params: { page, page_size: pageSize, order, column, search },
          }
        );
      } else {
        response = await axiosInstance.get(
          "/specializations-with-additional/",
          {
            params: { page, page_size: pageSize, order, column },
          }
        );
      }

      currentPage.value = response.data.results.current_page;
      specializationsAdditional.value = response.data.results.data;
      dataTablePageCount.value = response.data.results.total_pages;
      objectsCount.value = response.data.count;
      console.log(response.data);
    } catch (error) {
      console.error("Error", error);
    }
  }
  async function getAllViaUser() {
    try {
      const response = await axiosInstance.get(
        "/high-school-specializations-via-user/"
      );
      this.highSchoolSpecializations = response.data;
    } catch (error) {
      console.error("Error", error);
    }
  }
  async function create(data) {
    let formData = {};
    if (data.classificator === 0) {
      formData = {
        name: data.name,
        abbreviation: data.abbreviation,
        classificator: null,
        degree: data.degree,
      };
    } else {
      formData = {
        name: data.name,
        abbreviation: data.abbreviation,
        classificator: data.classificator,
        degree: data.degree,
      };
    }
    try {
      const response = await axiosInstance.post("/specializations/", formData);
      createStatus.value = "success";
    } catch (error) {
      createStatus.value = "error";
      console.error("Error", error);
    }
  }
  async function _delete(id) {
    try {
      const response = await axiosInstance.delete(`/specializations/${id}/`);
      deleteStatus.value = "success";
    } catch (error) {
      deleteStatus.value = "error";
    }
  }
  async function put(id, data) {
    let formData = {};
    if (data.classificator === 0) {
      formData = {
        name: data.name,
        abbreviation: data.abbreviation,
        degree: data.degree,
      };
    } else {
      formData = {
        name: data.name,
        abbreviation: data.abbreviation,
        classificator: data.classificator,
        degree: data.degree,
      };
    }

    try {
      const response = await axiosInstance.put(
        `/update-specialization/${id}/`,
        formData
      );
      updateStatus.value = "success";
    } catch (error) {
      console.error("Error", error);
      updateStatus.value = "error";
    }
  }
  async function join(data) {
    try {
      const response = await axiosInstance.post("/join-specializations/", data);
      joinStatus.value = "success";
    } catch (error) {
      console.error("Error", error);
      joinStatus.value = "error";
    }
  }
  async function getHighSchoolSpecializations(highSchoolId) {
    try {
      const response = await axiosInstance.get(
        `/high-school-specializations/${highSchoolId}/inc/`
      );
      highSchoolSpecializations.value = response.data;
    } catch (error) {
      console.error("Error", error);
    }
  }
  async function getHighSchoolExcSpecializations(highSchoolId) {
    try {
      const response = await axiosInstance.get(
        `/high-school-specializations/${highSchoolId}/exc/`
      );
      highSchoolExcSpecializations.value = response.data;
    } catch (error) {
      console.error("Error", error);
    }
  }
  async function createDepartmentSpecialization(data) {
    try {
      const response = await axiosInstance.post(
        "/create-department-specializations/",
        data
      );
      createDepartmentSpecializationsStatus.value = "success";
    } catch (error) {
      createDepartmentSpecializationsStatus.value = "error";
    }
  }
  async function removeSpecialization(departmentSpecializationId) {
    try {
      const response = await axiosInstance.get(
        `/remove/department-specialization/${departmentSpecializationId}/`
      );
      removeStatus.value = "success";
    } catch (error) {
      console.error("Error", error);
      removeStatus.value = "error";
    }
  }
  return {
    specialization,
    specializationsAdditional,
    createStatus,
    deleteStatus,
    removeStatus,
    updateStatus,
    joinStatus,
    createDepartmentSpecializationsStatus,
    highSchoolSpecializations,
    highSchoolExcSpecializations,
    dataTablePageCount,
    currentPage,
    objectsCount,
    get,
    getAllViaUser,
    getAllAdditional,
    create,
    _delete,
    put,
    join,
    getHighSchoolSpecializations,
    getHighSchoolExcSpecializations,
    createDepartmentSpecialization,
    removeSpecialization,
  };
});

export const useNationalizationsStore = defineStore({
  id: "nationalizations",
  state: () => ({
    nationalization: {},
    nationalizations: [],
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
        console.error("Error", error);
      }
    },
    async getAll() {
      try {
        const response = await axiosInstance.get(`/nationalities/`);
        this.nationalizations = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async getAllAdditional() {
      try {
        const response = await axiosInstance.get(
          "/nationalizations-with-additional/"
        );
        this.nationalizationsAdditional = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async create(data) {
      try {
        const response = await axiosInstance.post("/nationalities/", data);
        this.createStatus = "success";
      } catch (error) {
        this.createStatus = "error";
        console.error("Error", error);
      }
    },
    async delete(id) {
      try {
        const response = await axiosInstance.delete(`/nationalities/${id}/`);
        this.deleteStatus = "success";
      } catch (error) {
        this.deleteStatus = "error";
      }
    },
    async put(id, data) {
      try {
        const response = await axiosInstance.put(`/nationalities/${id}/`, data);
        this.updateStatus = "success";
      } catch (error) {
        console.error("Error", error);
        this.updateStatus = "error";
      }
    },
  },
});

export const useCountriesStore = defineStore({
  id: "countries",
  state: () => ({
    country: {},
    countries: [],
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
        console.error("Error", error);
      }
    },
    async getAll(id) {
      try {
        const response = await axiosInstance.get(`/countries/`);
        this.countries = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async getAllAdditional() {
      try {
        const response = await axiosInstance.get("/countries-with-additional/");
        this.countriesAdditional = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async create(data) {
      try {
        const response = await axiosInstance.post("/countries/", data);
        this.createStatus = "success";
      } catch (error) {
        this.createStatus = "error";
        console.error("Error", error);
      }
    },
    async delete(id) {
      try {
        const response = await axiosInstance.delete(`/countries/${id}/`);
        this.deleteStatus = "success";
      } catch (error) {
        this.deleteStatus = "error";
      }
    },
    async put(id, data) {
      try {
        const response = await axiosInstance.put(`/countries/${id}/`, data);
        this.updateStatus = "success";
      } catch (error) {
        console.error("Error", error);
        this.updateStatus = "error";
      }
    },
  },
});

export const useRegionsStore = defineStore({
  id: "regions",
  state: () => ({
    region: {},
    regions: [],
    regionsAdditional: [],
    createStatus: null,
    deleteStatus: null,
    updateStatus: null,
  }),
  actions: {
    async get(id) {
      try {
        const response = await axiosInstance.get(`/regions/${id}/`);
        this.region = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async getAll(id) {
      try {
        const response = await axiosInstance.get(`/regions/`);
        this.regions = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async getAllAdditional() {
      try {
        const response = await axiosInstance.get("/regions-with-additional/");
        this.regionsAdditional = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async create(data) {
      try {
        const response = await axiosInstance.post("/regions/", data);
        this.createStatus = "success";
      } catch (error) {
        this.createStatus = "error";
        console.error("Error", error);
      }
    },
    async delete(id) {
      try {
        const response = await axiosInstance.delete(`/regions/${id}/`);
        this.deleteStatus = "success";
      } catch (error) {
        this.deleteStatus = "error";
      }
    },
    async put(id, data) {
      try {
        const response = await axiosInstance.put(`/regions/${id}/`, data);
        this.updateStatus = "success";
      } catch (error) {
        console.error("Error", error);
        this.updateStatus = "error";
      }
    },
  },
});

export const useClassificatorsStore = defineStore({
  id: "classificators",
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
        console.error("Error", error);
      }
    },
    async getAll() {
      try {
        const response = await axiosInstance.get(`/classificators/`);
        this.classificators = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async getAllAdditional() {
      try {
        const response = await axiosInstance.get(
          "/classificators-with-additional/"
        );
        this.classificatorsAdditional = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async create(data) {
      try {
        const response = await axiosInstance.post("/classificators/", data);
        this.createStatus = "success";
      } catch (error) {
        this.createStatus = "error";
        console.error("Error", error);
      }
    },
    async delete(id) {
      try {
        const response = await axiosInstance.delete(`/classificators/${id}/`);
        this.deleteStatus = "success";
      } catch (error) {
        this.deleteStatus = "error";
      }
    },
    async put(id, data) {
      try {
        const response = await axiosInstance.put(
          `/classificators/${id}/`,
          data
        );
        this.updateStatus = "success";
      } catch (error) {
        console.error("Error", error);
        this.updateStatus = "error";
      }
    },
  },
});

export const useDegreesStore = defineStore({
  id: "degrees",
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
        console.error("Error", error);
      }
    },
    async getAll() {
      try {
        const response = await axiosInstance.get(`/degrees/`);
        this.degrees = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async getAllAdditional() {
      try {
        const response = await axiosInstance.get("/degrees-with-additional/");
        this.degreesAdditional = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async create(data) {
      try {
        const response = await axiosInstance.post("/degrees/", data);
        this.createStatus = "success";
      } catch (error) {
        this.createStatus = "error";
        console.error("Error", error);
      }
    },
    async delete(id) {
      try {
        const response = await axiosInstance.delete(`/degrees/${id}/`);
        this.deleteStatus = "success";
      } catch (error) {
        this.deleteStatus = "error";
      }
    },
    async put(id, data) {
      try {
        const response = await axiosInstance.put(`/degrees/${id}/`, data);
        this.updateStatus = "success";
      } catch (error) {
        console.error("Error", error);
        this.updateStatus = "error";
      }
    },
  },
});

export const useStudentsStore = defineStore("students", () => {
  const students = ref([]);
  const studentsAdditional = ref([]);
  let student = ref({});
  let studentInfo = ref({});
  const expelledStudent = ref({});
  const neutralStudent = reactive({});
  const expelledStudentsAdditional = ref([]);

  const dataTablePageCount = ref(1);
  const excelForm = ref(null);
  const excelFormContentType = ref(null);
  const documentation = ref(null);
  const documentationContentType = ref(null);
  const createStatus = ref(null);
  const createSessionStatus = ref(null);
  const createSessionMistakes = ref([]);
  const deleteStatus = ref(null);
  const updateStatus = ref(null);

  const currentPage = ref(1);
  const objCount = ref(0);

  const route = useRoute();

  async function updateStudyYears() {
    try {
      const response = await axiosInstance.get(`/update-study-year/`);
    } catch (error) {
      console.error("Error", error);
    }
  }
  function resetMistakeVariables() {
    createSessionStatus.value = null;
    createSessionMistakes.value = [];
  }
  function resetExcelFormStates() {
    excelForm.value = null;
    excelFormContentType.value = null;
  }
  function resetDocumentationStates() {
    documentation.value = null;
    documentationContentType.value = null;
  }
  async function getExpelledStudent(id) {
    try {
      const response = await axiosInstance.get(`/expelled-students/${id}/`);
      expelledStudent.value = response.data;
    } catch (error) {
      console.error("Error", error);
    }
  }
  async function getNeutralInfo(id) {
    try {
      const response = await axiosInstance.get(`/neutral-students-info/${id}/`);
      studentInfo.value = response.data;
    } catch (error) {
      console.error("Error", error);
    }
  }
  async function getAllExpelledStudents() {
    try {
      const response = await axiosInstance.get(`/expelled-students/`);
      expelledStudentsAdditional.value = response.data;
    } catch (error) {
      console.error("Error", error);
    }
  }
  async function get(id) {
    try {
      const response = await axiosInstance.get(`/students/${id}/`);
      student.value = response.data;
      console.log(student);
    } catch (error) {
      console.error("Error", error);
    }
  }
  async function getInfo(id) {
    try {
      const response = await axiosInstance.get(`/students-info/${id}/`);
      studentInfo.value = response.data;
      console.log(studentInfo.value);
    } catch (error) {
      console.error("Error", error);
    }
  }
  async function getForm(highSchoolId, rowCount) {
    try {
      const response = await axiosInstance.get(
        `get-example/high-school/${highSchoolId}/row-count/${rowCount}/`,
        { responseType: "blob" }
      );
      excelForm.value = response.data;
      excelFormContentType.value = response.headers["Content-Type"];
    } catch (error) {
      console.error("Error", error);
    }
  }
  async function getFormForHighSchool(rowCount) {
    try {
      const response = await axiosInstance.get(
        `get-example/row-count/${rowCount}/`,
        { responseType: "blob" }
      );
      excelForm.value = response.data;
      excelFormContentType.value = response.headers["Content-Type"];
    } catch (error) {
      console.error("Error", error);
    }
  }
  async function getDocumentation() {
    try {
      const response = await axiosInstance.get(`get-documentation/`, {
        responseType: "blob",
      });
      documentation.value = response.data;
      documentationContentType.value = response.headers["Content-Type"];
    } catch (error) {
      console.error("Error", error);
    }
  }
  async function getAll() {
    try {
      const response = await axiosInstance.get(`/students/`);
      students.value = response.data;
    } catch (error) {
      console.error("Error", error);
    }
  }
  async function getAllAdditional() {
    try {
      let order = route.query.order ? route.query.order : "asc";
      let column = route.query.column ? route.query.column : "full_name";
      let search = route.query.search ? route.query.search : false;

      const filterFields = [
        "faculty",
        "department",
        "specialization",
        "gender",
        "region",
        "country",
        "nationality",
        "classificator",
        "degree",
        "study_year",
      ];

      let filterQuery = {};

      for (let i = 0; i < filterFields.length; i++) {
        if (!!route.query[filterFields[i]]) {
          filterQuery[filterFields[i]] = route.query[filterFields[i]];
        }
      }

      let page = route.query.page ? route.query.page : 1;
      let pageSize = localStorage.getItem("rowsPerPage");
      let response = null;
      if (search) {
        response = await axiosInstance.get("/students-with-additional/", {
          params: {
            page,
            page_size: pageSize,
            order,
            column,
            search,
            ...filterQuery,
          },
        });
      } else {
        response = await axiosInstance.get("/students-with-additional/", {
          params: {
            page,
            page_size: pageSize,
            order,
            column,
            ...filterQuery,
          },
        });
      }
      objCount.value = response.data.count;
      currentPage.value = response.data.results.current_page;
      studentsAdditional.value = response.data.results.data;
      dataTablePageCount.value = response.data.results.total_pages;
    } catch (error) {
      console.error("Error", error);
    }
  }
  async function getAllAdditionalWithQuery(key, value) {
    try {
      const response = await axiosInstance.get(
        `/students-with-additional/?${key}=${value}`
      );
      studentsAdditional.value = response.data;
    } catch (error) {
      console.error("Error", error);
    }
  }
  async function create(data) {
    try {
      const response = await axiosInstance.post("/import-students/", data, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      createSessionStatus.value = response.data.mistakes ? false : true;
      if (!createSessionStatus.value) {
        createSessionMistakes.value = response.data.mistakes;
      }
      createStatus.value = "success";
    } catch (error) {
      createStatus.value = "error";
      console.error("Error", error);
    }
  }
  async function validate(data) {
    try {
      const response = await axiosInstance.post(
        "/validate-student-form/",
        data,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      createSessionStatus.value = response.data.mistakes ? false : true;
      if (!createSessionStatus.value) {
        createSessionMistakes.value = response.data.mistakes;
      }
      createStatus.value = "success";
    } catch (error) {
      createStatus.value = "error";
      console.error("Error", error);
    }
  }
  async function _delete(id) {
    try {
      const response = await axiosInstance.delete(`/students/${id}/`);
      deleteStatus.value = "success";
    } catch (error) {
      deleteStatus.value = "error";
    }
  }
  async function put(id, data) {
    try {
      const response = await axiosInstance.put(`/students/${id}/`, data);
      updateStatus.value = "success";
    } catch (error) {
      console.error("Error", error);
      updateStatus.value = "error";
    }
  }
  return {
    students,
    studentsAdditional,
    student,
    studentInfo,
    expelledStudent,
    neutralStudent,
    expelledStudentsAdditional,
    excelForm,
    excelFormContentType,
    documentation,
    documentationContentType,
    createStatus,
    createSessionStatus,
    createSessionMistakes,
    deleteStatus,
    updateStatus,
    dataTablePageCount,
    currentPage,
    objCount,
    updateStudyYears,
    resetMistakeVariables,
    resetExcelFormStates,
    resetDocumentationStates,
    getExpelledStudent,
    getNeutralInfo,
    getAllExpelledStudents,
    get,
    getInfo,
    getForm,
    getFormForHighSchool,
    getDocumentation,
    getAll,
    getAllAdditional,
    getAllAdditionalWithQuery,
    create,
    validate,
    _delete,
    put,
  };
});

export const useGraduatesStore = defineStore({
  id: "graduates",
  state: () => ({
    graduatesAdditional: [],
    studentInfo: {},
  }),
  actions: {
    async getAllAdditional() {
      try {
        const response = await axiosInstance.get("/graduates-with-additional/");
        this.graduatesAdditional = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },

    async getInfo(id) {
      try {
        const response = await axiosInstance.get(`/graduates-info/${id}/`);
        this.studentInfo = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
  },
});

export const useExpulsionReasonsStore = defineStore({
  id: "expulsion-reasons",
  state: () => ({
    expulsionReason: {},
    expulsionReasons: [],
    createStatus: null,
    deleteStatus: null,
    updateStatus: null,
  }),
  actions: {
    async get(id) {
      try {
        const response = await axiosInstance.get(`/expulsion-reasons/${id}/`);
        this.expulsionReason = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async getAll(id) {
      try {
        const response = await axiosInstance.get(`/expulsion-reasons/`);
        this.expulsionReasons = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async create(data) {
      try {
        const response = await axiosInstance.post("/expulsion-reasons/", data);
        this.createStatus = "success";
      } catch (error) {
        this.createStatus = "error";
        console.error("Error", error);
      }
    },
    async delete(id) {
      try {
        const response = await axiosInstance.delete(
          `/expulsion-reasons/${id}/`
        );
        this.deleteStatus = "success";
      } catch (error) {
        this.deleteStatus = "error";
      }
    },
    async put(id, data) {
      try {
        const response = await axiosInstance.put(
          `/expulsion-reasons/${id}/`,
          data
        );
        this.updateStatus = "success";
      } catch (error) {
        console.error("Error", error);
        this.updateStatus = "error";
      }
    },
  },
});

export const useExpulsionRequestsStore = defineStore({
  id: "expulsion-requests",
  state: () => ({
    expulsionRequest: {},
    expulsionRequests: [],
    createStatus: null,
  }),
  actions: {
    async get(id) {
      try {
        const response = await axiosInstance.get(`/expulsion-requests/${id}/`);
        this.expulsionRequest = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async getAll() {
      try {
        const response = await axiosInstance.get(`/expulsion-requests/`);
        this.expulsionRequests = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async create(data) {
      try {
        const response = await axiosInstance.post("/expulsion-requests/", data);
        this.createStatus = "success";
      } catch (error) {
        this.createStatus = "error";
        console.error("Error", error);
      }
    },
  },
});

export const useReinstateRequestsStore = defineStore({
  id: "reinstate-requests",
  state: () => ({
    reinstateRequest: {},
    reinstateRequests: [],
    createStatus: null,
  }),
  actions: {
    async get(id) {
      try {
        const response = await axiosInstance.get(`/reinstate-requests/${id}/`);
        this.reinstateRequest = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async getAll() {
      try {
        const response = await axiosInstance.get(`/reinstate-requests/`);
        this.reinstateRequests = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async create(data) {
      try {
        const response = await axiosInstance.post("/reinstate-requests/", data);
        this.createStatus = "success";
      } catch (error) {
        this.createStatus = "error";
        console.error("Error", error);
      }
    },
  },
});

export const useStatementsStore = defineStore({
  id: "statements",
  state: () => ({
    statement: {},
    statements: [],
    confirmStatus: null,
    rejectStatus: null,
  }),
  actions: {
    async markAsViewed(id, objName) {
      try {
        const response = await axiosInstance.post(`/mark-as-viewed/${id}/`, {
          obj_name: objName,
        });
      } catch {
        console.error("Error", error);
      }
    },
    async markAsUnviewed(id, objName) {
      try {
        const response = await axiosInstance.post(`/mark-as-unviewed/${id}/`, {
          obj_name: objName,
        });
      } catch {
        console.error("Error", error);
      }
    },
    async confirmStatement(id, type) {
      try {
        const response = await axiosInstance.get(
          `/statements/${id}/${type}/confirm/`
        );
        this.confirmStatus = "success";
      } catch {
        this.confirmStatus = "error";
        console.error("Error", error);
      }
    },
    async rejectStatement(id, type) {
      try {
        const response = await axiosInstance.get(
          `/statements/${id}/${type}/reject/`
        );
        this.rejectStatus = "success";
      } catch {
        this.rejectStatus = "error";
        console.error("Error", error);
      }
    },
    async get(id, type) {
      try {
        const response = await axiosInstance.get(`/statements/${id}/${type}/`);
        this.statement = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
    async getAll() {
      try {
        const response = await axiosInstance.get(`/statements/`);
        this.statements = response.data;
      } catch (error) {
        console.error("Error", error);
      }
    },
  },
});

export const useDiplomasStore = defineStore({
  id: "diplomas",
  state: () => ({
    diplomaRequests: [],
    diplomaActions: [],
    diplomaRequestAdvanced: { null: true },
    highSchoolDiplomaActions: {},
    deactivateStatus: null,
    createStatus: null,
    updateStatus: null,
    submitStatus: null,
  }),
  actions: {
    async create(data) {
      try {
        const response = await axiosInstance.post(
          "/create-diploma-request/",
          data
        );
        this.createStatus = "success";
      } catch (error) {
        this.createStatus = "error";
        console.error("Error", error);
      }
    },
    async put(id, data) {
      try {
        const response = await axiosInstance.put(
          `/diploma-requests/${id}/`,
          data
        );
        this.updateStatus = "success";
      } catch (error) {
        this.updateStatus = "error";
        console.error("Error", error);
      }
    },
    async markAsUnviewed(id) {
      try {
        const response = await axiosInstance.post(
          `/mark-diploma-as-unviewed/${id}/`
        );
      } catch {
        console.error("Error", error);
      }
    },
    async giveVerdictDiplomaRequest(id, verdict) {
      try {
        const response = await axiosInstance.get(
          `/verdict-diploma-request/${id}/${verdict}/`
        );
      } catch (error) {
        console.error("Error", error);
      }
    },
    async update(id, data) {
      try {
        const response = await axiosInstance.post(
          `/update-diploma-request/${id}/`,
          data
        );
        this.updateStatus = "success";
      } catch (error) {
        this.updateStatus = "error";
        console.error("Error", error);
      }
    },
    async getAllForTable() {
      try {
        const response = await axiosInstance.get(`/diploma-requests-table/`);
        this.diplomaRequests = response.data;
      } catch {
        console.error("Error", error);
      }
    },
    async submitAction(id) {
      try {
        const response = await axiosInstance.get(
          `/submit-diploma-action/${id}/`
        );
        this.submitStatus = "success";
      } catch (error) {
        this.submitStatus = "error";
        console.error("Error", error);
      }
    },
    async submitReport(id) {
      try {
        const response = await axiosInstance.get(
          `/submit-diploma-report/${id}/`
        );
        this.submitStatus = "success";
      } catch (error) {
        this.submitStatus = "error";
        console.error("Error", error);
      }
    },
    async getActions() {
      try {
        const response = await axiosInstance.get(`/diploma-request-actions/`);
        this.diplomaActions = response.data;
      } catch {
        console.error("Error", error);
      }
    },
    async getHighSchoolActions(id) {
      try {
        const response = await axiosInstance.get(
          `/high-school-diploma-request-actions/${id}/`
        );
        this.highSchoolDiplomaActions = response.data;
      } catch {
        console.error("Error", error);
      }
    },
    async getDiplomaRequestAdvanced() {
      try {
        const response = await axiosInstance.get(`/diploma-request-by-user/`);
        this.diplomaRequestAdvanced = response.data;
      } catch {
        console.error("Error", error);
      }
    },
    async getDiplomaRequestAdvancedById(id) {
      try {
        const response = await axiosInstance.get(
          `/diploma-request-by-id/${id}/`
        );
        this.diplomaRequestAdvanced = response.data;
      } catch {
        console.error("Error", error);
      }
    },
    async getDiplomaRequestAdvancedByHighSchool(id) {
      try {
        const response = await axiosInstance.get(
          `/diploma-request-by-high-school/${id}/`
        );
        this.diplomaRequestAdvanced = response.data;
      } catch {
        console.error("Error", error);
      }
    },
    async deactivate(id) {
      try {
        const response = await axiosInstance.delete(`/diploma-requests/${id}/`);
        this.deactivateStatus = "success";
      } catch (error) {
        this.deactivateStatus = "error";
      }
    },
  },
});

export const useTeacherStatementsStore = defineStore({
  id: "teacher-statements",
  state: () => ({
    teacherStatements: [],
    teacherStatement: { null: true },
    deactivateStatus: null,
    createStatus: null,
    updateStatus: null,
    submitStatus: null,
  }),
  actions: {
    async create(data) {
      try {
        const response = await axiosInstance.post(
          "/create-teacher-statement/",
          data
        );
        this.createStatus = "success";
      } catch (error) {
        this.createStatus = "error";
        console.error("Error", error);
      }
    },
    async put(id, data) {
      try {
        const response = await axiosInstance.put(
          `/teacher-statements/${id}/`,
          data
        );
        this.updateStatus = "success";
      } catch (error) {
        this.updateStatus = "error";
        console.error("Error", error);
      }
    },
    async giveVerdictStatement(id, verdict) {
      try {
        const response = await axiosInstance.get(
          `/verdict-teacher-statement/${id}/${verdict}/`
        );
      } catch (error) {
        console.error("Error", error);
      }
    },
    async markAsUnviewed(id) {
      try {
        const response = await axiosInstance.post(
          `/mark-teacher-statement-as-unviewed/${id}/`
        );
      } catch {
        console.error("Error", error);
      }
    },
    async getAll() {
      try {
        const response = await axiosInstance.get(`/teacher-statements-table/`);
        this.teacherStatements = response.data;
      } catch {
        console.error("Error", error);
      }
    },
    async getTeacherStatementByUser() {
      try {
        const response = await axiosInstance.get(`/teacher-statement-by-user/`);
        this.teacherStatement = response.data;
      } catch {
        console.error("Error", error);
      }
    },

    async getTeacherStatementById(id) {
      try {
        const response = await axiosInstance.get(
          `/teacher-statement-by-id/${id}/`
        );
        this.teacherStatement = response.data;
      } catch {
        console.error("Error", error);
      }
    },
    async deactivate(id) {
      try {
        const response = await axiosInstance.delete(
          `/teacher-statements/${id}/`
        );
        this.deactivateStatus = "success";
      } catch (error) {
        this.deactivateStatus = "error";
      }
    },
  },
});

export const useFilterStore = defineStore({
  id: "filter",
  state: () => ({
    data: null,
    isLoading: false,
    isfilterOptionsInSession: sessionStorage.getItem("filterOptions")
      ? true
      : false,
    filterOptions: JSON.parse(sessionStorage.getItem("filterOptions")),
    filteredStudents: [],
  }),
  actions: {
    async getFilterOptions() {
      this.filterOptions = JSON.parse(sessionStorage.getItem("filterOptions"));
      this.isfilterOptionsInSession = sessionStorage.getItem("filterOptions")
        ? true
        : false;
    },
    async post(data) {
      try {
        this.isLoading = true;
        const response = await axiosInstance.post("/filter/", data);
        this.data = response.data.output;
        sessionStorage.setItem(
          "filterOptions",
          JSON.stringify(this.filterOptions)
        );
      } catch (error) {
        console.error("Error", error);
      } finally {
        this.isLoading = false;
      }
    },
    async get() {
      try {
        const response = await axiosInstance.get(`/filter/`);
        this.data = response.data;
        this.isLoading = false;
      } catch {
        console.error("Error", error);
      }
    },
    async getFilteredStudents(data, key, value) {
      try {
        const response = await axiosInstance.post(
          `/filtered-students/?${key}=${value}`,
          data
        );
        this.filteredStudents = response.data;
      } catch {
        console.error("Error", error);
      }
    },
  },
});
