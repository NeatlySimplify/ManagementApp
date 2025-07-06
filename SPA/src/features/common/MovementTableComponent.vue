<script setup>
import { defineModel } from "vue";
import { useMovementStore } from "@/features/movement/store";
import { useRouter } from "vue-router";

const router = useRouter();
const movementStore = useMovementStore();

function getMovement(id) {
  router.push({
    name: "movement",
    params: {
      id: id,
      back: true,
    },
  });
}

function deleteMovement(item, index) {
  movementStore.removeMovement(item.id);
  movement.value.splice(index, 1);
}

const movement = defineModel("movement", { type: Array });
</script>

<template>
  <table class="table table-hover">
    <thead>
      <tr>
        <th scope="col">
          Tipo
        </th>
        <th scope="col">
          Valor
        </th>
        <th scope="col">
          Parcelas
        </th>
        <th scope="col">
          #
        </th>
      </tr>
    </thead>
    <tbody class="table-group-divider">
      <tr
        v-for="(item, index) in payments"
        :key="index"
      >
        <td>R$ {{ item.type_tage }}</td>
        <td>{{ item.value }}</td>
        <td>{{ item.installment }}</td>
        <td>
          <div class="dropdown">
            <button
              class="btn btn-outline-secondary dropdown-toggle"
              type="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            />
            <ul class="dropdown-menu">
              <li>
                <a
                  class="dropdown-item"
                  href="#"
                  @click="getMovement(item)"
                >Ver Mais!</a>
              </li>
              <li>
                <a
                  class="dropdown-item"
                  href="#"
                  @click="deleteMovement(item, index)"
                >Excluir!</a>
              </li>
            </ul>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
</template>
