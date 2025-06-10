import { defineStore } from "pinia";

interface Entity {
  id: string;

  // other fields — will be used only by Rust/WASM for filtering
}

export const useEntryStore = defineStore("entries", {
  state: () => ({
    entries: {} as Record<string, Entity>,
  }),

  getters: {
    getById: (state) => (id: string) => state.entries[id],
  },

  actions: {
    add(entry: Entity) {
      this.entries[entry.id] = entry;
    },

    remove(id: string) {
      delete this.entries[id];
    },

    set(entries: Entity[]) {
      this.entries = Object.fromEntries(entries.map((e) => [e.id, e]));
    },

    clear() {
      this.entries = {};
    },
  },
});
