import { defineStore } from "pinia";
import { RecordSchema, type RecordType } from "./schema";

export const useRecordStore = defineStore("record", {
  state: () => ({
    entries: {} as Record<string, RecordType>,
  }),

  getters: {
    getRecord: (state) => (id: string) => state.entries[id],
    getAllRecords: (state) => state.entries,
  },

  actions: {
    add(entry: unknown) {
      const temp = RecordSchema.parse(entry);
      this.entries[temp.id] = temp;
    },

    remove(entry: string) {
      delete this.entries[entry];
    },

    set(raw: unknown[]) {
      this.entries = raw.reduce((acc: Record<string, RecordType>, rawAcc: unknown) => {
        const record = RecordSchema.parse(rawAcc);
        acc[record.id] = record;
        return acc;
      }, {});
    },
    update(raw: unknown) {
      const temp = RecordSchema.parse(raw);
      this.entries[temp.id] = temp;
    },
  },
});
