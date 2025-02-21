import axios from "axios";
import { useAuthStore } from "@/stores/auth.store.js";
import router from "@/router/index.js";
import baseUrl from "@/api/base";

const axiosInstance = axios.create({
  baseURL: baseUrl,
  headers: {
    "Content-Type": "application/json",
  },
});

axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers["Authorization"] = `BMDU ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore();
      authStore.logout();

      if (router.currentRoute.value.name !== "login-page") {
        router.push("/login");
      }
    }
    return {};
  }
);

export default axiosInstance;
