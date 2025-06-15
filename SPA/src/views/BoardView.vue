<script setup>
import { onMounted } from "vue";
import api from "@/api";
import { useUserStore } from "@/stores/user";
import ErrorComponent from "@/components/ErrorComponent.vue";

const compt = ref();
onMounted(() => {
  getData();
});
</script>

<template>
  <component :is="compt"></component>
</template>
