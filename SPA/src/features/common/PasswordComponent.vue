<script setup>
import { ref, watch, computed, onMounted, defineModel, defineProps } from "vue";

const passwordModel = defineModel("password", { type: String, default: "" });

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

// Internal state for the component
const currentPassword = ref(passwordModel.value); // Use ref for internal password state
const displayValue = ref(""); // What's actually shown in the input
const isFocused = ref(false); // To control when to show the last character
const validationErrors = ref([]); // Still used internally to determine hasError and emit
let timeoutId = null; // To clear the last character after a delay
const passwordInput = ref(null); // Ref to the input element

// --- Constant Validation Rules ---
const MIN_LENGTH = 6;
const MAX_LENGTH = 30;
const REQUIRE_UPPERCASE = true;
const REQUIRE_LOWERCASE = true;
// No requirement for digit or special character as per new instructions

// --- Computed Properties ---

// Determines if there are any validation errors
const hasError = computed(() => validationErrors.value.length > 0);

// --- Watchers ---

// Watch for changes in the passwordModel (from parent v-model)
watch(passwordModel, (newVal) => {
  currentPassword.value = newVal;
  maskInput(currentPassword.value); // Re-mask when parent changes value
  validate(); // Re-validate
});

// Watch for internal password changes to trigger validation
watch(currentPassword, () => {
  validate();
});

// --- Methods ---

// Handles input events from the text field
const handleInput = (event) => {
  const newValue = event.target.value;

  // Update the internal password model and emit to parent
  currentPassword.value = newValue;
  passwordModel.value = newValue; // Update defineModel

  // Logic for showing the last typed character
  if (isFocused.value) {
    clearTimeout(timeoutId); // Clear any existing timeout

    if (newValue.length > 0) {
      // Show all but the last character masked, and the last character unmasked
      displayValue.value = getMaskedString(newValue.slice(0, -1)) + newValue.slice(-1);

      // Set a timeout to mask the last character after a short delay
      timeoutId = setTimeout(() => {
        maskInput(newValue);
      }, 700); // Show last character for 700ms
    } else {
      displayValue.value = ""; // If empty, clear display
    }
  } else {
    maskInput(newValue); // If not focused, keep it fully masked
  }
};

// Handles blur event (when input loses focus)
const handleBlur = () => {
  isFocused.value = false;
  clearTimeout(timeoutId); // Clear any pending masking timeout
  maskInput(currentPassword.value); // Fully mask on blur
  validate(); // Run final validation on blur
};

// Generates a masked string of asterisks
const getMaskedString = (text) => {
  return "*".repeat(text.length);
};

// Masks the input field's display value
const maskInput = (password) => {
  displayValue.value = getMaskedString(password);
};

// Performs validation checks
const validate = () => {
  const password = currentPassword.value;
  const errors = [];

  // 1. At least 6 characters
  if (password.length < MIN_LENGTH) {
    errors.push("A senha deve conter no mínimo 6 caracteres.");
  }

  // 2. At most 30 characters
  if (password.length > MAX_LENGTH) {
    errors.push("A senha deve conter no máximo 30 caracteres.");
  }
  if (REQUIRE_UPPERCASE && !/[A-Z]/.test(password)) {
    errors.push("Senha deve conter pelo menos uma letra maiuscula.");
  }
  if (REQUIRE_LOWERCASE && !/[a-z]/.test(password)) {
    errors.push("Senha deve conter pelo menos uma letra minuscula.");
  }

  validationErrors.value = errors;
  emit("validation-status", errors.length === 0); // Emit overall validity
  emit("errors", errors); // Emit the array of errors for parent to display
};

onMounted(() => {
  maskInput(currentPassword.value);
  validate(); // Initial validation
});
</script>
<template>
  <div class="mb-4 p-4 bg-light rounded shadow-sm">
    <label v-if="props.label" class="form-label">{{ props.label }}</label>
    <div class="input-group">
      <input
        ref="passwordInput"
        type="text"
        :value="displayValue"
        @input="handleInput"
        @focus="isFocused = true"
        @blur="handleBlur"
        :placeholder="props.placeholder"
        :class="['form-control', { 'is-invalid': hasError }]"
        :maxlength="maxLength"
        autocomplete="new-password"
      />
    </div>
  </div>
</template>
