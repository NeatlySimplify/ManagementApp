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
  <div class="mb-2 row rounded shadow-sm">
    <label for="select" class="col-sm-2 form-label">{{ prop.title }}</label>
    <input class="form-control" list="datalistOptions" id="select" v-if="!prop.isReadOnly" v-model="placeholder"
      :required="required">
    <datalist id="datalistOptions">
      <option v-for="(option, index) in prop.types" :key="index" :value="option">
        {{ option }}
      </option>
    </datalist>
  </div>
</template>
