<script setup>
import { ref, defineProps, onMounted } from "vue";
import { useUserStore } from "@/features/user/store";
import PasswordComponent from "@/features/common/PasswordComponent.vue";
import FormInputComponent from "@/features/common/FormInputComponent.vue";

const props = defineProps({
  first_access: {
    type: [Boolean, null],
    required: false,
    default: null,
  },
});
const passwordPlaceholder = ref({});

onMounted(() => {
  if (props.first_access !== null) {
    if (props.first_access === false) {
      showLists.value = true;
    }
  }
});

const userStore = useUserStore();
const user = userStore.getUser;
</script>
<template>
  <div class="container">
    <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
      <input
        type="radio"
        class="btn-check"
        name="btnradio"
        id="btnradio1"
        autocomplete="off"
        checked
      />
      <label class="btn btn-outline-primary" for="btnradio1">Radio 1</label>

      <input type="radio" class="btn-check" name="btnradio" id="btnradio2" autocomplete="off" />
      <label class="btn btn-outline-primary" for="btnradio2">Radio 2</label>

      <input type="radio" class="btn-check" name="btnradio" id="btnradio3" autocomplete="off" />
      <label class="btn btn-outline-primary" for="btnradio3">Radio 3</label>
    </div>
    <p class="fs-3">Usuário</p>
  </div>
  <div>
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
  </div>
</template>
