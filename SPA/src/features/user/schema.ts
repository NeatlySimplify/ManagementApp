import z from "zod/v4";

export const BankAccountSchema = z.object({
  id: z.uuid(),
  bank_name: z.string(),
  account_name: z.string(),
  balance_str: z.coerce.bigint(),
  ignore_on_totals: z.boolean(),
});
export type BankAccount = z.infer<typeof BankAccountSchema>;

export const SettingsSchema = z.object({
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
