import { defineStore } from "pinia";
import api from "@/util/api";
import z from "zod/v4";

const EntitySchema = z.object({
  id: z.uuid(),
  name: z.string(),
  email: z.string(),
  document: z.string(),
  type_tag: z.string(),
  document_type: z.string(),
  status: z.boolean(),
});
const CreateEntitySchema = z.object({
  name: z.string(),
  email: z.string(),
  document: z.string(),
  type_tag: z.string(),
  document_type: z.string(),
  status: z.boolean(),
});

type Entity = z.infer<typeof EntitySchema>;

export const useEntityStore = defineStore("entity", {
  state: () => ({
    entries: {} as Record<string, Entity>, // Cache of entities by ID
  }),
  persist: {
    storage: sessionStorage,
  },

  getters: {
    getEntity:
      (state) =>
      (id: string): Entity | undefined =>
        state.entries[id],

    getEntitiesByStatus:
      (state) =>
      (status: boolean): Entity[] =>
        Object.values(state.entries).filter((entity) => entity.status === status),

    getEntitiesByType:
      (state) =>
      (type_tag: string): Entity[] =>
        Object.values(state.entries).filter((entity) => entity.type_tag === type_tag),

    getAllEntities: (state) => Object.values(state.entries), // Get all entities as an array
    // Add other helpful getters, e.g., getActiveEntities
  },

  actions: {
    set(raw: unknown[]) {
      this.entries = raw.reduce((acc: Record<string, Entity>, rawAcc: unknown) => {
        const record = EntitySchema.parse(rawAcc);
        acc[record.id] = record;
        return acc;
      }, {});
    },

    async getEntity(id: string): Promise<string | null> {
      try {
        const response = await api.get(`/api/entity/${id}`);
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        return result;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },

    async updateEntity(raw: unknown): Promise<string | null> {
      try {
        const response = await api.put("/api/entity", raw);
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        const partial = EntitySchema.parse(raw);
        this.entries[partial.id] = partial;
        return null;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },

    async createEntity(raw: unknown): Promise<string | null> {
      try {
        const response = await api.post("/api/entity", raw);
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        const parsed = CreateEntitySchema.parse(raw);
        // We already have raw + now the id → build the full & safe partial
        const full = { ...parsed, id: result.id };
        const partial = EntitySchema.parse(full);
        this.entries[partial.id] = partial;
        return partial.id;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },

    async removeEntity(id: string): Promise<string | null> {
      try {
        const response = await api.delete(`/api/entity/${id}`);
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        // We already have raw + now the id → build the full & safe partial
        delete this.entries[id];
        return null;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },
    async createAddress(raw: unknown): Promise<null> {
      try {
        const response = await api.post("/api/entity/address", raw);
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        return null;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },
    async updateAddress(raw: unknown): Promise<null> {
      try {
        const response = await api.put("/api/entity/address", raw);
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        return null;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },
    async deleteAddress(entity: string, address: string): Promise<null> {
      try {
        const response = await api.delete(`/api/entity/${entity}/address`, {
          params: { address: address },
        });
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        return null;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },
    async createContact(raw: unknown): Promise<null> {
      try {
        const response = await api.post("/api/entity/contact", raw);
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        return null;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },
    async updateContact(raw: unknown): Promise<null> {
      try {
        const response = await api.put("/api/entity/contact", raw);
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        return null;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },
    async deleteContact(entity: string, contact: string): Promise<null> {
      try {
        const response = await api.delete(`/api/entity/${entity}/contact`, {
          params: { contact: contact },
        });
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        return null;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },
  },
});
