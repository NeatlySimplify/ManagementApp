<script setup>
import { defineModel } from "vue";
import { useEntityStore } from "@/features/entity/store";
import { useRouter } from "vue-router";

const router = useRouter();
const entityStore = useEntityStore();

function getEntity(id) {
  router.push({
    name: "entity",
    params: {
      id: id,
      back: true,
    },
  });
}

function deleteEntity(item, index) {
  entityStore.removeEntity(item.id);
  entity.value.splice(index);
}

const entity = defineModel("entity", { type: Array });
</script>

<template>
  <table class="table table-hover">
    <thead>
      <tr>
        <th scope="col">Nome</th>
        <th scope="col">#</th>
      </tr>
    </thead>
    <tbody class="table-group-divider">
      <tr v-for="(item, index) in entity" :key="index">
        <td>R$ {{ item.name }}</td>
        <td>
          <div class="dropdown">
            <button
              class="btn btn-outline-secondary dropdown-toggle"
              type="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            ></button>
            <ul class="dropdown-menu">
              <li>
                <a class="dropdown-item" @click="getEntity(item)" href="#">Ver Mais!</a>
              </li>
              <li>
                <a class="dropdown-item" href="#" @click="deleteEntity(item, index)">Excluir!</a>
              </li>
            </ul>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
</template>
