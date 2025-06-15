import { defineStore } from "pinia";

interface PartialAddress {
  state: string;
  city: string;
}

interface PartialContact {
  number: string;
}

interface PartialEntity {
  id: string;
  name: string;
  email: string;
  govt_id: string;
  type_entity: string;
  id_type: string;
  status: boolean;
  address: PartialAddress[];
  phone: PartialContact[];
}

export const useEntityStore = defineStore("entity", {
  state: () => ({
    entries: {} as Record<string, PartialEntity>,
  }),

  getters: {
    getEntity: (state) => (id: string) => state.entries[id],
    getAllEntities: (state) => state.entries,
  },

  actions: {
    addEntity(entry: PartialEntity) {
      this.entries[entry.id] = entry;
    },

    removeEntity(id: string) {
      delete this.entries[id];
    },

    set(entry: PartialEntity[]) {
      this.entries = Object.fromEntries(entry.map((e) => [e.id, e]));
    },
    updateEntity(entry: PartialEntity) {
      this.entries[entry.id] = entry;
    },
  },
});
