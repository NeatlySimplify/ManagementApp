<script setup>
import { computed } from "vue";
import LoginComponent from "@/features/auth/LoginComponent.vue";
import RegisterComponent from "@/features/auth/RegisterComponent.vue";
import { useRoute } from "vue-router";

const route = useRoute();

const formComponent = computed(() => {
  switch (route.name) {
    case "root":
      return {
        title: "Login Form",
        component: LoginComponent,
      };
    case "register":
      return {
        title: "Register Form",
        component: RegisterComponent,
      };
    default:
      return {
        title: "Unknown Page",
        component: null,
      };
  }
});
const title = computed(() => formComponent.value.title);
const form = computed(() => formComponent.value.component);
</script>

<template>
  <div class="fullscreen-image d-flex align-items-center justify-content-center">
    <div
      class="col-12 col-md-8 mt-5 text-end text-sm-center position-absolute top-0 start-50 rounded-5 translate-middle-x"
      style="background-color: #ffffff"
    >
      <h1 class="text-center fs-2">{{ title }}</h1>
      <component :is="form"></component>
    </div>
  </div>
</template>
<style scoped>
.fullscreen-image {
  background-position: center;
  background-attachment: fixed;
  margin: 0;
  background-image: url("@/assets/maxresdefault.jpg"); /* Replace with your image path */
  background-size: cover;
  background-repeat: no-repeat;
}
</style>
