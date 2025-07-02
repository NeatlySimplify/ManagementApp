<script setup>
import { RouterView, useRoute } from "vue-router";
import SidebarComponent from "@/features/common/SidebarComponent.vue";

const route = useRoute();
const excludedRoutes = ["root", "register"];

const shouldLoadComponent = !excludedRoutes.includes(route.name);
</script>

<template>
  <SidebarComponent v-if="shouldLoadComponent"></SidebarComponent>
  <RouterView />
</template>
