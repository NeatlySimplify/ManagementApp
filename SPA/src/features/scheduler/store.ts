import { defineStore } from "pinia";
import { SchedulerSchema, type Scheduler } from "./schema";

export const useSchedulerStore = defineStore("scheduler", {
  state: () => ({
    entries: {} as Record<string, Scheduler>,
  }),

  getters: {
    getEvent: (state) => (id: string) => state.entries[id],
    getAllEvents: (state) => Object.values(state.entries),
    getEventsByStatus:
      (state) =>
      (status: boolean): Scheduler[] =>
        Object.values(state.entries).filter((entity) => entity.status === status),

    getEventsByType:
      (state) =>
      (type_tag: string): Scheduler[] =>
        Object.values(state.entries).filter((entity) => entity.type_tag === type_tag),
  },

  actions: {
    add(entry: unknown) {
      const temp = SchedulerSchema.parse(entry);
      this.entries[temp.id] = temp;
    },

    remove(entry: string) {
      delete this.entries[entry];
    },

    set(raw: unknown[]) {
      this.entries = raw.reduce((acc: Record<string, Scheduler>, rawAcc: unknown) => {
        const record = SchedulerSchema.parse(rawAcc);
        acc[record.id] = record;
        return acc;
      }, {});
    },
    update(raw: unknown) {
      const temp = SchedulerSchema.parse(raw);
      this.entries[temp.id] = temp;
    },
  },
});
