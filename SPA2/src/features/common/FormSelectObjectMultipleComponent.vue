<script setup>
import { defineProps, defineModel } from "vue";

const prop = defineProps({
  title: {
    type: String,
  },
  object: {
    type: Array,
  },
});
const selectedOptions = defineModel("selectedOptions", { type: Array });
const custom = prop.object.value.map((item) => ({ id: item.id, name: item.name }));
const searchTerm = ref("");
const filteredOptions = computed(() =>
  custom.filter((opt) => opt.name.toLowerCase().includes(searchTerm.value.toLowerCase())),
);

function selectOption(opt) {
  const exists = selectedOptions.value.some((item) => item.id === opt.id);
  if (!exists) {
    selectedOptions.value.push(opt);
  }
  searchTerm.value = ""; // Optional: clear search after selection
}

function removeEntity(index) {
  selectedOptions.splice(index, 1);
}
</script>
<template>
  <div class="mb-3 row">
    <label for="entities" class="col-sm-2 col-form-label">{{ prop.title }}</label>
    <input v-model="searchTerm" type="text" placeholder="" class="form-control" />

    <!-- Filtered list -->
    <ul v-if="filteredOptions.length && searchTerm" class="list-group position-absolute w-100 z-3">
      <li
        v-for="opt in filteredOptions"
        :key="String(opt.value)"
        class="list-group-item list-group-item-action"
        @click="selectOption(opt)"
        style="cursor: pointer"
      >
        {{ opt.name }}
      </li>
    </ul>

    <!-- Selected display -->
    <ul v-if="selectedOptions" class="mt-2 list-group">
      <li class="list-group-item" v-for="(option, index) in selectedEntity" :key="index">
        {{ option.name }}
      </li>
      <span class="btn-close" @click="removeEntity(index)"></span>
    </ul>
  </div>
</template>
