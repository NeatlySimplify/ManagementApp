<script setup>
import { useUserStore } from "@/features/user/store";
import { useMovementStore } from "@/features/movement/store";
import { useSchedulerStore } from "@/features/scheduler/store";
import { ScheduleXCalendar } from "@schedule-x/vue";
import { useRecordStore } from "@/features/records/store";
import { Line } from "@/features/common/LineChartComponent.vue";
import { createCalendar, createViewMonthAgenda, createViewMonthGrid } from "@schedule-x/calendar";
import "@schedule-x/theme-default/dist/index.css";
import { ref, computed } from "vue";

const userStore = useUserStore();
const movementStore = useMovementStore();
const recordStore = useRecordStore();
const schedulerStore = useSchedulerStore();
const settings = userStore.getSettings;

const currentDate = ref(new Date());
const showYourself = ref(false);

const record_active = computed(() => recordStore.getRecordsByStatus(false));
const movement_active = computed(() => movementStore.getActiveMovement(currentDate.value));

// Function to increment the month
const nextMonth = () => {
  currentDate.value = new Date(
    currentDate.value.getFullYear(),
    currentDate.value.getMonth() + 1,
    1,
  );
};

// Function to decrement the month
const prevMonth = () => {
  currentDate.value = new Date(
    currentDate.value.getFullYear(),
    currentDate.value.getMonth() - 1,
    1,
  );
};

// Computed property to format the year and month
const year_month = computed(() => {
  const year = currentDate.value.getFullYear();
  const month = currentDate.value.toLocaleString("default", { month: "long" }); // Get full month name

  return `${month} ${year}`;
});

const events = computed(() => schedulerStore.getMonthlyEvents(currentDate.value));
const calendarApp = createCalendar({
  selectedDate: currentDate.value,
  views: [createViewMonthGrid(), createViewMonthAgenda()],
  events: events.value,
});
</script>

<template class="container">
  <div class="row">
    <button class="btn btn-outline-primary col-1 col-md-2 col-lg-3 col" @click="prevMonth">
      <i>&#11144;</i>
    </button>
    <span>{{ year_month }}</span>
    <button class="btn btn-outline-primary col-1 col-md-2 col-lg-3 col" @click="nextMonth">
      <i>&#11146;</i>
    </button>
  </div>
  <div class="row">
    <div class="card col">
      <Line :referenceDate="currentDate"></Line>
    </div>
    <div class="card col-12 col-md-6 col-lg-4">
      <ul class="list-group list-group-flush">
        <li class="list-group-item">
          <p>
            {{ settings.record_title }} Ativos
            <span class="badge text-bg-secondary">{{ record_active.length }}</span>
          </p>
          <RouterLink :to="{ name: record }">Ver Mais...</RouterLink>
        </li>
        <li class="list-group-item">
          <p>
            {{ settings.movement_title }} Ativos
            <span class="badge text-bg-secondary">{{ movement_active.length }}</span>
          </p>
          <RouterLink :to="{ name: movement }">Ver Mais...</RouterLink>
        </li>
      </ul>
    </div>
  </div>
  <div class="row" v-if="showYourself"></div>
  <div>
    <ScheduleXCalendar :calendar-app="calendarApp" />
  </div>
</template>
