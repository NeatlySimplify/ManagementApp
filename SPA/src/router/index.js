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
      path: "/entity/:id",
      name: "entity",
      component: () => import("@/views/EntityView.vue"),
      meta: { requiresAuth: true },
      props: (route) => ({
        id: route.params.id ?? null,
        back: route.query.back ?? null,
      }),
    },
    {
      path: "/entity/filter",
      name: "entityFiltered",
      component: () => import("@/views/EntityView.vue"),
      meta: { requiresAuth: true },
      props: (route) => ({
        filter: route.query.filter ?? null,
        term: route.query.term ?? null,
      }),
    },
    {
      path: "/record/:id",
      name: "record",
      component: () => import("@/views/RecordView.vue"),
      meta: { requiresAuth: true },
      props: (route) => ({
        id: route.params.id ?? null,
        back: route.query.back ?? null,
      }),
    },
    {
      path: "/record/filter",
      name: "recordFiltered",
      component: () => import("@/views/RecordView.vue"),
      meta: { requiresAuth: true },
      props: (route) => ({
        filter: route.query.filter ?? null,
        term: route.query.term ?? null,
      }),
    },
    {
      path: "/movement/:id",
      name: "movement",
      component: () => import("@/views/MovementView.vue"),
      meta: { requiresAuth: true },
      props: (route) => ({
        id: route.params.id ?? null,
        back: route.query.back ?? null,
      }),
    },
    {
      path: "/payment",
      name: "paymentFiltered",
      component: () => import("@/views/PaymentView.vue"),
      meta: { requiresAuth: true },
      props: (route) => ({
        term: route.query.term ?? null,
      }),
    },
    {
      path: "/payment/:id",
      name: "payment",
      component: () => import("@/views/PaymentView.vue"),
      meta: { requiresAuth: true },
      props: (route) => ({
        id: route.params.id ?? null,
      }),
    },
    {
      path: "/scheduler/:id",
      name: "scheduler",
      component: () => import("@/views/ScheduleView.vue"),
      meta: { requiresAuth: true },
      props: (route) => ({
        id: route.params.id ?? null,
        back: route.query.back ?? null,
      }),
    },
    {
      path: "/scheduler/filter",
      name: "schedulerFiltered",
      component: () => import("@/views/SchedulerView.vue"),
      meta: { requiresAuth: true },
      props: (route) => ({
        filter: route.query.filter ?? null,
        term: route.query.term ?? null,
      }),
    },
    {
      path: "/user",
      name: "user",
      component: () => import("@/views/UserView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/user/settings",
      name: "settings",
      component: () => import("@/views/SettingsView.vue"),
      meta: { requiresAuth: true },
    },
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
