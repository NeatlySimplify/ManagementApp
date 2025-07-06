<script setup>
import { defineModel, computed } from "vue";

const currentDate = defineModel("currentDate", { type: Date, default: new Date() });

const nextMonth = () => {
  currentDate.value = new Date(
    currentDate.value.getFullYear(),
    currentDate.value.getMonth() + 1,
    1,
  );
};

const prevMonth = () => {
  currentDate.value = new Date(
    currentDate.value.getFullYear(),
    currentDate.value.getMonth() - 1,
    1,
  );
};
const year_month = computed(() => {
  const year = currentDate.value.getFullYear();
  const month = currentDate.value.toLocaleString("default", { month: "long" }); // Get full month name

  return `${month} ${year}`;
});
</script>
<template>
  <div class="row">
    <button
      class="btn btn-outline-primary col-1 col-md-2 col-lg-3 col"
      @click="prevMonth"
    >
      <i>&#11144;</i>
    </button>
    <span>{{ year_month }}</span>
    <button
      class="btn btn-outline-primary col-1 col-md-2 col-lg-3 col"
      @click="nextMonth"
    >
      <i>&#11146;</i>
    </button>
  </div>
</template>
