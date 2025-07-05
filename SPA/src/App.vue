<script setup>
import { useRoute } from "vue-router";
import RouterView from "vue-router";
import SidebarComponent from "@/features/common/SidebarComponent.vue";

const route = useRoute();
const excludedRoutes = ["root", "register"];

const shouldLoadComponent = !excludedRoutes.includes(String(route.name));
</script>

<template>
  <SidebarComponent v-if="shouldLoadComponent"></SidebarComponent>
  <RouterView />
</template>
