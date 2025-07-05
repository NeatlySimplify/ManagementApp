<script setup>
import { ref, watch } from "vue";
import api from "@/util/api";
import { RouterLink, useRouter } from "vue-router";
import FormInputComponent from "@/features/common/FormInputComponent.vue";
import PasswordComponent from "@/features/common/PasswordComponent.vue";

const router = useRouter();
const form = ref({
  name: "",
  tag_type: "",
  email: "",
  identification: "",
  password: "",
  confirm_pw: "",
});
const isLoading = ref(false);
const showYourself = ref(false);

watch(showYourself, (newValue) => {
  if (newValue === true) {
    form.value.tag_type = "individual";
  } else {
    form.value.tag_type = "organization";
  }
});

const onSubmit = async () => {
  if (form.value.password !== form.value.confirm_pw) {
    alert("Senhas não coincidem.");
    return;
  }
  const formData = {
    name: form.value.name,
    is_type: form.value.tag_type,
    email: form.value.email,
    password: form.value.password,
  };
  try {
    isLoading.value = true;
    const response = await api.post("api/auth/signup", formData);
    if (response.status === "ok") {
      alert(`Usuário ${form.value.name} registrado com sucesso!`);
      isLoading.value = false;
      router.push("root");
    }
  } catch (err) {
    console.error("Error on request:", err);
  }
};
</script>
<template>
  <div class="container">
    <form @submit.prevent="onSubmit">
      <FormInputComponent
        title="Nome:"
        :required="true"
        :isReadOnly="false"
        v-model:placeholder="form.name"
      ></FormInputComponent>

      <FormInputComponent
        title="E-mail:"
        :required="true"
        :isReadOnly="false"
        v-model:placeholder="form.email"
      ></FormInputComponent>

      <div class="border rounded border-start-0 border-end-0 my-3">
        <p class="form-label fs-4">Tipo de Usuário</p>
        <div class="btn-group d-flex mb-3" role="group">
          <input
            type="radio"
            @click="showYourself = true"
            class="btn-check btn-lg"
            name="options-outlined"
            id="individual-btn"
            autocomplete="off"
            :checked="showYourself"
          />
          <label class="btn btn-outline-secondary flex-grow-1 fs-5" for="individual-btn"
            >Individual</label
          >
          <input
            type="radio"
            @click="showYourself = false"
            class="btn-check btn-lg"
            name="options-outlined"
            id="organization-btn"
            autocomplete="off"
            :checked="!showYourself"
          />
          <label class="btn btn-outline-secondary flex-grow-1 fs-5" for="organization-btn"
            >Organização</label
          >
        </div>

        <div class="input-group input-group-lg my-3" v-if="!showYourself">
          <span class="input-group-text">CNPJ:</span>
          <input
            type="text"
            class="form-control"
            placeholder="CNPJ da Organização..."
            v-model="form.identification"
            required
            minlength="14"
            maxlength="18"
          />
        </div>

        <div class="input-group input-group-lg my-3" v-else>
          <span class="input-group-text">CPF:</span>
          <input
            type="text"
            class="form-control"
            v-model="form.identification"
            required
            minlength="11"
            maxlength="15"
          />
        </div>
      </div>

      <PasswordComponent label="Senha" v-model:passwordModel="form.password"></PasswordComponent>

      <PasswordComponent
        label="Confirme sua Senha"
        v-model:passwordModel="form.confirm_pw"
      ></PasswordComponent>

      <div class="mb-3 row">
        <div class="btn-group d-flex">
          <RouterLink
            class="btn btn-outline-danger btn-lg flex-grow-1"
            :to="{ name: 'root' }"
            :class="{ disabled: isLoading }"
          >
            Cancelar
          </RouterLink>
          <button type="submit" class="btn btn-outline-primary btn-lg flex-grow-1">
            Registrar <i v-if="isLoading" class="fa fa-spinner fa-spin"></i>
          </button>
        </div>
      </div>
    </form>
  </div>
</template>
