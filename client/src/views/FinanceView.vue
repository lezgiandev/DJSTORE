<template>
  <div class="min-h-screen bg-light-bg dark:bg-gray-900 flex flex-col">
    <NavBar />

    <main class="flex-1 container mx-auto px-4 py-8 md:py-12">
      <div class="max-w-4xl mx-auto">
        <h1 class="text-3xl md:text-4xl font-bold mb-6 md:mb-10 bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent animate-fade-in">
          Финансовые операции
        </h1>

        <!-- Блок баланса -->
        <div v-if="authStore.state.profile" class="bg-light-bg-secondary dark:bg-gray-800/40 backdrop-blur-lg p-6 md:p-8 rounded-2xl border border-light-border dark:border-gray-700/30 shadow-xl mb-8">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 md:gap-6">
            <div class="flex items-center space-x-3 md:space-x-4">
              <div class="p-2.5 bg-green-400/10 rounded-lg border border-green-400/20">
                <CurrencyDollarIcon class="w-7 h-7 text-green-400" />
              </div>
              <div>
                <p class="text-sm md:text-base text-light-text-secondary dark:text-gray-400">Доступный баланс</p>
                <p class="text-2xl md:text-3xl font-bold text-green-400">
                  {{ authStore.state.profile.balance }} ₽
                </p>
              </div>
            </div>
            <router-link
                to="/withdrawals"
                class="flex items-center justify-center space-x-2 px-5 py-2.5 md:px-6 md:py-3 bg-gradient-to-r from-purple-600/30 to-blue-500/30 hover:from-purple-600/50 hover:to-blue-500/50 rounded-xl border border-purple-400/30 hover:border-purple-400/50 transition-all group"
            >
              <ArrowUpCircleIcon class="w-6 h-6 text-purple-400 group-hover:rotate-45 transition-transform" />
              <span class="text-purple-400 group-hover:text-white transition-colors">Вывод средств</span>
            </router-link>
          </div>
        </div>

        <!-- История транзакций -->
        <div class="bg-light-bg-secondary dark:bg-gray-800/40 backdrop-blur-lg p-6 md:p-8 rounded-2xl border border-light-border dark:border-gray-700/30 shadow-xl">
          <h2 class="text-xl md:text-2xl font-bold text-light-text dark:text-gray-200 mb-6 bg-gradient-to-r from-blue-400/30 to-cyan-400/30 w-max px-4 py-1 rounded-full">
            История операций
          </h2>

          <div v-if="financeStore.loading" class="text-center p-6 bg-light-bg dark:bg-gray-900/20 rounded-xl border border-light-border dark:border-gray-700/30">
            <div class="flex items-center justify-center space-x-3 text-light-text-secondary dark:text-gray-400">
              <ArrowPathIcon class="w-6 h-6 animate-spin-once" />
              <span>Загрузка транзакций...</span>
            </div>
          </div>

          <div v-else-if="financeStore.error" class="p-4 bg-red-400/10 rounded-xl border border-red-400/30 text-red-400">
            {{ financeStore.error }}
          </div>

          <div v-else-if="financeStore.transactions.length === 0" class="text-center p-6 text-light-text-secondary dark:text-gray-400">
            Нет зарегистрированных операций
          </div>

          <div v-else>
            <!-- Десктоп таблица -->
            <div class="hidden md:block overflow-x-auto">
              <table class="w-full">
                <thead class="bg-light-bg dark:bg-gray-900/30">
                <tr class="border-b border-light-border dark:border-gray-700/30">
                  <th class="px-5 py-3.5 text-left text-sm font-medium text-light-text-secondary dark:text-gray-400">Дата</th>
                  <th class="px-5 py-3.5 text-left text-sm font-medium text-light-text-secondary dark:text-gray-400">Тип операции</th>
                  <th class="px-5 py-3.5 text-left text-sm font-medium text-light-text-secondary dark:text-gray-400">Сумма</th>
                </tr>
                </thead>
                <tbody class="divide-y divide-light-border dark:divide-gray-700/30">
                <tr
                    v-for="transaction in financeStore.transactions"
                    :key="transaction.id"
                    class="hover:bg-light-bg dark:hover:bg-gray-700/10 transition-colors group"
                >
                  <td class="px-5 py-4 text-light-text dark:text-gray-300 text-sm">{{ formatDate(transaction.created_at) }}</td>
                  <td class="px-5 py-4">
                    <div class="flex items-center space-x-2">
                      <component
                          :is="transactionIcon(transaction.transaction_type)"
                          class="w-5 h-5"
                          :class="transactionTypeColor(transaction.transaction_type)"
                      />
                      <span :class="transactionTypeColor(transaction.transaction_type)">
                          {{ transactionTypeText(transaction.transaction_type) }}
                        </span>
                    </div>
                  </td>
                  <td class="px-5 py-4 font-medium" :class="amountColor(transaction.transaction_type)">
                    {{ transaction.amount }} ₽
                  </td>
                </tr>
                </tbody>
              </table>
            </div>

            <!-- Мобильные карточки -->
            <div class="md:hidden space-y-3">
              <div
                  v-for="transaction in financeStore.transactions"
                  :key="transaction.id"
                  class="bg-light-bg dark:bg-gray-900/20 p-4 rounded-xl border border-light-border dark:border-gray-700/30 hover:border-purple-400/30 transition-all group"
              >
                <div class="flex justify-between items-start mb-2">
                  <div class="flex items-center space-x-3">
                    <component
                        :is="transactionIcon(transaction.transaction_type)"
                        class="w-6 h-6"
                        :class="transactionTypeColor(transaction.transaction_type)"
                    />
                    <span :class="transactionTypeColor(transaction.transaction_type)" class="font-medium text-sm">
                      {{ transactionTypeText(transaction.transaction_type) }}
                    </span>
                  </div>
                  <span class="font-bold text-sm" :class="amountColor(transaction.transaction_type)">
                    {{ transaction.amount }} ₽
                  </span>
                </div>
                <div class="text-xs text-light-text-secondary dark:text-gray-400">
                  {{ formatDate(transaction.created_at) }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup lang="ts">
import {type Component, onMounted} from 'vue';
import { useAuthStore } from '../stores/auth';
import { useFinanceStore } from '../stores/finance';
import NavBar from "@/components/NavBar.vue";
import Footer from "@/components/Footer.vue";
import {
  CurrencyDollarIcon,
  ArrowUpCircleIcon,
  ArrowPathIcon,
  ArrowUpIcon,
  ArrowDownIcon,
  CreditCardIcon
} from '@heroicons/vue/24/outline';

const authStore = useAuthStore();
const financeStore = useFinanceStore();

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

function transactionTypeText(type: string): string {
  const typeMap: Record<string, string> = {
    'deposit': 'Пополнение',
    'withdrawal': 'Вывод средств',
    'payment': 'Оплата'
  };
  return typeMap[type] || type;
}

const transactionIcon = (type: string): Component => {
  type TransactionType = 'deposit' | 'withdrawal' | 'payment';
  const icons: Record<TransactionType, Component> = {
    'deposit': ArrowUpIcon,
    'withdrawal': ArrowDownIcon,
    'payment': CreditCardIcon
  } as const;

  return icons[type as TransactionType] || CurrencyDollarIcon;
};

function transactionTypeColor(type: string): string {
  const colors: Record<string, string> = {
    'deposit': 'text-green-400',
    'withdrawal': 'text-red-400',
    'payment': 'text-blue-400'
  };
  return colors[type] || 'text-gray-400';
}

function amountColor(type: string): string {
  return type === 'withdrawal' ? 'text-red-400' : 'text-green-400';
}

onMounted(async () => {
  // Обновляем профиль пользователя для получения актуального баланса
  await authStore.fetchProfile();
  // Загружаем историю транзакций
  await financeStore.fetchTransactions();
});
</script>