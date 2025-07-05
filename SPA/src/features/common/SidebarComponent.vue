<script setup>
import api from "@/util/api";
import { defineEmits } from "vue";
import { useUserStore } from "@/features/user/store";
import { useRouter, RouterLink } from "vue-router";

const userStore = useUserStore();
const setting = useRouter.getSettings;
const router = useRouter();

defineEmits(["close"]);

async function logout() {
  const result = await api.get("api/auth/logout");
  if (result.status === "success") {
    userStore.$reset();
    router.push("root");
  }
}
</script>
<template>
  <div id="sidebar">
    <button type="button" class="btn btn-outline-dark" @click="$emit('close')">
      <i class="fa fa-bars fa-solid" aria-hidden="true"></i>
    </button>
    <div class="offcanvas offcanvas-start container-fluid" data-bs-scroll="true" tabindex="-1">
      <div class="offcanvas-header row align-content-center">
        <div class="col-1">
          <button
            type="button"
            class="btn-close"
            @click="$emit('close')"
            aria-label="Close"
          ></button>
        </div>
      </div>
      <div class="offcanvas-body">
        <div class="accordion" id="menuAccordion">
          <div class="accordion-item">
            <RouterLink :to="{ name: user }"></RouterLink>
            <h2 class="accordion-header" id="heading_user">
              <a class="accordion-button menu-item" type="button" href="#"> Usuário </a>
            </h2>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="heading_entity">
              <a
                class="accordion-button collapsed menu-item"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#collapse_entity"
                aria-expanded="false"
                aria-controls="collapse_entity"
                href="#"
              >
                {{ setting.entity_title }}
              </a>
            </h2>
            <div
              id="collapse_entity"
              class="accordion-collapse collapse"
              aria-labelledby="heading_entity"
              data-bs-parent="#menuAccordion"
            >
              <div class="accordion-body sub-menu">
                <ul class="list-group list-group-flush">
                  <li class="list-group-item">
                    <RouterLink :to="{ name: entity }" class="link-dark link-underline-opacity-0">
                      Todos
                    </RouterLink>
                  </li>
                  <li class="list-group-item">
                    <RouterLink
                      :to="{ name: entityFiltered, query: { filter: status, term: false } }"
                      class="link-dark link-underline-opacity-0"
                    >
                      Ativos
                    </RouterLink>
                  </li>
                  <li class="list-group-item">
                    <RouterLink
                      :to="{ name: entityFiltered, query: { filter: status, term: true } }"
                      class="link-dark link-underline-opacity-0"
                    >
                      Desativados
                    </RouterLink>
                  </li>
                  <li
                    v-for="(item, index) in setting.entity_types"
                    :key="index"
                    class="list-group-item"
                  >
                    <RouterLink
                      :to="{ name: entityFiltered, query: { filter: type_tag, term: item } }"
                      class="link-dark link-underline-opacity-0"
                    >
                      Tipo - {{ item }}
                    </RouterLink>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="heading_record">
              <a
                class="accordion-button collapsed menu-item"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#collapse_record"
                aria-expanded="false"
                aria-controls="collapse_record"
                href="#"
              >
                {{ setting.record_title }}
              </a>
            </h2>
            <div
              id="collapse_record"
              class="accordion-collapse collapse"
              aria-labelledby="heading_record"
              data-bs-parent="#menuAccordion"
            >
              <div class="accordion-body sub-menu">
                <ul class="list-group list-group-flush">
                  <li class="list-group-item">
                    <RouterLink :to="{ name: record }" class="link-dark link-underline-opacity-0"
                      >Todos</RouterLink
                    >
                  </li>
                  <li class="list-group-item">
                    <RouterLink
                      :to="{ name: recordFiltered, query: { filter: status, status: false } }"
                      class="link-dark link-underline-opacity-0"
                      >Ativos</RouterLink
                    >
                  </li>
                  <li class="list-group-item">
                    <RouterLink
                      :to="{ name: recordFiltered, query: { filter: status, status: true } }"
                      class="link-dark link-underline-opacity-0"
                      >Desativados</RouterLink
                    >
                  </li>
                  <li
                    v-for="(item, index) in setting.record_types"
                    :key="index"
                    class="list-group-item"
                  >
                    <RouterLink
                      :to="{ name: recordFiltered, query: { filter: type_tag, term: item } }"
                      class="link-dark link-underline-opacity-0"
                      >Tipo - {{ item }}</RouterLink
                    >
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="heading_movement">
              <a
                class="accordion-button collapsed menu-item"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#collapse_movement"
                aria-expanded="false"
                aria-controls="collapse_movement"
                ref="#"
              >
                {{ setting.movement_title }}
              </a>
            </h2>
            <div
              id="collapse_movement"
              class="accordion-collapse collapse"
              aria-labelledby="heading_movement"
              data-bs-parent="#menuAccordion"
            >
              <div class="accordion-body sub-menu">
                <ul class="list-group list-group-flush">
                  <li class="list-group-item">
                    <RouterLink :to="{ name: movement }" class="link-dark link-underline-opacity-0"
                      >Todos</RouterLink
                    >
                  </li>
                  <li class="list-group-item">
                    <RouterLink
                      :to="{ name: paymentFiltered, query: { term: 'Entrada' } }"
                      class="link-dark link-underline-opacity-0"
                      >Entrada</RouterLink
                    >
                  </li>
                  <li class="list-group-item">
                    <RouterLink
                      :to="{ name: paymentFiltered, query: { term: 'Saída' } }"
                      class="link-dark link-underline-opacity-0"
                      >Saída</RouterLink
                    >
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="heading_schedule">
              <a
                class="accordion-button collapsed menu-item"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#collapse_schedule"
                aria-expanded="false"
                aria-controls="collapse_schedule"
                href="#"
              >
                Agenda
              </a>
            </h2>
            <div
              id="collapse_schedule"
              class="accordion-collapse collapse"
              aria-labelledby="heading_schedule"
              data-bs-parent="#menuAccordion"
            >
              <div class="accordion-body sub-menu">
                <ul class="list-group list-group-flush">
                  <li
                    v-for="(item, index) in setting.scheduler_types"
                    :key="index"
                    class="list-group-item"
                  >
                    <RouterLink
                      :to="{ name: schedulerFiltered, query: { filter: type_tag, term: item } }"
                    ></RouterLink>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <button class="btn btn-outline-danger btn-lg" @click="logout">Logout</button>
        </div>
      </div>
    </div>
  </div>
</template>
