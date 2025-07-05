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
    <FormInputComponent title="Nome" v-model:placeholder="user.name"></FormInputComponent>

    <FormInputComponent title="E-mail" v-model:placeholder="user.email"></FormInputComponent>

    <p class="fs-4">Mudar a senha:</p>
    <PasswordComponent
      label="Nova Senha:"
      v-model:passwordModel="passwordPlaceholder.new"
    ></PasswordComponent>
    <PasswordComponent
      label="Antiga Senha:"
      v-model:passwordModel="passwordPlaceholder.old"
    ></PasswordComponent>
  </form>
</template>
