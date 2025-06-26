<script setup>
import { useRouter } from "vue-router";
import { ref } from "vue";
import api from "@util/api";
import { useUserStore } from "@user/store";
import { useEntityStore } from "@entity/store";
//import { useMovementStore } from "@/stores/movement";
//import { useRecordStore } from "@/stores/record";
//import { useSchedulerStore } from "@/stores/scheduler";
//
//
//For testing

const router = useRouter();
const data = ref({
  email: "",
  password: "",
});
const isLoading = ref(false);
const user = useUserStore();

const onSubmit = async () => {
  try {
    //const request = await api.post(`${route}/login`, data.value);
    // const first_access = request.result.first_access;
    // if (first_access === false) {
    //   router.push("first-access");
    // }
    const request = await api.get("/user", {
      params: {
        email: data.value.email,
        password: data.value.password,
      },
    });
    const dataRequest = request.data[0];

    if (dataRequest.first_access === true) {
      user.setUser(dataRequest, true);
      console.log(user.getUser);
      router.push("first-access");
    } else {
      try {
        const request = await api.get("/db");

        //schedule = useSchedulerStore();
        const entity = useEntityStore();
        //record = useRecordStore();
        //movement = useMovementStore();

        result = request.result;
        entity.set(result.entity);
        //schedule.set(result.event);
        //record.set(result.record);
        //movement.setMovement(result.movement);
        //movement.setIncome(result.payment_income);
        //movement.setExpense(result.payment_expense);
        user.setAccounts(result.account);
        userData = result.user[1];
        userData.settings = result.settings[1];
        accounts = result.bankAccount;
        user.setUser(userData);
        user.setAccounts(accounts);
      } catch {
        user = useUserStore();
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
      <div class="input-group input-group-lg my-3">
        <span class="input-group-text">E-Mail:</span>
        <input
          type="email"
          class="form-control"
          v-model="data.email"
          required
          placeholder="fulano@mail.com"
          minlength="6"
          maxlength="40"
        />
      </div>
      <div class="input-group input-group-lg my-3">
        <span class="input-group-text">Password:</span>
        <input
          type="password"
          class="form-control"
          v-model="data.password"
          required
          minlength="6"
          maxlength="30"
        />
      </div>
      <div class="mb-3 row">
        <div class="btn-group d-flex">
          <RouterLink
            class="btn btn-outline-danger btn-lg flex-grow-1"
            :to="{ name: 'register' }"
            :class="{ disabled: isLoading }"
          >
            Registrar
          </RouterLink>
          <button type="submit" class="btn btn-outline-primary btn-lg flex-grow-1">
            Login <i v-if="isLoading" class="fa fa-spinner fa-spin"></i>
          </button>
        </div>
      </div>
    </form>
  </div>
</template>
