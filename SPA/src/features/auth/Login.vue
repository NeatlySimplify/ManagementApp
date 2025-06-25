<script setup>
import { useRouter } from "vue-router";
import FormButtons from "./FormButtons.vue";
import { ref } from "vue";
import api from "@/util/api";
import { useUserStore } from "@/stores/user";
import { useEntityStore } from "@/stores/entity";
import { useMovementStore } from "@/stores/movement";
import { useRecordStore } from "@/stores/record";
import { useSchedulerStore } from "@/stores/scheduler";

const router = useRouter();
const route = "api/auth";
const data = ref({
  email: "",
  password: "",
});

const onSubmit = async () => {
  try {
    const request = await api.post(`${route}/login`, data.value);
    const first_access = request.result.first_access;
    if (first_access === true) {
      router.push("first-access");
    } else {
      try {
        request = await api.get(route);
        schedule = useSchedulerStore();
        entity = useEntityStore();
        record = useRecordStore();
        movement = useMovementStore();
        user = useUserStore();

        result = request.result;
        entity.set(result.entity);
        schedule.set(result.event);
        record.set(result.record);
        movement.setMovement(result.movement);
        movement.setIncome(result.payment_income);
        movement.setExpense(result.payment_expense);
        user.setAccounts(result.account);
        user.setUser(result);
      } catch {
        user = useUserStore();
        user.userRequest = true;
      } finally {
        router.push("board");
      }
    }
  } catch (err) {
    console.error("Error on request:", err);
  }
};
</script>

<template>
  <div class="container-fluid border rounded border-top-0">
    <form @submit.prevent="onSubmit">
      <div class="mb-3 row">
        <label for="inputEmail" class="col-4 col-form-label">Email:</label>
        <div class="col-8">
          <input
            type="email"
            class="form-control"
            v-model="data.email"
            id="inputEmail"
            placeholder="Email"
          />
        </div>
      </div>
      <div class="mb-3 row">
        <label for="inputPassword" class="col-4 col-form-label">Password:</label>
        <div class="col-8">
          <input
            type="password"
            class="form-control"
            v-model="data.password"
            id="inputPassword"
            placeholder="Password"
          />
        </div>
      </div>
      <div class="mb-3 row">
        <div class="offset-sm-4 col-sm-8">
          <FormButtons></FormButtons>
        </div>
      </div>
    </form>
  </div>
</template>
