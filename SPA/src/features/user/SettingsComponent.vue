<script setup>
  import { ref, defineProps, onMounted } from 'vue'
  import { useUserStore } from '@/features/user/store'
  import ListInputComponent from '@/features/common/ListInputComponent.vue'

  const props = defineProps({
    firstAccess: {
      type: [Boolean, null],
      required: false,
      default: null,
    },
  })

  onMounted(() => {
    if (props.firstAccess !== null) {
      if (props.firstAccess === false) {
        showLists.value = true
      }
    }
  })

  const showLists = ref(false)
  const userStore = useUserStore()
  const settings = userStore.getSettings
</script>
<template>
  <form>
    <div class="container">
      <p class="fs-3">
Personalização
</p>
      <div class="border rounded row my-3">
        <p class="fs-4">
Movement:
</p>
        <p class="fs-5">
          Esta palavra "Movement" representa uma movimentação financeira genérica, você pode mudar o
          nome para "Entrada", "Conta", ou qualquer outra coisa que faça sentido para seu uso
          diário.
        </p>
        <input
          v-model="custom.movement_title"
          class="form-control"
          type="text"
        />
      </div>

      <div class="border rounded row my-3">
        <p class="fs-4">
Record:
</p>
        <p class="fs-5">
          Esta palavra "Record" representa uma "Ação" ou "Registro" ou "Serviço", você pode mudar o
          nome para qualquer outra coisa que faça sentido para seu uso diário.
        </p>
        <input
          v-model="custom.record_title"
          class="form-control"
          type="text"
        />
      </div>

      <div class="border rounded row my-3">
        <p class="fs-4">
Entity:
</p>
        <p class="fs-5">
          Esta palavra "Entity" representa uma "Entidade" genérica, podendo ser um "Cliente",
          "Organização", "Sócio" você pode mudar o nome para qualquer outra coisa que faça sentido
          para seu uso diário.
        </p>
        <input
          v-model="custom.entity_title"
          class="form-control"
          type="text"
        />
      </div>
      <div
        v-if="showLists"
        class="border rounded row my-3"
      >
        <ListInputComponent v-model:tags="settings.account_types" />
        <ListInputComponent
          v-model:tags="settings.entity_types"
          :title="`Tipos de ${settings.entity_title}`"
        />
        <ListInputComponent
          v-model:tags="settings.entity_document_types"
          :title="`Tipos de Documentos de ${settings.entity_title}`"
        />
        <ListInputComponent v-model:tags="settings.contact_number_types" />
        <ListInputComponent v-model:tags="settings.record_types" />
        <ListInputComponent v-model:tags="settings.record_status" />
        <ListInputComponent v-model:tags="settings.movement_income_types" />
        <ListInputComponent v-model:tags="settings.movement_expense_types" />
        <ListInputComponent v-model:tags="settings.scheduler_types" />
        <ListInputComponent v-model:tags="settings.relationship_status" />
        <ListInputComponent v-model:tags="settings.sex" />
      </div>
    </div>
    <button type="submit" />
  </form>
</template>
