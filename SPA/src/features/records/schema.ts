import z from "zod/v4";

export const RecordSchema = z.object({
  id: z.uuid(),
  type_tag: z.string(),
  name: z.string(),
  status: z.boolean(),
  optional_status: z.string().optional(),
  service_id: z.string().optional(),
});

export type RecordType = z.infer<typeof RecordSchema>;
