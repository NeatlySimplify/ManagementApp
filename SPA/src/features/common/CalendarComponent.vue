<script setup>
import { defineModel, defineProps, onMounted } from "vue";
import { useSchedulerStore } from "@/features/scheduler/store";
import { ScheduleXCalendar } from "@schedule-x/vue";
import {
  createCalendar,
  createViewMonthAgenda,
  createViewMonthGrid,
  createViewWeek,
  createViewDay,
} from "@schedule-x/calendar";
import "@schedule-x/theme-default/dist/index.css";

const schedulerStore = useSchedulerStore();

const currentDate = defineModel("currentDate", { type: Date, default: new Date() });
const prop = defineProps({
  limited: {
    type: Boolean,
    default: false,
  },
  objects: {
    type: [Array, null],
    required: false,
    default: null,
  },
});

const events = ref(null);

const calendarApp = ref(null);

onMounted(() => {
  if (prop.limited) {
    calendarApp.value = createCalendar({
      selectedDate: currentDate.value,
      views: [createViewMonthGrid(), createViewMonthAgenda()],
      events: events.value,
    });
  } else {
    calendarApp.value = createCalendar({
      selectedDate: currentDate.value,
      views: [createViewMonthGrid(), createViewMonthAgenda(), createViewWeek(), createViewDay()],
      events: events.value,
    });
    if (prop.objects) {
      events.value = props.object;
    } else {
      events.value = computed(() => schedulerStore.getMonthlyEvents(currentDate.value));
    }
  }
});
</script>

<template>
  <ScheduleXCalendar :calendar-app="calendarApp" />
</template>
