import { defineStore } from "pinia";
import z from "zod/v4";
import api from "@/util/api";

const BankAccountSchema = z.object({
  id: z.uuid(),
  bank_name: z.string(),
  account_name: z.string(),
  balance_str: z.coerce.bigint(),
  ignore_on_totals: z.boolean(),
});
const CreateBankAccountSchema = z.object({
  bank_name: z.string(),
  account_name: z.string(),
  balance_str: z.coerce.bigint(),
  ignore_on_totals: z.boolean(),
});
type BankAccount = z.infer<typeof BankAccountSchema>;

const SettingsSchema = z.object({
  id: z.string(),
  account_types: z.array(z.string()),
  default_bank_account: z.uuid(),
  record_title: z.string(),
  movement_title: z.string(),
  entity_title: z.string(),
  entity_types: z.array(z.string()),
  entity_document_types: z.array(z.string()),
  contact_number_types: z.array(z.string()),
  record_types: z.array(z.string()),
  record_status: z.array(z.string()),
  movement_income_types: z.array(z.string()),
  movement_expense_types: z.array(z.string()),
  scheduler_types: z.array(z.string()),
  movement_cycle_types: z.array(z.string()),
  relationship_status: z.array(z.string()),
  sex: z.array(z.string()),
});
export type Settings = z.infer<typeof SettingsSchema>;

export const UserSchema = z.object({
  name: z.string(),
  email: z.string(),
  auth: z.boolean().default(false),
});
export type User = z.infer<typeof UserSchema>;

export const useUserStore = defineStore("user", {
  state: () => ({
    user: {} as User,
    bank_account: {} as Record<string, BankAccount>,
    setting: {} as Settings,
    placeholder: {} as string,
  }),
  persist: {
    storage: sessionStorage,
  },

  getters: {
    getUser: (state) => state.user,
    getAccount: (state) => (id: string) => state.bank_account[id],
    getSettings: (state) => state.setting,
    getAllAccounts: (state) => Object.values(state.bank_account),
    getTotalBalance: (state) => {
      return Object.values(state.bank_account)
        .filter((account) => !account.ignore_on_totals)
        .reduce((total, account) => total + BigInt(account.balance_str), 0n)
        .toString(); // Pode retornar como bigint ou string
    },
    getGroupedAccounts: (state) => {
      const included: { account_name: string; balance: string }[] = [];
      const ignored: { account_name: string; balance: string }[] = [];
      for (const account of Object.values(state.bank_account)) {
        const item = {
          account_name: account.account_name,
          balance: BigInt(account.balance_str).toString(),
        };

        if (account.ignore_on_totals) {
          ignored.push(item);
        } else {
          included.push(item);
        }
      }

      return {
        included,
        ignored,
      };
    },
  },

  actions: {
    setUser(raw: unknown) {
      const user: User = UserSchema.parse(raw);
      this.user = { ...user };
    },

    setSettings(raw: unknown) {
      const set: Settings = SettingsSchema.parse(raw);
      this.setting = set;
    },

    setAccounts(raw: unknown[]) {
      this.bank_account = raw.reduce((acc: Record<string, BankAccount>, rawAccount: unknown) => {
        const bankAccount = BankAccountSchema.parse(rawAccount);
        acc[bankAccount.id] = bankAccount;
        return acc;
      }, {});
    },

    async getData(): Promise<string | null> {
      try {
        const response = await api.get(`/api/user/`);
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        return result.data;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },

    async getBankAccount(): Promise<string | null> {
      try {
        const response = await api.get(`/api/user/bank-account`);
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

    async updateUser(raw: unknown): Promise<null> {
      try {
        const response = await api.put(`/api/user/`, raw);
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        const new_user = UserSchema.parse(raw);
        this.user.email = new_user.email || this.user.email;
        this.user.name = new_user.name || this.user.name;
        return result;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },

    async updateSettings(raw: unknown): Promise<null> {
      try {
        const response = await api.put(`/api/user/settings`, raw);
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

    async updateBankAccount(raw: unknown): Promise<null> {
      try {
        const response = await api.put(`/api/user/bank-account`, raw);
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

    async createSettings(raw: unknown): Promise<null> {
      try {
        const response = await api.put(`/api/user/settings`, raw);
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

    async createBankAccount(raw: unknown): Promise<null> {
      try {
        const response = await api.put(`/api/user/bank-account`, raw);
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        const partial = CreateBankAccountSchema.parse(raw);
        const full = BankAccountSchema.parse(partial, result.id);
        this.bank_account[full.id] = full;
        return null;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },

    async removeBankAccount(id: string): Promise<null> {
      try {
        const response = await api.delete(`/api/user/bank-account/${id}`);
        const { status, result } = response.data;
        if (status !== "success") {
          console.error("Server rejected creation:", result);
          return null;
        }
        delete this.bank_account[id];
        return null;
      } catch (err) {
        console.error("Unexpected error:", err);
        return null;
      }
    },
  },
});
