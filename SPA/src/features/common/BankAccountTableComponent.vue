<script setup>
import { defineModel } from "vue";
import { useUserStore } from "@/features/User/store";

const userStore = useUserStore();
const setting = userStore.getSettings;

function deleteAccount(item, index) {
  if (setting.default_bank_account === item.id) {
    alert("Não é possívle deletar a conta bancária padrão!");
  } else {
    userStore.removeBankAccount(item.id);
    accounts.value.splice(index);
  }
}

const accounts = defineModel("accounts", { type: Array });
</script>

<template>
  <table class="table table-hover">
    <thead>
      <tr>
        <th scope="col">
          Nome do Banco
        </th>
        <th scope="col">
          Nome da Conta
        </th>
        <th scope="col">
          Balanço
        </th>
        <th scope="col">
          Ignorar nos Totais
        </th>
        <th scope="col">
          #
        </th>
      </tr>
    </thead>
    <tbody class="table-group-divider">
      <tr
        v-for="(item, index) in entity"
        :key="index"
      >
        <td>{{ item.bank_name }}</td>
        <td>{{ item.bank_account }}</td>
        <td>{{ item.balance }}</td>
        <td>{{ item.ignore_on_totals }}</td>
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
                  @click="getAccount(item)"
                >Ver Mais!</a>
              </li>
              <li>
                <a
                  class="dropdown-item"
                  href="#"
                  @click="deleteAccount(item, index)"
                >Excluir!</a>
              </li>
            </ul>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
</template>

const BankAccountSchema = z.object({ id: z.uuid(), bank_name: z.string(), account_name: z.string(),
balance: z.coerce.bigint(), ignore_on_totals: z.boolean(), });
