import z from "zod/v4";

export const SchedulerSchema = z.object({
  id: z.uuid(),
  type_tag: z.string(),
  name: z.string(),
  status: z.boolean(),
  date: z.date(),
});
export type Scheduler = z.infer<typeof SchedulerSchema>;
