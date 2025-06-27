import z from "zod/v4";

export const EntitySchema = z.object({
  id: z.uuid(),
  name: z.string(),
  email: z.string(),
  document: z.string(),
  type_tag: z.string(),
  document_type: z.string(),
  status: z.boolean(),
});

export type Entity = z.infer<typeof EntitySchema>;
