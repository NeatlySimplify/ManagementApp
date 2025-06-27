import { defineStore } from "pinia";
import type { Entity } from "./schema";

export const useEntityStore = defineStore("entity", {
  state: () => ({
    entries: {} as Record<string, Entity>, // Cache of entities by ID
    isLoading: false, // For initial bundle loading
  }),

  getters: {
    getEntity:
      (state) =>
      (id: string): Entity | undefined =>
        state.entries[id],
    getAllEntities: (state) => Object.values(state.entries), // Get all entities as an array
    // Add other helpful getters, e.g., getActiveEntities
  },

  actions: {
    setAllEntities(entities: Entity[]) {
      this.entries = Object.fromEntries(entities.map((e) => [e.id, e]));
    },

    // --- Individual Entity Actions (for one-to-one sync after backend success) ---

    // Adds a new entity to the cache
    addEntity(entity: Entity) {
      this.entries[entity.id] = entity;
    },

    // Updates an existing entity in the cache
    updateEntity(entity: Entity) {
      if (this.entries[entity.id]) {
        this.entries[entity.id] = entity;
      } else {
        console.warn(
          `Attempted to update non-existent entity with ID: ${entity.id}. Adding it instead.`,
        );
        this.addEntity(entity); // Or throw an error, depending on desired behavior
      }
    },

    // Removes an entity from the cache
    removeEntity(id: string) {
      delete this.entries[id];
    },
  },
});
