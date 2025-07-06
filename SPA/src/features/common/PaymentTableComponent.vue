<script setup>
import { defineModel } from "vue";
import { useMovementStore } from "@/features/movement/store";
import { useRouter } from "vue-router";

const router = useRouter();
const movementStore = useMovementStore();

function getPayment(item) {
  router.push({ name: "payment", params: { id: item.id, back: true } });
}
function deletePayment(item, index) {
  movementStore.deletePayment(item.id);
  payments.value.splice(index, 1);
}

const payments = defineModel("payments", { type: Array });
</script>

<template>
  <table class="table table-hover">
    <thead>
      <tr>
        <th scope="col">
          Valor
        </th>
        <th scope="col">
          Data de Pagamento
        </th>
        <th scope="col">
          Status
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
        <td>R$ {{ item.value }}</td>
        <td>{{ item.status ? item.payment_date : item.is_due }}</td>
        <td>{{ item.status }}</td>
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
                  @click="getPayment(item)"
                >Ver Mais!</a>
              </li>
              <li>
                <a
                  class="dropdown-item"
                  href="#"
                  @click="deletePayment(item, index)"
                >Excluir!</a>
              </li>
            </ul>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
</template>
