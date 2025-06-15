import { defineStore } from "pinia";

interface PartialRecord {
  id: string;
  type_record: string;
  name: string;
  status: string;
  active: boolean;
  id_service: string;
}

export const useRecordStore = defineStore("record", {
  state: () => ({
    entries: {} as Record<string, PartialRecord>,
  }),

  getters: {
    getRecord: (state) => (id: string) => state.entries[id],
    getAllRecords: (state) => state.entries,
  },

  actions: {
    add(entry: PartialRecord) {
      this.entries[entry.id] = entry;
    },

    remove(entry: string) {
      delete this.entries[entry];
    },

    set(entry: PartialRecord[]) {
      this.entries = Object.fromEntries(entry.map((e) => [e.id, e]));
    },
    update(entry: PartialRecord) {
      this.entries[entry.id] = entry;
    },
  },
});
