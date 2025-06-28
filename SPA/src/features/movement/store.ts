import { defineStore } from "pinia";

interface PartialMovement {
  id: string;
  type_movement: string;
  value_str: string;
  installment: number;
}

interface PartialPayment {
  id: string;
  name: string;
  type_payment: string;
  value_str: string;
  payment_date: string;
  status: boolean;
  movement: PartialMovement["id"];
}

export const useMovementStore = defineStore("movement", {
  state: () => ({
    movement: {} as Record<string, PartialMovement>,
    income: {} as Record<string, PartialPayment>,
    expense: {} as Record<string, PartialPayment>,
  }),

  getters: {
    getMovement: (state) => (id: string) => state.movement[id],
    getAllMovement: (state) => state.movement,
    getIncome: (state) => (id: string) => state.income[id],
    getAllIncome: (state) => state.income,
    getExpense: (state) => (id: string) => state.expense[id],
    getAllExpense: (state) => state.expense,
  },

  actions: {
    addMovement(entry: PartialMovement) {
      this.movement[entry.id] = entry;
    },
    removeMovement(id: string) {
      delete this.movement[id];
    },
    removeIncome(id: string) {
      delete this.income[id];
    },
    removeExpense(id: string) {
      delete this.expense[id];
    },
    setMovement(entry: PartialMovement[]) {
      this.movement = Object.fromEntries(entry.map((e) => [e.id, e]));
    },
    setIncome(entry: PartialPayment[]) {
      this.income = Object.fromEntries(entry.map((e) => [e.id, e]));
    },
    setExpense(entry: PartialPayment[]) {
      this.expense = Object.fromEntries(entry.map((e) => [e.id, e]));
    },
    updateMovement(entry: PartialMovement) {
      this.movement[entry.id] = entry;
    },
    updateIncome(entry: PartialPayment) {
      this.income[entry.id] = entry;
    },
    updateExpense(entry: PartialPayment) {
      this.expense[entry.id] = entry;
    },
  },
});
