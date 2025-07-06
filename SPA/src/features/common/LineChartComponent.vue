<script setup>
import { Line } from "vue-chartjs";
import { useMovementStore } from "@/features/movement/store";
import { defineProps, computed } from "vue";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  CategoryScale,
} from "chart.js";

ChartJS.register(Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale);

const movementStore = useMovementStore();
const prop = defineProps({
  referenceDate: Date,
});

// Helper function to group payments by week
const groupPaymentsByWeek = (payments, referenceDate) => {
  const paymentsByWeek = [0n, 0n, 0n, 0n];
  const firstDayOfMonth = new Date(prop.referenceDate.getFullYear(), referenceDate.getMonth(), 1);
  const firstDayOfMonthWeekday = firstDayOfMonth.getDay(); // 0 (Sun) to 6 (Sat)

  payments.forEach((payment) => {
    const paymentDate = new Date(payment.payment_date);
    const dayOfMonth = paymentDate.getDate();

    // Adjust for the starting weekday of the month
    const adjustedDay = dayOfMonth + firstDayOfMonthWeekday - 1;
    const weekNumber = Math.floor(adjustedDay / 7);

    if (weekNumber >= 0 && weekNumber < 4) {
      paymentsByWeek[weekNumber] += payment.value_str;
    }
  });
  return paymentsByWeek;
};

const income = computed(() => {
  const incomePayments = movementStore.getPaymentWindow(prop.referenceDate, "income");
  return groupPaymentsByWeek(incomePayments, prop.referenceDate);
});

const expense = computed(() => {
  const expensePayments = movementStore.getPaymentWindow(prop.referenceDate, "expense");
  return groupPaymentsByWeek(expensePayments, prop.referenceDate);
});

const chartData = computed(() => {
  return {
    labels: ["1º Semana", "2º Semana", "3º Semana", "4º Semana"],
    datasets: [
      {
        label: "Entrada",
        data: [
          Number(income.value[0]),
          Number(income.value[1]),
          Number(income.value[2]),
          Number(income.value[3]),
        ],
        borderColor: "rgb(75, 192, 192)",
        tension: 0.1,
      },
      {
        label: "Saída",
        data: [
          Number(expense.value[0]),
          Number(expense.value[1]),
          Number(expense.value[2]),
          Number(expense.value[3]),
        ],
        borderColor: "rgb(255, 99, 132)",
        tension: 0.1,
      },
    ],
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
    },
  },
};
</script>
<template>
  <div class="container">
    <Line
      :data="chartData"
      :options="chartOptions"
    />
  </div>
</template>
