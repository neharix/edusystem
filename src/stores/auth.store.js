import { defineStore } from 'pinia';
import axiosInstance from "@/api/axiosInstance.js"; // импортируем конфигурированный axios
import router from "@/router/index.js";


export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    role: 'empty',
    token: localStorage.getItem('access_token') || null,
    isLoading: true,
  }),
  actions: {
    async login(credentials) {
      try {
        const response = await axiosInstance.post('/token/', credentials);
        this.token = response.data.access;

        localStorage.setItem('access_token', this.token);
        axiosInstance.defaults.headers['Authorization'] = `BMDU ${this.token}`;
      } catch (error) {
        console.error('Login failed', error);
      }
    },

    async logout() {
      this.token = null;
      this.user = null;
      this.role = 'empty'
      localStorage.removeItem('access_token');
      delete axiosInstance.defaults.headers['Authorization'];
      router.push('/login');
    },

    async fetchUser() {
      try {
        const response = await axiosInstance.get('/user/');
        this.user = response.data;
        if (response.status === 200) {
          this.role = this.user.is_superuser ? 'root' : 'user';
        }
        this.isLoading = false;
      } catch (error) {
        console.error('Failed to fetch user', error);
      }
    },
  },
});
