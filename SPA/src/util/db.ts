import { type Entity } from "@/features/entity/schema";
import axios from "axios";

export const writeEntity = async (value: Entity[]) => {
  for (let entity = 0; entity < value.length; entity++) {
    try {
      await axios.post("/entity", entity);
      console.log("Successfully posted entity"); // Added for feedback
    } catch (error) {
      console.error("Error posting entity:", error); // Log the error
    }
  }
};
