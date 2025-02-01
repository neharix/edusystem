import {useAuthStore} from "@/stores/auth.store.js";


function defaultGuard (to, from, next) {
  let title = to.meta.title || "";
  document.title = title.length > 0 ? title + " | BMDU" : "BMDU";
  return next();
}

async function authGuard (to, from, next) {
  let title = to.meta.title || "";
  document.title = title.length > 0 ? title + " | BMDU" : "BMDU";

  const authStore = useAuthStore();
  await authStore.fetchUser();

  while (authStore.isLoading) {
    await new Promise((resolve) => setTimeout(resolve, 50));
  }

  if (to.meta.adminRequired && authStore.role !== "root") {
    return next("/403");
  }

  return next();
}

export default {authGuard, defaultGuard};
