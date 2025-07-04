<script setup>
import { ref } from "vue";
import api from "@/util/api";
import FormInputComponent from "@/features/common/FormInputComponent.vue";
import { useRouter } from "vue-router";

const email = ref("");
const router = useRouter();
const isLoading = ref(false);

const onSubmit = async () => {
  try {
    await api.post("api/auth/reset-password", email.value);
    isLoading.value = true;
    alert("Password reset email sent successfully! Verify your email to get your new password.");
    router.push("/root");
  } catch (err) {
    console.error("Error on request:", err);
    isLoading.value = false;
    alert(
      "An error occurred while sending the password reset email. Update the page and try again.",
    );
  }
};
</script>
<template>
  <div class="container">
    <form @submit.prevent="onSubmit">
      <FormInputComponent
        title="Type your email to reset your password:"
        :required="true"
        :isReadOnly="false"
        v-model:placeholder="email"
      ></FormInputComponent>
      <div class="offset-sm-4 col-sm-8 mt-3 mx-auto">
        <RouterLink
          class="btn btn-outline-danger btn-lg flex-grow-1"
          :to="{ name: 'root' }"
          :class="{ disabled: isLoading }"
        >
          Registrar
        </RouterLink>
        <button type="submit" class="btn btn-outline-primary btn-lg flex-grow-1">
          Login <i v-if="isLoading" class="fa fa-spinner fa-spin"></i>
        </button>
      </div>
    </form>
  </div>
</template>
