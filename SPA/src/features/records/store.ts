import { defineStore } from "pinia";
import api from "@/util/api";
import z from "zod/v4";

const RecordSchema = z.object({
  id: z.uuid(),
  type_tag: z.string(),
  name: z.string(),
  status: z.boolean(),
  optional_status: z.string().optional(),
  service_id: z.string().optional(),
});
const CreateRecordSchema = z.object({
  type_tag: z.string(),
  name: z.string(),
  status: z.boolean(),
  optional_status: z.string().optional(),
  service_id: z.string().optional(),
});

type RecordType = z.infer<typeof RecordSchema>;

export const useRecordStore = defineStore("record", {
  state: () => ({
    entries: {} as Record<string, RecordType>,
    placeholder: {} as string,
  }),
  persist: {
    storage: sessionStorage,
  },

  getters: {
    getRecord: (state) => (id: string) => state.entries[id],
    getAllRecords: (state) => Object.values(state.entries),
    getRecordsByStatus:
      (state) =>
      (status: boolean): RecordType[] =>
        Object.values(state.entries).filter((entity) => entity.status === status),

    getRecordsByType:
      (state) =>
      (type_tag: string): RecordType[] =>
        Object.values(state.entries).filter((entity) => entity.type_tag === type_tag),
  },

  actions: {
    set(raw: unknown[]) {
      this.entries = raw.reduce((acc: Record<string, RecordType>, rawAcc: unknown) => {
        const record = RecordSchema.parse(rawAcc);
        acc[record.id] = record;
        return acc;
      }, {});
    },
    async getRecord(id: string): Promise<string | null> {
      try {
        const response = await api.get(`/api/record/${id}`);
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

    async updateRecord(raw: unknown): Promise<null> {
      try {
        const response = await api.put("/api/record", raw);
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        const partial = RecordSchema.parse(raw);
        this.entries[partial.id] = partial;
        return null;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },

    async createRecord(raw: unknown): Promise<null> {
      try {
        const response = await api.post("/api/record", raw);
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        const parsed = CreateRecordSchema.parse(raw);
        // We already have raw + now the id → build the full & safe partial
        const full = { ...parsed, id: result.id };
        const partial = RecordSchema.parse(full);
        this.entries[partial.id] = partial;
        return null;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },

    async removeRecord(id: string): Promise<null> {
      try {
        const response = await api.delete(`/api/record/${id}`);
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

    async linkEntity(id: string): Promise<null> {
      try {
        const response = await api.put(`/api/record/${this.placeholder}/add-entity`, {
          params: { entity: id },
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

    async unlinkEntity(id: string): Promise<null> {
      try {
        const response = await api.put(`/api/record/${this.placeholder}/del-entity`, {
          params: { entity: id },
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

    async linkEvent(id: string): Promise<null> {
      try {
        const response = await api.put(`/api/record/${this.placeholder}/add-event`, {
          params: { event: id },
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

    async unlinkEvent(id: string): Promise<null> {
      try {
        const response = await api.put(`/api/record/${this.placeholder}/del-event`, {
          params: { event: id },
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
    async linkMovement(id: string): Promise<null> {
      try {
        const response = await api.put(`/api/record/${this.placeholder}/add-movement`, {
          params: { movement: id },
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

    async unlinkMovement(id: string): Promise<null> {
      try {
        const response = await api.put(`/api/record/${this.placeholder}/del-movement`, {
          params: { movement: id },
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
