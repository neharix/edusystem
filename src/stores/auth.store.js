import { defineStore } from 'pinia';
import router from '@/router/index.js'
import { fetchWrapper } from '@/helpers/fetch-wrapper.js';
import baseUrl from "@/helpers/base.js";
const url = baseUrl + "v1/token/";


export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    // initialize state from local storage to enable user to stay logged in
    accessToken: localStorage.getItem('access_token'),
    returnUrl: null
  }),
  actions: {
    async login(username, password) {
      const user = await fetchWrapper.post(url, { username, password });
      console.log("login", user);
      // update pinia state
      this.accessToken = user.access;
      // store user details and jwt in local storage to keep user logged in between page refreshes
      localStorage.setItem('access_token', user.access);

      // redirect to previous url or default to home page
      router.push(this.returnUrl || '/');
    },
    logout() {
      this.accessToken = null;
      localStorage.removeItem('access_token');
      router.push('/login');
    }
  }
});
