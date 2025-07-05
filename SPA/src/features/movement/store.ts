import { defineStore } from "pinia";
import z from "zod/v4";
import api from "@/util/api";
import { useSchedulerStore, SchedulerSchema } from "@/features/scheduler/store";

const schedulerStore = useSchedulerStore();

const PaymentSchema = z.object({
  id: z.uuid(),
  name: z.string(),
  type_tag: z.string(),
  value: z.coerce.bigint(),
  payment_date: z.coerce.date(),
  is_due: z.coerce.date(),
  status: z.boolean(),
  movement: z.string(), // Movement.id
});
type Payment = z.infer<typeof PaymentSchema>;

const PaymentResponseSchema = z.object({
  id: z.uuid(),
  name: z.string(),
  type_tag: z.string(),
  value: z.coerce.bigint(),
  payment_date: z.coerce.date(),
  is_due: z.coerce.date(),
  status: z.boolean(),
  movement: z.string(),
  event: SchedulerSchema,
});

const MovementResponseSchema = z.object({
  payment: z.array(PaymentResponseSchema),
});

const CreateMovementSchema = z.object({
  type_tag: z.string(),
  value: z.coerce.bigint(),
  installment: z.number(),
});

const MovementSchema = z.object({
  id: z.string(),
  type_tag: z.string(),
  value: z.coerce.bigint(),
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
      (referenceDate: Date, tag: string | null): Payment[] => {
        const start = new Date(referenceDate);
        start.setDate(1);
        const end = new Date(referenceDate.getFullYear(), referenceDate.getMonth() + 1);
        end.setDate(1);
        let relevantPayments;
        if (tag) {
          relevantPayments = Object.values(state.payment).filter(
            (pay) => pay.type_tag === tag && pay.payment_date >= start && pay.payment_date < end,
          );
        } else {
          relevantPayments = Object.values(state.payment).filter(
            (pay) => pay.payment_date >= start && pay.payment_date < end,
          );
        }
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
    getExpectedCashFlow: (state) => (referenceDate: Date) => {
      const start = new Date(referenceDate);
      start.setDate(1);
      const end = new Date(referenceDate);
      end.setMonth(end.getMonth() + 1);
      end.setDate(0); // last day of the month

      const relevantPayments = Object.values(state.payment).filter((pay) => {
        return pay.status === false && pay.payment_date >= start && pay.payment_date <= end;
      });

      let income = 0n;
      let expense = 0n;

      for (const payment of relevantPayments) {
        const val = BigInt(payment.value);
        if (payment.type_tag.startsWith("Entrada")) {
          income += val;
        } else if (payment.type_tag.startsWith("Saída")) {
          expense += val;
        }
      }

      return {
        income: income.toString(), // or keep as bigint
        expense: expense.toString(),
        net: (income - expense).toString(),
      };
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
    async fetchMovement(id: string): Promise<string | null> {
      try {
        const response = await api.get(`/api/movement/${id}`);
        const result = response.data;
        if (response.status !== 200) {
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
        const request = await api.post("/api/movement", raw);
        const { status, result } = request.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        const parsed = CreateMovementSchema.parse(raw);
        // We already have raw + now the id → build the full & safe partial
        const full = { ...parsed, id: result.id };
        const partial = MovementSchema.parse(full);
        this.movement[partial.id] = partial;
        const response = await this.fetchMovement(partial.id);

        if (response) {
          try {
            // Parse the response using the Zod schema
            const parsedResponse = MovementResponseSchema.parse(response);

            // Access the payment array from the parsed response

            this.setPayment(parsedResponse.payment);
            const event_list = [];
            for (let i = 0; i < parsedResponse.payment.length; i++) {
              const eventObj = parsedResponse.payment[i].event;
              event_list.push(eventObj);
            }
            schedulerStore.set(event_list);
          } catch (error) {
            console.error("Error parsing fetchMovement response:", error);
            return null; // Or handle the error as needed
          }
        }

        return null;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },

    async removeMovement(id: string): Promise<null> {
      try {
        const bag = this.fetchMovement(id);
        const response = await api.delete(`/api/movement/${id}`);
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        // We already have raw + now the id → build the full & safe partial
        delete this.movement[id];
        if (bag) {
          try {
            // Parse the response using the Zod schema
            const parsedResponse = MovementResponseSchema.parse(bag);
            const payments = parsedResponse.payment;
            for (let i = 0; i < payments.length; i++) {
              schedulerStore.directDelete(payments[i].event.id);
              delete this.payment[id];
            }
          } catch (error) {
            console.error("Error parsing fetchMovement response:", error);
            return null; // Or handle the error as needed
          }
        }

        return null;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },
    async fetchPayment(id: string): Promise<string | null> {
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
