<script setup>
import { useUserStore } from "@/stores/user";
import { computed } from "vue";

const userStore = useUserStore();
const setting = userStore.getSettings;
const showConfirm = ref(false);
</script>
<template></template>
