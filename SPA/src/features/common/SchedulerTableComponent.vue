<script setup>
import { defineModel } from "vue";
import { useSchedulerStore } from "@/features/scheduler/store";
import { useRouter } from "vue-router";

const router = useRouter();
const schedulerStore = useSchedulerStore();

function getScheduler(id) {
  router.push({
    name: "",
    params: {
      id: id,
      back: true,
    },
  });
}

function deleteScheduler(item, index) {
  schedulerStore.removeScheduler(item.id);
  scheduler.value.splice(index, 1);
}

const scheduler = defineModel("scheduler", { type: Array });
</script>

<template>
  <table class="table table-hover">
    <thead>
      <tr>
        <th scope="col">
          Nome
        </th>
        <th scope="col">
          Tipo
        </th>
        <th scope="col">
          Status
        </th>
        <th scope="col">
          Começo
        </th>
        <th scope="col">
          Fim
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
        <td>{{ item.name }}</td>
        <td>{{ item.type_tag }}</td>
        <td>{{ item.status }}</td>
        <td>{{ item.date_beginning }}</td>
        <td>{{ item.date_ending }}</td>
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
                  @click="getScheduler(item)"
                >Ver Mais!</a>
              </li>
              <li>
                <a
                  class="dropdown-item"
                  href="#"
                  @click="deleteScheduler(item, index)"
                >Excluir!</a>
              </li>
            </ul>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
</template>
