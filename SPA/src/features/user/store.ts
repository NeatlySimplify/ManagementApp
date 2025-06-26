import { defineStore } from "pinia";
import {
  type User,
  type BankAccount,
  UserSchema,
  BankAccountSchema,
  type Settings,
  SettingsSchema,
} from "./schema";

export const useUserStore = defineStore("user", {
  state: () => ({
    user: {} as User,
    bank_account: {} as Record<string, BankAccount>,
    total_balance: {} as string,
    setting: {} as Settings,
  }),
  persist: {
    storage: sessionStorage,
  },

  getters: {
    getUser: (state) => state.user,
    getAccount: (state) => (id: string) => state.bank_account[id],
    getSettings: (state) => state.setting,
    getAllAccounts: (state) => state.bank_account,
    getBalance: (state) => state.total_balance,
  },

  actions: {
    addAccount(entry: BankAccount) {
      this.bank_account[entry.id] = entry;
    },

    setUser(raw: unknown, auth: boolean) {
      const user: User = UserSchema.parse(raw);
      this.user.name = user.name;
      this.user.email = user.email;
      this.user.auth = auth;
    },
    setSettings(raw: unknown) {
      const set: Settings = SettingsSchema.parse(raw);
      this.setting = set;
    },

    removeAccount(entry: string) {
      delete this.bank_account[entry];
    },

    setAccounts(raw: unknown[]) {
      this.bank_account = raw.reduce((acc: Record<string, BankAccount>, rawAccount: unknown) => {
        const bankAccount = BankAccountSchema.parse(rawAccount);
        acc[bankAccount.id] = bankAccount;
        return acc;
      }, {});
    },

    update(entry: BankAccount) {
      this.bank_account[entry.id] = entry;
    },
  },
});
