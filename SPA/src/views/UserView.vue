<script setup>
import { defineProps, onMounted } from "vue";
import BankAccountComponent from "@/features/user/BankAccountComponent.vue";
import PerfilComponent from "@/features/user/PerfilComponent.vue";
import SettingsComponent from "@/features/user/SettingsComponent.vue";

const props = defineProps({
  first_access: {
    type: [Boolean, null],
    required: false,
    default: null,
  },
});

const view_component = ref("perfil");

onMounted(() => {
  if (props.first_access !== null) {
    if (props.first_access === false) {
      showLists.value = true;
    } else {
      view_component.value = "settings";
    }
  }
});
</script>
<template>
  <div class="container">
    <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
      <input
        type="radio"
        class="btn-check"
        name="btnradio"
        value="perfil"
        v-mode="view_component"
        id="btnradio1"
        autocomplete="off"
      />
      <label class="btn btn-outline-primary" for="btnradio1">Perfil</label>

      <input
        type="radio"
        class="btn-check"
        name="btnradio"
        value="settings"
        v-mode="view_component"
        id="btnradio2"
        autocomplete="off"
        @click="userComponent('settings')"
      />
      <label class="btn btn-outline-primary" for="btnradio2">Customização</label>

      <input
        type="radio"
        class="btn-check"
        name="btnradio"
        value="bank_account"
        v-mode="view_component"
        id="btnradio3"
        autocomplete="off"
        @click="userComponent('bank_account')"
      />
      <label class="btn btn-outline-primary" for="btnradio3">Contas Bancárias</label>
    </div>
    <div v-if="view_component === 'bank_acocunt'">
      <BankAccountComponent></BankAccountComponent>
    </div>
    <div v-if="view_component === 'settings'">
      <SettingsComponent></SettingsComponent>
    </div>
    <div v-else>
      <PerfilComponent></PerfilComponent>
    </div>
  </div>
</template>
