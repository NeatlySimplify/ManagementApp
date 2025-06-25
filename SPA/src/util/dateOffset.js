export default function getDateOffsetsISO(baseDate = new Date(), numDates = 1, interval = "daily") {
  const dateList = [];
  let currentDate = new Date(baseDate); // Work with a copy of the base date

  for (let i = 0; i < numDates; i++) {
    // Format the current date into YYYY-MM-DD
    const year = currentDate.getFullYear();
    const month = String(currentDate.getMonth() + 1).padStart(2, "0");
    const day = String(currentDate.getDate()).padStart(2, "0");
    dateList.push(`${year}-${month}-${day}`);

    // Calculate the next date based on the interval
    switch (interval.toLowerCase()) {
      case "daily":
        currentDate.setDate(currentDate.getDate() + 1);
        break;
      case "weekly":
        currentDate.setDate(currentDate.getDate() + 7);
        break;
      case "monthly":
        currentDate.setMonth(currentDate.getMonth() + 1);
        break;
      case "yearly":
        currentDate.setFullYear(currentDate.getFullYear() + 1);
        break;
      default:
        // If an invalid interval is given, just default to daily
        console.warn(`Invalid interval "${interval}" provided. Defaulting to 'daily'.`);
        currentDate.setDate(currentDate.getDate() + 1);
    }
  }

  return dateList;
}
