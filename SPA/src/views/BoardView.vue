<script setup>
import { useUserStore } from "@/features/user/store";
import { useMovementStore } from "@/features/movement/store";
import { useSchedulerStore } from "@/features/scheduler/store";
import { ScheduleXCalendar } from "@schedule-x/vue";
import { createCalendar, createViewMonthAgenda, createViewMonthGrid } from "@schedule-x/calendar";
import "@schedule-x/theme-default/dist/index.css";

const date = new Date().now();

const userStore = useUserStore();
const movementStore = useMovementStore();
const schedulerStore = useSchedulerStore();

const events = schedulerStore.getMonthlyEvents(date);
const calendarApp = createCalendar({
  selectedDate: date,
  views: [createViewMonthGrid(), createViewMonthAgenda()],
  events: events,
});
</script>

<template>
  <div>
    <ScheduleXCalendar :calendar-app="calendarApp" />
  </div>
</template>
