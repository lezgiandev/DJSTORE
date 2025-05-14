import { defineStore } from 'pinia';
import { ref } from 'vue';
import {withdrawalsAPI, transactionsAPI, withdrawalsMockAPI} from '../api/api';
import type { Transaction, Withdrawal } from '@/types';

export const useFinanceStore = defineStore('finance', () => {
  const transactions = ref<Transaction[]>([]);
  const withdrawals = ref<Withdrawal[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function fetchTransactions() {
    try {
      loading.value = true;
      error.value = null;
      const response = await transactionsAPI.getTransactions();
      transactions.value = response.data;
    } catch (err: any) {
      console.error('Fetch transactions error:', err);
      error.value = err.response?.data?.detail || 'Ошибка при загрузке транзакций';
    } finally {
      loading.value = false;
    }
  }

  async function fetchWithdrawals() {
    try {
      loading.value = true;
      error.value = null;
      const response = await withdrawalsAPI.getWithdrawalsHistory();
      withdrawals.value = response.data;
    } catch (err: any) {
      console.error('Fetch withdrawals error:', err);
      error.value = err.response?.data?.detail || 'Ошибка при загрузке истории выводов';
    } finally {
      loading.value = false;
    }
  }

  async function createWithdrawal(data: {
    amount: number;
  }) {
    try {
      loading.value = true;
      error.value = null;
      const response = await withdrawalsMockAPI.createWithdrawal(data);
      await fetchWithdrawals();
      return response.data;
    } catch (err: any) {
      console.error('Create withdrawal error:', err);
      error.value = err.response?.data?.detail || 'Ошибка при создании заявки на вывод средств';
      return null;
    } finally {
      loading.value = false;
    }
  }

  return {
    transactions,
    withdrawals,
    loading,
    error,
    fetchTransactions,
    fetchWithdrawals,
    createWithdrawal
  };
}); 