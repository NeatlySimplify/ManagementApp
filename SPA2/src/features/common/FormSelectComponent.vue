<script setup>
import { defineModel, defineProps } from "vue";

const prop = defineProps({
  title: String,
  isReadOnly: Boolean,
  types: Array,
  required: {
    type: Boolean,
    required: false,
    default: false,
  },
});

const placeholder = defineModel("placeholder");
</script>
<template>
  <div class="mb-3 row">
    <label for="select" class="col-sm-2 col-form-label">{{ prop.title }}</label>
    <div class="col-sm-10">
      <select v-if="!prop.isReadOnly" v-model="placeholder" :required="required">
        <option selected></option>
        <option v-for="(option, index) in prop.types" :key="index" :value="option">
          {{ option }}
        </option>
      </select>
      <input
        type="text"
        v-else
        readonly
        v-model="placeholder"
        class="form-control-plaintext"
        id="select"
      />
    </div>
  </div>
</template>
