import {createRouter, createWebHistory} from "vue-router";
import HomeView from "../views/HomeView.vue";
import {useAuthStore} from '@/stores/auth.store.js';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/login",
      name: "login",
      component: () => import('../views/LoginView.vue'),
      meta: {
        layout: "empty",
        title: "Giriş"
      },
    },
    {
      path: "/",
      name: "home",
      component: HomeView,
      meta: {
        layout: "main",
        title: "Baş sahypa"
      },
    },
    {
      path: '/high-schools',
      name: 'high-schools',
      component: () => import('../views/HighSchoolsView.vue'),
      meta: {
        layout: "main",
        title: "Ýokary okuw mekdepleri",
      }
    },
    {
      path: '/secondary-schools',
      name: 'secondary-schools',
      component: () => import('../views/SecondarySchoolsView.vue'),
      meta: {
        layout: "main",
        title: "Orta hünär mekdepleri",
      }
    },
    {
      path: '/faculties',
      name: 'faculties',
      component: () => import('../views/FacultiesView.vue'),
      meta: {
        layout: "main",
        title: "Fakultetler",
      }
    },
  ],
});


router.beforeEach((to, from, next) => {
  let title = to.meta.title || "";
  document.title = title.length > 0 ? title + " | BMDU" : "BMDU";

  const publicPages = ['/login'];
  const authRequired = !publicPages.includes(to.path);
  const auth = useAuthStore();

  if (authRequired && !auth.accessToken) {
    auth.returnUrl = to.fullPath;
    next('/login');
  } else {
    next();
  }

});

export default router;
