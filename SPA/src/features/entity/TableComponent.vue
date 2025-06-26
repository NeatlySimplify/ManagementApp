<script setup>
import { useUserStore } from "@/features/user/stores";
import { computed } from "vue";

const userStore = useUserStore();
const setting = userStore.getSettings;
const showConfirm = ref(false);
</script>
<template></template>
