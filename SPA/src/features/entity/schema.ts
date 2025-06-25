import z from "zod/v4";

const AddressSchema = z.object({
  state: z.string(),
  city: z.string(),
});

const ContactSchema = z.object({
  number: z.string(),
});

export const EntitySchema = z.object({
  id: z.uuid(),
  name: z.string(),
  email: z.string(),
  document: z.string(),
  type_tag: z.string(),
  document_type: z.string(),
  status: z.boolean(),
  address: z.array(AddressSchema),
  phone: z.array(ContactSchema),
});

export type Entity = z.infer<typeof EntitySchema>;
