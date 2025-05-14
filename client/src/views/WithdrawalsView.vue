<template>
  <div class="min-h-screen bg-gray-900 flex flex-col">
    <NavBar />

    <main class="flex-1 container mx-auto px-4 py-8 md:py-12">
      <div class="max-w-4xl mx-auto">
        <h1 class="text-3xl md:text-4xl font-bold mb-6 md:mb-10 bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent animate-fade-in">
          Вывод средств
        </h1>

        <!-- Блок баланса -->
        <div v-if="authStore.state.profile" class="bg-gray-800/40 backdrop-blur-lg p-6 md:p-8 rounded-2xl border border-gray-700/30 shadow-xl mb-8">
          <div class="flex items-center gap-4 md:gap-6">
            <div class="p-3 bg-gradient-to-br from-green-400/10 to-emerald-400/10 rounded-xl border border-green-400/20">
              <CurrencyDollarIcon class="w-7 h-7 text-green-400" />
            </div>
            <div>
              <p class="text-sm md:text-base text-gray-400">Доступно к выводу</p>
              <p class="text-2xl md:text-3xl font-bold text-green-400">
                {{ authStore.state.profile.balance }} ₽
              </p>
            </div>
          </div>
        </div>

        <!-- Форма вывода -->
        <div class="bg-gray-800/40 backdrop-blur-lg p-6 md:p-8 rounded-2xl border border-gray-700/30 shadow-xl mb-8">
          <h2 class="text-xl md:text-2xl font-bold text-gray-200 mb-6 bg-gradient-to-r from-blue-400/30 to-cyan-400/30 w-max px-4 py-1 rounded-full">
            Новый вывод
          </h2>

          <div v-if="financeStore.error" class="mb-6 p-4 bg-red-400/10 rounded-xl border border-red-400/30 text-red-400">
            {{ financeStore.error }}
          </div>

          <form @submit.prevent="handleWithdrawal" class="space-y-6">
            <div>
              <label class="block text-gray-400 mb-2">Сумма вывода</label>
              <input
                  type="number"
                  v-model.number="formData.amount"
                  min="1"
                  :max="authStore.state.profile?.balance || 0"
                  required
                  class="w-full p-3.5 bg-gray-900/20 border text-white border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all placeholder-gray-500"
                  placeholder="Введите сумму в рублях"
              />
            </div>

            <div class="grid md:grid-cols-2 gap-6">
              <div>
                <label class="block text-gray-400 mb-2">Номер карты</label>
                <input
                    type="text"
                    v-model="formData.card_number"
                    pattern="[0-9]{16}"
                    maxlength="16"
                    required
                    class="w-full p-3.5 bg-gray-900/20 border text-white border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all placeholder-gray-500"
                    placeholder="1234 5678 9012 3456"
                />
              </div>

              <div class="grid grid-cols-3 gap-4">
                <div>
                  <label class="block text-gray-400 mb-2">Месяц</label>
                  <input
                      type="text"
                      v-model="formData.card_expiry_month"
                      pattern="[0-9]{2}"
                      maxlength="2"
                      required
                      class="w-full p-3.5 bg-gray-900/20 border text-white border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all placeholder-gray-500"
                      placeholder="MM"
                  />
                </div>

                <div>
                  <label class="block text-gray-400 mb-2">Год</label>
                  <input
                      type="text"
                      v-model="formData.card_expiry_year"
                      pattern="[0-9]{4}"
                      maxlength="4"
                      required
                      class="w-full p-3.5 bg-gray-900/20 border text-white border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all placeholder-gray-500"
                      placeholder="YYYY"
                  />
                </div>

                <div>
                  <label class="block text-gray-400 mb-2">CVC</label>
                  <input
                      type="text"
                      v-model="formData.card_csc"
                      pattern="[0-9]{3}"
                      maxlength="3"
                      required
                      class="w-full p-3.5 bg-gray-900/20 border text-white border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all placeholder-gray-500"
                      placeholder="123"
                  />
                </div>
              </div>
            </div>

            <button
                type="submit"
                :disabled="financeStore.loading || !canWithdraw"
                class="w-full py-3.5 bg-gradient-to-r from-purple-600 to-blue-500 border border-purple-400/20 rounded-xl font-semibold text-white hover:from-purple-700 hover:to-blue-600 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed group"
            >
              <span v-if="financeStore.loading" class="flex items-center justify-center">
                <ArrowPathIcon class="w-5 h-5 mr-2 animate-spin" />
                Обработка...
              </span>
              <span v-else class="group-hover:translate-x-1 transition-transform">Вывести средства</span>
            </button>
          </form>
        </div>

        <!-- История выводов -->
        <div class="bg-gray-800/40 backdrop-blur-lg p-6 md:p-8 rounded-2xl border border-gray-700/30 shadow-xl">
          <h2 class="text-xl md:text-2xl font-bold text-gray-200 mb-6 bg-gradient-to-r from-cyan-400/30 to-purple-400/30 w-max px-4 py-1 rounded-full">
            История операций
          </h2>

          <div v-if="financeStore.loading && financeStore.withdrawals.length === 0" class="text-center p-6">
            <div class="inline-flex items-center gap-3 text-gray-400">
              <ArrowPathIcon class="w-6 h-6 animate-spin-once" />
              <span>Загрузка истории...</span>
            </div>
          </div>

          <div v-else-if="financeStore.withdrawals.length === 0" class="text-center p-6 text-gray-400">
            Нет операций по выводу средств
          </div>

          <div v-else class="space-y-3">
            <div
                v-for="withdrawal in financeStore.withdrawals"
                :key="withdrawal.id"
                class="bg-gray-900/20 p-4 rounded-xl border border-gray-700/30 hover:border-purple-400/30 transition-all group"
            >
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-center">
                <div class="space-y-1">
                  <p class="text-xs text-gray-400">Дата</p>
                  <p class="text-sm text-gray-300">{{ formatDate(withdrawal.created_at) }}</p>
                </div>

                <div class="space-y-1">
                  <p class="text-xs text-gray-400">Сумма</p>
                  <p class="text-base font-bold text-gray-100">{{ withdrawal.amount }} ₽</p>
                </div>

                <div class="space-y-1">
                  <p class="text-xs mb-2 text-gray-400">Статус</p>
                  <span :class="statusColor(withdrawal.status)" class="px-3 py-1.5 rounded-full text-sm font-medium">
                    {{ getWithdrawalStatusText(withdrawal.status) }}
                  </span>
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
import { reactive, computed, onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useFinanceStore } from '../stores/finance';
import { useRouter } from 'vue-router';
import NavBar from "@/components/NavBar.vue";
import Footer from "@/components/Footer.vue";
import { CurrencyDollarIcon, ArrowPathIcon } from '@heroicons/vue/24/outline';

const authStore = useAuthStore();
const financeStore = useFinanceStore();
const router = useRouter();

const formData = reactive({
  amount: 0,
  card_number: '',
  card_expiry_month: '',
  card_expiry_year: '',
  card_csc: ''
});

const canWithdraw = computed(() => {
  if (!authStore.state.profile) return false;
  return formData.amount > 0 && formData.amount <= authStore.state.profile.balance;
});

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

function getWithdrawalStatusText(status: string): string {
  const statusMap: Record<string, string> = {
    'pending': 'Ожидает',
    'processing': 'В обработке',
    'succeeded': 'Успешно',
    'canceled': 'Отменен',
    'failed': 'Ошибка'
  };
  return statusMap[status] || status;
}

function statusColor(status: string): string {
  const colors: Record<string, string> = {
    'pending': 'bg-amber-400/10 text-amber-400 border-amber-400/20',
    'processing': 'bg-blue-400/10 text-blue-400 border-blue-400/20',
    'succeeded': 'bg-green-400/10 text-green-400 border-green-400/20',
    'canceled': 'bg-gray-400/10 text-gray-400 border-gray-400/20',
    'failed': 'bg-red-400/10 text-red-400 border-red-400/20'
  };
  return colors[status] || 'bg-gray-400/10 text-gray-400';
}

async function handleWithdrawal() {
  if (!canWithdraw.value) return;

  const result = await financeStore.createWithdrawal(formData);

  if (result) {
    formData.amount = 0;
    formData.card_number = '';
    formData.card_expiry_month = '';
    formData.card_expiry_year = '';
    formData.card_csc = '';

    await authStore.fetchProfile();
    await router.push('/withdrawals');
  }
}

onMounted(() => {
  authStore.fetchProfile();
  financeStore.fetchWithdrawals();
});
</script>
