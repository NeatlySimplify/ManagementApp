import { defineStore } from "pinia";

interface PartialBankAccount {
  id: string;
  bank_name: string;
  account_name: string;
  balance_str: string;
}

interface Settings {
  id: string;
  account_types: string[];
  default_bank_account: PartialBankAccount["id"];
  record_title: string;
  movement_title: string;
  entity_title: string;
  entity_types: string[];
  entity_id_types: string[];
  contact_number_types: string[];
  record_types: string[];
  record_status: string[];
  movement_income_types: string[];
  movement_expense_types: string[];
  scheduler_types: string[];
  movement_cycle_types: string[];
}

interface User {
  name: string;
  email: string;
  settings: Settings;
  auth: boolean;
}

export const useUserStore = defineStore("user", {
  state: () => ({
    user: {} as User,
    bank_account: {} as Record<string, PartialBankAccount>,
    total_balance: {} as string
  }),

  getters: {
    getUser: (state) => state.user,
    getAccount: (state) => (id: string) => state.bank_account[id],
    getSettings: (state) => state.user.settings,
    getAllAccounts: (state) => state.bank_account,
    getBalance: (state) => state.total_balance,
  },

  actions: {
    addAccount(entry: PartialBankAccount) {
      this.bank_account[entry.id] = entry;
    },

    setUser({name, email, auth, settings}: User, balance: string) {
      this.user.name = name;
      this.user.email = email;
      this.user.auth = auth;
      this.user.settings = settings;
      this.total_balance = balance;
    },

    removeAccount(entry: string) {
      delete this.bank_account[entry];
    },

    setAccounts(entry: PartialBankAccount[]) {
      this.bank_account = Object.fromEntries(entry.map((e) => [e.id, e]));
    },

    update(entry: PartialBankAccount) {
      this.bank_account[entry.id] = entry;
    },
  },
});
