import { defineStore } from "pinia";

interface PartialScheduler {
  id: string;
  type_entry: string;
  name: string;
  status: boolean;
  date: string;
}

export const useSchedulerStore = defineStore("scheduler", {
  state: () => ({
    entries: {} as Record<string, PartialScheduler>,
  }),

  getters: {
    getEvent: (state) => (id: string) => state.entries[id],
    getAllEvents: (state) => state.entries,
  },

  actions: {
    add(entry: PartialScheduler) {
      this.entries[entry.id] = entry;
    },

    remove(entry: string) {
      delete this.entries[entry];
    },

    set(entry: PartialScheduler[]) {
      this.entries = Object.fromEntries(entry.map((e) => [e.id, e]));
    },
    update(entry: PartialScheduler) {
      this.entries[entry.id] = entry;
    },
  },
});
