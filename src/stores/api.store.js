import { defineStore } from 'pinia';
import baseUrl from "@/helpers/base.js";
import { fetchWrapper } from '@/helpers/fetch-wrapper.js';

const url = baseUrl + "v1/";


export const useUserStore =  defineStore({
  id: 'user',
  state: () => ({
    userData: {}
  }),
  actions: {
    async get() {
      this.data = { loading: true };
      fetchWrapper.get(url + "user/")
        .then(data => {
          this.userData = data
        })
        .catch(error => this.userData = { error })
    }
  }
});



export const useDashboardStore =  defineStore({
  id: 'root',
  state: () => ({
    data: {}
  }),
  actions: {
    async get() {
      this.data = { loading: true };
      fetchWrapper.get(url + "root-dashboard/")
        .then(data => {
          this.data = data
        })
        .catch(error => this.data = { error })
    }
  }
});


//
// export const useHighSchoolsStore =  defineStore({
//   id: 'root',
//   state: () => ({
//     data: {}
//   }),
//   actions: {
//     async get() {
//       this.data = { loading: true };
//       fetchWrapper.get(url + "high-schools/")
//         .then(data => {
//           this.data = data
//         })
//         .catch(error => this.data = { error })
//     }
//   }
// });
