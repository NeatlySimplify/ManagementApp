<script setup>
import { ref, watch, computed, defineModel, defineProps } from "vue";

const passwordModel = defineModel("passwordModel", { type: String, default: "" });
const valid = defineModel("valid", { type: Boolean, default: false});


// Props for title, label, and placeholder
const props = defineProps({
  label: {
    type: String,
    default: "Password",
  },
  placeholder: {
    type: String,
    default: "Entre sua senha",
  },
});


const validateMax = ref(false)
const validateMin = ref(false)
const validateUpper = ref(false)
const validateLow = ref(false)


const validate = () => {
  const password = passwordModel.value;

  // 1. At least 6 characters
  if (password.length < 6) {
    validateMin.value = true;
  } else {
    validateMin.value = false;
  }

  if (password.length > 30) {
    validateMax.value = true
  } else {
    validateMax.value = false
  }
  if (!/[A-Z]/.test(password)) {
    validateUpper.value = true
  } else { validateUpper.value = false }
  if (!/[a-z]/.test(password)) {
    validateLow.value = true
  } else {
    validateLow.value = false
  }
};
const showPassword = ref(false);


watch(passwordModel, validate);


// Performs validation checks

valid.value = computed(() => {
  return !validateMin.value &&
    !validateMax.value &&
    !validateUpper.value &&
    !validateLow.value;
});

</script>
<template>
  <div class="mb-2 row rounded shadow-sm">
    <div class="col-2">
      <label
        v-if=" props.label"
        class="form-label"
      >{{ props.label }}</label>
    </div>
    <div class="col-10">
      <div class="input-group">
        <input
          v-model="passwordModel"
          :type="showPassword ? 'text' : 'password'"
          :placeholder="props.placeholder"
          class="form-control"
          autocomplete="new-password"
        >
        <span
          class="input-group-text text-secondary"
          @mouseenter="showPassword = true"
          @mouseleave="showPassword = false"
        >&#128065;</span>
      </div>
    </div>
  </div>
  <div class="col-12">
    <ul class="list-group">
      <li
        v-if="validateMax"
        class="list-group-item text-danger"
      >
        A senha deve conter no máximo 30 caracteres.
      </li>
      <li
        v-if="validateMin"
        class="list-group-item text-danger"
      >
        A senha deve conter no mínimo 6 caracteres.
      </li>
      <li
        v-if="validateUpper"
        class="list-group-item text-danger"
      >
        A senha deve conter pelo menos uma letra maiúscula.
      </li>
      <li
        v-if="validateLow"
        class="list-group-item text-danger"
      >
        A senha deve conter pelo menos uma letra minuscula.
      </li>
    </ul>
  </div>
</template>
