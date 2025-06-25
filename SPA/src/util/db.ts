import type { Entity } from "@/features/entity/schema";
import axios from "axios";

export const writeEntity = async (value: Entity[]) => {
  const entityRecord: Record<string, Entity> = value.reduce(
    (acc: Record<string, Entity>, entity) => {
      acc[entity.id] = entity;

      return acc;
    },
    {},
  );

  try {
    await axios.post("http://localhost:3001", entityRecord);
    console.log("Successfully posted entity"); // Added for feedback
  } catch (error) {
    console.error("Error posting entity:", error); // Log the error
  }
};
