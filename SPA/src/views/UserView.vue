<script setup>
  import { defineProps, onMounted, ref } from 'vue'
  import BankAccountComponent from '@/features/user/BankAccountComponent.vue'
  import PerfilComponent from '@/features/user/PerfilComponent.vue'
  import SettingsComponent from '@/features/user/SettingsComponent.vue'

  const props = defineProps({
    firstAccess: {
      type: [Boolean, null],
      required: false,
      default: null,
    },
  })

  const view_component = ref('perfil')

  onMounted(() => {
    if (props.first_access !== null) {
      if (props.firstAccess) {
        view_component.value = 'settings'
      }
    }
  })
</script>
<template>
  <div class="container">
    <div
      class="btn-group"
      role="group"
      aria-label="Basic radio toggle button group"
    >
      <input
        id="btnradio1"
        v-mode="view_component"
        type="radio"
        class="btn-check"
        name="btnradio"
        value="perfil"
        autocomplete="off"
      />
      <label
        class="btn btn-outline-primary"
        for="btnradio1"
        >Perfil</label>

      <input
        id="btnradio2"
        v-mode="view_component"
        type="radio"
        class="btn-check"
        name="btnradio"
        value="settings"
        autocomplete="off"
        @click="userComponent('settings')"
      />
      <label
        class="btn btn-outline-primary"
        for="btnradio2"
        >Customização</label>

      <input
        id="btnradio3"
        v-mode="view_component"
        type="radio"
        class="btn-check"
        name="btnradio"
        value="bank_account"
        autocomplete="off"
        @click="userComponent('bank_account')"
      />
      <label
        class="btn btn-outline-primary"
        for="btnradio3"
        >Contas Bancárias</label>
    </div>
    <div v-if="view_component === 'bank_acocunt'">
      <BankAccountComponent />
    </div>
    <div v-if="view_component === 'settings'">
      <SettingsComponent :first-access="props.firstAccess" />
    </div>
    <div v-else>
      <PerfilComponent />
    </div>
  </div>
</template>
