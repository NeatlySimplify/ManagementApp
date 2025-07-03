import { defineStore } from "pinia";
import api from "@/util/api";
import z from "zod/v4";

const SchedulerSchema = z.object({
  id: z.uuid(),
  type_tag: z.string(),
  name: z.string(),
  status: z.boolean(),
  date_beginning: z.date(),
  date_ending: z.date(),
});
const CreateSchedulerSchema = z.object({
  type_tag: z.string(),
  name: z.string(),
  status: z.boolean(),
  date_beginning: z.date(),
  date_ending: z.optional(z.date()),
});
type Scheduler = z.infer<typeof SchedulerSchema>;

export const useSchedulerStore = defineStore("scheduler", {
  state: () => ({
    entries: {} as Record<string, Scheduler>,
  }),
  persist: {
    storage: sessionStorage,
  },

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

    getMonthlyEvents:
      (state) =>
      (referenceDate: Date): Scheduler[] => {
        const start = new Date(referenceDate.getFullYear(), referenceDate.getMonth(), 1);
        const end = new Date(referenceDate.getFullYear(), referenceDate.getMonth() + 1, 0);

        const events = Object.values(state.entries).filter((event) => {
          return (
            event.status === false && event.date_beginning >= start && event.date_beginning <= end
          );
        });

        return events.sort((a, b) => a.date_beginning.getTime() - b.date_beginning.getTime());
      },
  },

  actions: {
    set(raw: unknown[]) {
      this.entries = raw.reduce((acc: Record<string, Scheduler>, rawAcc: unknown) => {
        const record = SchedulerSchema.parse(rawAcc);
        acc[record.id] = record;
        return acc;
      }, {});
    },
    async getScheduler(id: string): Promise<string | null> {
      try {
        const response = await api.get(`/api/scheduler/${id}`);
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

    async updateScheduler(raw: unknown): Promise<null> {
      try {
        const response = await api.put("/api/scheduler", raw);
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        const partial = SchedulerSchema.parse(raw);
        this.entries[partial.id] = partial;
        return null;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },

    async createRecord(raw: unknown): Promise<null> {
      try {
        const response = await api.post("/api/scheduler", raw);
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        const parsed = CreateSchedulerSchema.parse(raw);
        // We already have raw + now the id → build the full & safe partial
        const full = { ...parsed, id: result.id };
        const partial = SchedulerSchema.parse(full);
        this.entries[partial.id] = partial;
        return null;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },

    async removeScheduler(id: string): Promise<null> {
      try {
        const response = await api.delete(`/api/scheduler/${id}`);
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
  },
});
