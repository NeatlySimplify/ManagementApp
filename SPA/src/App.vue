<script setup>
import { RouterView, useRoute } from "vue-router";
import SidebarComponent from "@/features/common/SidebarComponent.vue";
import {watch, ref} from "vue";

const route = useRoute();

const shouldLoadSidebar = ref(false);


watch(() => route.meta,
  (meta) => {
    if (route.matched.length === 0) {
      shouldLoadSidebar.value = false;
      return;
    }
    shouldLoadSidebar.value = meta?.skipSidebar;
  },
  { immediate: true })
</script>

<template>
  <SidebarComponent v-if="shouldLoadSidebar" />
  <RouterView />
</template>
