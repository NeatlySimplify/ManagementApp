<script setup>
import { useRouter, RouterLink } from "vue-router";
import { ref } from "vue";
import api from "@/util/api";
import { useUserStore } from "@/features/user/store";
import { useEntityStore } from "@/features/entity/store";
import { useMovementStore } from "@/features/movement/store";
import { useRecordStore } from "@/features/records/store";
import { useSchedulerStore } from "@/features/scheduler/store";
import FormInputComponent from "@/features/common/FormInputComponent.vue";
import PasswordComponent from "@/features/common/PasswordComponent.vue";

const router = useRouter();
const data = ref({
  email: "",
  password: "",
});
const isLoading = ref(false);
const first_access = ref(false);
const valid = ref(false)

const onSubmit = async () => {
  try {
    const request = await api.get("/api/auth/signin", {
      params: {
        email: data.value.email,
        password: data.value.password,
      },
    });
    if (request.status === "ok") {
      const userStore = useUserStore();
      const scheduleStore = useSchedulerStore();
      const entityStore = useEntityStore();
      const recordStore = useRecordStore();
      const movementStore = useMovementStore();
      const data = userStore.getData();
      if (data.settings.record_title === "" || data.settings.record_title === null) {
        first_access.value = true;
        router.push({ name: 'user', params: { first_access: first_access } });
      } else {
        userStore.setSettings(data.settings);
        userStore.setAccounts(data.account);
        userStore.setUser(data);
        entityStore.set(data.entity);
        scheduleStore.set(data.event);
        recordStore.set(data.record);
        movementStore.setMovement(data.movement);
        movementStore.setPayment(data.payment);
      }
      router.push({ name: 'board' });
    }
  } catch (err) {
    console.error("Error on request:", err);
  }
};
</script>

<template>
  <div class="container-fluid border rounded border-top-0">
    <form @submit.prevent="onSubmit">
      <FormInputComponent
        v-movel:placeholder="data.email"
        title="E-mail"
        :required="true"
        :is-read-only="false"
      />
      <PasswordComponent
        v-model:password-model="data.password"
        v-model:valid="valid"
        label="Senha"
      />
      <div class="mb-3 row">
        <div class="btn-group d-flex">
          <RouterLink
            class="btn btn-outline-danger btn-lg flex-grow-1"
            :to="{ name: 'register' }"
            :class="{ disabled: isLoading }"
          >
            Registrar
          </RouterLink>
          <button
            type="submit"
            :disabled="!valid"
            class="btn btn-outline-primary btn-lg flex-grow-1"
          >
            Login <i
              v-if="isLoading"
              class="fa fa-spinner fa-spin"
            />
          </button>
        </div>
      </div>
    </form>
  </div>
</template>
