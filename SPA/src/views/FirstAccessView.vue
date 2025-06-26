<script setup>
import { ref } from "vue";
import { useUserStore } from "@user/store";

const custom = ref({
  movement_title: "Movement",
  record_title: "Record",
  entity_title: "Entity",
});
const userStore = useUserStore();
console.log("from first-access: ", userStore.getUser);
</script>
<template>
  <form>
    <p class="fs-3">Personalização</p>
    <div class="border rounded my-3">
      <p class="fs-4">Movement:</p>
      <p class="fs-5">
        Esta palavra "Movement" representa uma movimentação financeira genérica, você pode mudar o
        nome para "Entrada", "Conta", ou qualquer outra coisa que faça sentido para seu uso diário.
      </p>
      <input class="form-control" v-model="custom.movement_title" type="text" />
    </div>
    <div class="border rounded my-3">
      <p class="fs-4">Record:</p>
      <p class="fs-5">
        Esta palavra "Record" representa uma "Ação" ou "Registro" ou "Serviço", você pode mudar o
        nome para qualquer outra coisa que faça sentido para seu uso diário.
      </p>
      <input class="form-control" v-model="custom.record_title" type="text" />
    </div>
    <div class="border rounded my-3">
      <p class="fs-4">Entity:</p>
      <p class="fs-5">
        Esta palavra "Entity" representa uma "Entidade" genérica, podendo ser um "Cliente",
        "Organização", "Sócio" você pode mudar o nome para qualquer outra coisa que faça sentido
        para seu uso diário.
      </p>
      <input class="form-control" v-model="custom.entity_title" type="text" />
    </div>
    <div class="my-5">
      <p class="fs-4">Conta Bancária:</p>
    </div>
  </form>
</template>
