<script setup>
import { ref, watch, computed } from "vue";
import api from "@/util/api";
import { RouterLink, useRouter } from "vue-router";

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

const passwordValid = computed(() =>
  /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,20}$/.test(form.value.password),
);

watch(showYourself, (newValue) => {
  if (newValue === true) {
    form.value.tag_type = "individual";
  } else {
    form.value.tag_type = "organization";
  }
});

const onSubmit = async () => {
  if (form.value.password !== form.value.confirm_pw) {
    alert("Passwords do not match.");
    return;
  }
  const formData = {
    name: form.value.name,
    tag_type: form.value.tag_type,
    email: form.value.email,
    document: form.value.identification,
    password: form.value.password,
  };
  try {
    isLoading.value = true;
    const response = await api.post("api/auth/register", formData);
    if (response.status === "success") {
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
      <div class="input-group input-group-lg my-3">
        <span class="input-group-text">Nome:</span>
        <input
          type="text"
          class="form-control"
          placeholder="Nome do Usuário..."
          v-model="form.name"
          required
          minlength="4"
          maxlength="100"
        />
      </div>
      <div class="input-group input-group-lg my-3">
        <span class="input-group-text">Email:</span>
        <input
          type="text"
          class="form-control"
          v-model="form.email"
          required
          minlength="4"
          maxlength="100"
        />
      </div>

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

      <div class="mb-3 row">
        <div class="col-12 col-md-6">
          <div class="input-group input-group-lg my-3">
            <span class="input-group-text">Senha:</span>
            <input
              type="password"
              class="form-control"
              v-model="form.password"
              required
              minlength="6"
              maxlength="30"
            />
            <p v-if="form.password && !passwordValid">
              A senha deve incluir pelo menos uma letra maiúscula, uma letra minúscula, e um número.
            </p>
          </div>
        </div>
        <div class="col-12 col-md-6">
          <div class="input-group input-group-lg my-3">
            <span class="input-group-text">Confirme:</span>
            <input
              type="password"
              class="form-control"
              v-model="form.confirm_pw"
              required
              minlength="6"
              maxlength="30"
            />
          </div>
        </div>
      </div>

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
