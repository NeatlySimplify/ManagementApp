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
const placeholder = defineModel("placeholder");
const custom = prop.object.value.map((item) => ({ id: item.id, name: item.name }));
const searchTerm = ref("");
const filteredOptions = computed(() =>
  custom.filter((opt) => opt.name.toLowerCase().includes(searchTerm.value.toLowerCase())),
);

function selectOption(opt) {
  placeholder.value = opt.value;
  searchTerm.value = opt.name;
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
  </div>
</template>
