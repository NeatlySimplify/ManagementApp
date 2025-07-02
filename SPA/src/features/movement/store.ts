import { defineStore } from "pinia";
import z from "zod/v4";
import api from "@/util/api";

const PaymentSchema = z.object({
  id: z.uuid(),
  name: z.string(),
  type_tag: z.string(),
  value_str: z.coerce.bigint(),
  payment_date: z.coerce.date(),
  status: z.boolean(),
  movement: z.string(), // Movement.id
});
type Payment = z.infer<typeof PaymentSchema>;

const CreateMovementSchema = z.object({
  type_tag: z.string(),
  value_str: z.coerce.bigint(),
  installment: z.number(),
});

const MovementSchema = z.object({
  id: z.string(),
  type_tag: z.string(),
  value_str: z.coerce.bigint(),
  installment: z.number(),
});
type Movement = z.infer<typeof MovementSchema>;

export const useMovementStore = defineStore("movement", {
  state: () => ({
    movement: {} as Record<string, Movement>,
    payment: {} as Record<string, Payment>,
  }),
  persist: {
    storage: sessionStorage,
  },

  getters: {
    getMovement: (state) => (id: string) => state.movement[id],
    getAllMovement: (state) => state.movement,
    getPayment: (state) => (id: string) => state.payment[id],
    getPaymentWindow:
      (state) =>
      (referenceDate: Date, tag: string): Payment[] => {
        const start = new Date(referenceDate);
        start.setDate(1);
        const end = new Date(referenceDate);
        end.setDate(0);
        const relevantPayments = Object.values(state.payment).filter(
          (pay) => pay.type_tag === tag && pay.payment_date >= start && pay.payment_date <= end,
        );
        return relevantPayments;
      },
    getActiveMovement:
      (state) =>
      (referenceDate: Date): Movement[] => {
        // Create window: 3 months before and after the reference date
        const start = new Date(referenceDate);
        start.setMonth(start.getMonth() - 3);

        const end = new Date(referenceDate);
        end.setMonth(end.getMonth() + 3);

        // Step 1: Filter relevant payments in that range
        const relevantPayments = Object.values(state.payment).filter(
          (pay) => pay.payment_date >= start && pay.payment_date <= end,
        );

        // Step 2: Collect unique movement IDs
        const movementIds = new Set(relevantPayments.map((p) => p.movement));

        // Step 3: Map to Movement objects, filtering out missing entries
        return Array.from(movementIds)
          .map((id) => state.movement[id])
          .filter((m): m is Movement => !!m);
      },
  },

  actions: {
    setMovement(raw: unknown[]) {
      this.movement = raw.reduce((acc: Record<string, Movement>, rawAcc: unknown) => {
        const record = MovementSchema.parse(rawAcc);
        acc[record.id] = record;
        return acc;
      }, {});
    },
    setPayment(raw: unknown[]) {
      this.payment = raw.reduce((acc: Record<string, Payment>, rawAcc: unknown) => {
        const record = PaymentSchema.parse(rawAcc);
        acc[record.id] = record;
        return acc;
      }, {});
    },
    async getMovement(id: string): Promise<string | null> {
      try {
        const response = await api.get(`/api/movement/${id}`);
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

    async updateMovement(raw: unknown): Promise<null> {
      try {
        const response = await api.put("/api/movement", raw);
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        const partial = MovementSchema.parse(raw);
        this.movement[partial.id] = partial;
        return null;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },

    async createMovement(raw: unknown): Promise<null> {
      try {
        const response = await api.post("/api/movement", raw);
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        const parsed = CreateMovementSchema.parse(raw);
        // We already have raw + now the id → build the full & safe partial
        const full = { ...parsed, id: result.id };
        const partial = MovementSchema.parse(full);
        this.movement[partial.id] = partial;
        return null;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },

    async removeMovement(id: string): Promise<null> {
      try {
        const response = await api.delete(`/api/movement/${id}`);
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        // We already have raw + now the id → build the full & safe partial
        delete this.movement[id];
        return null;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },
    async getPayment(id: string): Promise<string | null> {
      try {
        const response = await api.get(`/api/movement/payment/${id}`);
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
    async deletePayment(id: string): Promise<null> {
      try {
        const response = await api.delete(`/api/movement/payment/${id}`);
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        delete this.payment[id];
        return null;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },
    async updatePayment(raw: unknown): Promise<null> {
      try {
        const response = await api.put("/api/movement/payment", raw);
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        const partial = PaymentSchema.parse(raw);
        this.payment[partial.id] = partial;
        return null;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },
  },
});
