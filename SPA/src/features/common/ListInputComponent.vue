<script setup>
import { ref, defineProps, defineModel } from "vue";

// defineModel sem tipo — só JavaScript
const tags = defineModel("tags");
const props = defineProps({
  title: String,
});

const inputValue = ref("");
const input = ref(null);

function addTag() {
  const value = inputValue.value.trim();
  if (value && !tags.value.includes(value)) {
    tags.value.push(value);
  }
  inputValue.value = "";
}

function removeTag(index) {
  tags.value.splice(index, 1);
}

function focusInput() {
  input.value?.focus();
}
</script>
<template>
  <p class="fs-4">TAG : {{ props.title }}</p>
  <div class="tag-input-container" @click="focusInput">
    <span v-for="(tag, index) in tags" :key="index" class="tag">
      {{ tag }}
      <button class="remove-btn" @click.stop="removeTag(index)">×</button>
    </span>
    <input
      ref="input"
      v-model="inputValue"
      @keydown.enter.prevent="addTag"
      @blur="addTag"
      placeholder="Enter tag and press Enter"
    />
  </div>
</template>

<style scoped>
.tag-input-container {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  border: 1px solid #ccc;
  padding: 6px;
  border-radius: 4px;
  cursor: text;
}
.tag {
  background-color: #e0e0e0;
  border-radius: 3px;
  padding: 3px 6px;
  margin: 2px;
  display: flex;
  align-items: center;
}
.remove-btn {
  background: none;
  border: none;
  margin-left: 4px;
  cursor: pointer;
  color: #555;
}
.input {
  flex: 1;
  border: none;
  outline: none;
  min-width: 120px;
  padding: 4px;
}
</style>
