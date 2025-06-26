<script setup>
import { ref } from "vue";
import FormButtons from "@auth/FormButtonsComponent.vue";
import api from "@/util/api";

const sequence_code = ref("");

const onSubmit = async () => {
  const sequence = sequence_code.value.toLowerCase();
  try {
    const response = await api.post("api/auth/register", sequence);
    console.log("Success:", response.data);
  } catch (err) {
    console.error("Error on request:", err);
  }
};
</script>
<template>
  <div class="container">
    <form @submit.prevent="onSubmit">
      <div class="mb-3 row">
        <label for="sequence" class="col-4 col-form-label">Type the sequence code:</label>
        <div class="col-8">
          <input
            type="text"
            class="form-control"
            id="sequence"
            placeholder="XXXXXX"
            v-model="sequence_code"
            required
            maxlength="6"
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
