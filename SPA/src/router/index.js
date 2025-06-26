import { createRouter, createWebHistory } from "vue-router";
import RootView from "@/views/RootView.vue";
import { useUserStore } from "@/features/user/store";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "root",
      component: RootView,
      meta: { guestOnly: true },
    },
    {
      path: "/register",
      name: "register",
      component: RootView,
      meta: { guestOnly: true },
    },
    {
      path: "/mfa",
      name: "mfa",
      component: RootView,
      meta: { guestOnly: true },
    },
    {
      path: "/forgot_password",
      name: "forgot_password",
      component: RootView,
      meta: { guestOnly: true },
    },
    {
      path: "/first-access",
      name: "first-access",
      component: () => import("@/views/FirstAccessView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/board",
      name: "board",
      component: () => import("@/views/BoardView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/entity",
      name: "entity",
      component: () => import("@/views/EntityView.vue"),
      meta: { requiresAuth: true },
    },
    // {
    //   path: '/app/user',
    //   name: 'user',
    //   component: () => import('@/views/UserView'),
    //   meta: { requiresAuth: true },
    // },
    // {
    //   path: '/app/unit',
    //   name: 'unit',
    //   component: () => import('@/views/UnitView'),
    //   meta: { requiresAuth: true },
    // },
    {
      path: "/:pathMatch(.*)*",
      name: "root",
      component: RootView, //fallback page component
      meta: { guestOnly: true },
    },
  ],
});

router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  const user = userStore.getUser;
  const auth = user.auth;
  console.log("Value of auth: ", auth);

  if (to.meta.requiresAuth && !auth) {
    next("/");
    console.log("blocked route");
  } else if (to.meta.guestOnly && auth) {
    next("/board");
    console.log("already autheticated");
  } else {
    next();
  }
});

export default router;
