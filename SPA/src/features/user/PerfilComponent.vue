<script setup>
import PasswordComponent from "@/features/common/PasswordComponent.vue";
import FormInputComponent from "@/features/common/FormInputComponent.vue";
import { useUserStore } from "@/features/user/store";
import { ref } from "vue";

const user = ref({});
const passwordPlaceholder = ref({});
const userStore = useUserStore();
user.value = { ...userStore.getUser };
</script>
<template>
  <form @submit.prevent>
    <FormInputComponent
      v-model:placeholder="user.name"
      title="Nome"
    />

    <FormInputComponent
      v-model:placeholder="user.email"
      title="E-mail"
    />

    <p class="fs-4">
      Mudar a senha:
    </p>
    <PasswordComponent
      v-model:password-model="passwordPlaceholder.new"
      label="Nova Senha:"
    />
    <PasswordComponent
      v-model:password-model="passwordPlaceholder.old"
      label="Antiga Senha:"
    />
  </form>
</template>
