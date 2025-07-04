import { defineStore } from "pinia";
import axiosInstance from "@/api/axiosInstance.js";
import router from "@/router/index.js";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    role: "empty",
    token: localStorage.getItem("access_token") || null,
    isLoading: true,
    isLoginSuccessfully: "",
    notifications: [],
  }),
  getters: {
    isSuperuser: (state) => {
      try {
        return state.user.is_superuser;
      } catch {
        return false;
      }
    },
  },
  actions: {
    async login(credentials) {
      try {
        const response = await axiosInstance.post("/token/", credentials);
        this.token = response.data.access;

        localStorage.setItem("access_token", this.token);
        axiosInstance.defaults.headers[
          "Authorization"
        ] = `EDUSYSTEM ${this.token}`;
        this.isLoginSuccessfully = "success";
      } catch (error) {
        this.isLoginSuccessfully = "failed";
        console.error("Login failed", error);
      }
    },

    async logout() {
      this.token = null;
      this.user = null;
      this.role = "empty";
      this.notifications = [];
      localStorage.removeItem("access_token");
      delete axiosInstance.defaults.headers["Authorization"];
      router.push("/login");
    },

    async fetchUser() {
      try {
        const response = await axiosInstance.get("/user/");
        this.user = response.data;
        if (response.status === 200) {
          this.role = this.user.is_superuser ? "root" : "user";
        }
        this.isLoading = false;
        if (this.user.notifications) {
          this.notifications = this.user.notifications;
        }
      } catch (error) {
        console.error("Failed to fetch user", error);
      }
    },
  },
});
