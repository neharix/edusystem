import {createRouter, createWebHistory} from "vue-router";
import HomeView from "../views/HomeView.vue";
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
        },
        {
          path: 'view/:id',
          name: 'about-high-school',
          component: () => import('../views/HighSchoolViews/AboutHighSchool.vue'),
          meta: {
            layout: 'MainLayout',
            title: "Ýokary okuw mekdebi",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
          children: [
            {
              path: '',
              name: 'high-school',
              component: () => import('../views/HighSchoolViews/ViewHighSchoolView.vue'),
              beforeEnter: guards.authGuard,
              meta: {
                layout: 'MainLayout',
                title: "Ýokary okuw mekdebi",
                adminRequired: true,
              },
            },
            {
              path: 'faculties',
              name: 'high-school-faculties',
              component: () => import('../views/HighSchoolViews/HighSchoolFacultiesView.vue'),
              beforeEnter: guards.authGuard,
              meta: {
                layout: 'MainLayout',
                title: "Ýokary okuw mekdebiň fakultetleri",
                adminRequired: true,
              },
            },
            {
              path: 'specializations',
              name: 'high-school-specializations',
              component: () => import('../views/HighSchoolViews/HighSchoolSpecializationsView.vue'),
              beforeEnter: guards.authGuard,
              meta: {
                layout: 'MainLayout',
                title: "Ýokary okuw mekdebiň hünarleri",
                adminRequired: true,
              },
            },
            {
              path: 'departments',
              name: 'high-school-departments',
              component: () => import('../views/HighSchoolViews/HighSchoolDepartmentsView.vue'),
              beforeEnter: guards.authGuard,
              meta: {
                layout: 'MainLayout',
                title: "Ýokary okuw mekdebiň kafedralary",
                adminRequired: true,
              },
            },
          ],

        },

      ],
      beforeEnter: guards.authGuard,
    },
    {
      path: '/faculties',
      name: 'faculties',
      component: () => import('../views/FacultyViews/Faculties.vue'),
      meta: {
        layout: 'MainLayout',
        title: "Fakultetler",
        adminRequired: true,
      },
      children: [
        {
          path: '',
          name: 'faculties-list',
          component: () => import('../views/FacultyViews/FacultiesListView.vue'),
          meta: {
            layout: 'MainLayout',
            title: "Fakultetler",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
        {
          path: 'add',
          name: 'add-faculty',
          component: () => import('../views/FacultyViews/AddFacultyView.vue'),
          meta: {
            layout: 'MainLayout',
            title: 'Fakultet goşmak',
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
        {
          path: 'edit/:id',
          name: 'edit-faculty',
          component: () => import('../views/FacultyViews/EditFacultyView.vue'),
          meta: {
            layout: 'MainLayout',
            title: 'Fakulteti üýtgetmek',
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        }
      ],
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
