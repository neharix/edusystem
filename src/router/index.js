import {createRouter, createWebHistory} from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
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
        title: "Ýokary okuw mekdepler",
      }
    },
  ],
});


router.beforeEach((to, from, next) => {
  let title = to.meta.title || "";
  document.title = title.length > 0  ? title + " | BMDU" : "BMDU";
  next();
});

export default router;
