import {createRouter, createWebHistory, useRoute} from "vue-router";
import HomeView from "../views/HomeView.vue";
import {useAuthStore} from '@/stores/auth.store.js';
import guards from "@/router/guards.js";


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/login",
      name: "login-page",
      component: () => import('../views/LoginView.vue'),
      meta: {
        layout: 'EmptyLayout',
        title: "Giriş",
        adminRequired: false,
      },
      beforeEnter: guards.defaultGuard,
    },
    {
      path: "/",
      name: "home",
      component: HomeView,
      meta: {
        layout: 'MainLayout',
        title: "Baş sahypa",
        adminRequired: false,
      },
      beforeEnter: guards.authGuard,
    },
    {
      path: '/high-schools',
      name: 'high-schools',
      component: () => import('../views/HighSchoolViews/HighSchools.vue'),
      meta: {
        layout: 'MainLayout',
        title: "Ýokary okuw mekdepleri",
        adminRequired: true,
      },
      children: [
        {
          path: '',
          name: 'high-schools-list',
          component: () => import('../views/HighSchoolViews/HighSchoolsListView.vue'),
          meta: {
            layout: 'MainLayout',
            title: "Ýokary okuw mekdepleri",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
        {
          path: 'add',
          name: 'add-high-school',
          component: () => import('../views/HighSchoolViews/AddHighSchoolView.vue'),
          meta: {
            layout: 'MainLayout',
            title: 'Ýokary okuw mekdebi goşmak',
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
        {
          path: 'edit/:id',
          name: 'edit-high-school',
          component: () => import('../views/HighSchoolViews/EditHighSchoolView.vue'),
          meta: {
            layout: 'MainLayout',
            title: 'Ýokary okuw mekdebi üýtgetmek',
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        }
      ],
      beforeEnter: guards.authGuard,
    },
    {
      path: '/secondary-schools',
      name: 'secondary-schools',
      component: () => import('../views/SecondarySchoolsView.vue'),
      meta: {
        layout: "MainLayout",
        title: "Orta hünär mekdepleri",
        adminRequired: true,
      },
      beforeEnter: guards.authGuard,
    },
    {
      path: '/faculties',
      name: 'faculties',
      component: () => import('../views/FacultiesView.vue'),
      meta: {
        layout: 'MainLayout',
        title: "Fakultetler",
        adminRequired: false,
      },
      beforeEnter: guards.authGuard,
    },
    {
      path: '/403',
      name: 'page-403',
      component: () => import('../views/errors/Page403.vue'),
      meta: {
        layout: 'EmptyLayout',
        title: "403 | Rugsat ýok",
        adminRequired: false,
      },
      beforeEnter: guards.defaultGuard,
    },
  ],
});

export default router;
