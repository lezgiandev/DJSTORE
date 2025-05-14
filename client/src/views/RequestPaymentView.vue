<template>
  <div class="min-h-screen bg-gray-900 flex flex-col">
    <main class="flex-1 container mx-auto px-4 py-8 md:py-12">
      <div class="max-w-4xl mx-auto">
        <h1 class="text-3xl md:text-4xl font-bold mb-6 md:mb-10 bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent animate-fade-in">
          Оплата запроса
        </h1>

        <div v-if="loading" class="text-center p-8 bg-gray-800/40 rounded-2xl border border-gray-700/30">
          <div class="inline-flex items-center gap-3 text-gray-400">
            <ArrowPathIcon class="w-6 h-6 animate-spin-once" />
            <span>Загрузка информации...</span>
          </div>
        </div>

        <div v-else-if="error" class="mb-6 p-4 bg-red-400/10 rounded-xl border border-red-400/30 text-red-400">
          {{ error }}
        </div>

        <div v-else-if="!requestData" class="p-8 bg-gray-800/40 rounded-2xl border border-gray-700/30 text-gray-400 text-center">
          Платежная информация не найдена
        </div>

        <div v-else class="space-y-8">
          <!-- Информация о треке -->
          <div class="bg-gray-800/40 backdrop-blur-lg p-6 md:p-8 rounded-2xl border border-gray-700/30 shadow-xl">
            <h2 class="text-xl md:text-2xl font-bold text-gray-200 mb-6 bg-gradient-to-r from-purple-400/30 to-blue-400/30 w-max px-4 py-1 rounded-full">
              Информация о треке
            </h2>
            <div class="grid md:grid-cols-2 gap-4">
              <div class="flex items-center gap-3 p-3 bg-gray-900/20 rounded-xl">
                <div class="p-2 bg-purple-400/10 rounded-lg border border-purple-400/20">
                  <MusicalNoteIcon class="w-6 h-6 text-purple-400" />
                </div>
                <div>
                  <p class="text-sm text-gray-400">Название</p>
                  <p class="font-medium text-gray-100">{{ requestData.track.title }}</p>
                </div>
              </div>
              <div class="flex items-center gap-3 p-3 bg-gray-900/20 rounded-xl">
                <div class="p-2 bg-purple-400/10 rounded-lg border border-purple-400/20">
                  <UserIcon class="w-6 h-6 text-purple-400" />
                </div>
                <div>
                  <p class="text-sm text-gray-400">Исполнитель</p>
                  <p class="font-medium text-gray-100">{{ requestData.track.artist }}</p>
                </div>
              </div>
              <div class="flex items-center gap-3 p-3 bg-gray-900/20 rounded-xl">
                <div class="p-2 bg-purple-400/10 rounded-lg border border-purple-400/20">
                  <TagIcon class="w-6 h-6 text-purple-400" />
                </div>
                <div>
                  <p class="text-sm text-gray-400">Жанр</p>
                  <p class="font-medium text-gray-100">{{ requestData.track.genre.name }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Информация о платеже -->
          <div class="bg-gray-800/40 backdrop-blur-lg p-6 md:p-8 rounded-2xl border border-gray-700/30 shadow-xl">
            <h2 class="text-xl md:text-2xl font-bold text-gray-200 mb-6 bg-gradient-to-r from-blue-400/30 to-cyan-400/30 w-max px-4 py-1 rounded-full">
              Детали платежа
            </h2>
            <div class="grid md:grid-cols-2 gap-4">
              <div class="flex items-center gap-3 p-3 bg-gray-900/20 rounded-xl">
                <div class="p-2 bg-green-400/10 rounded-lg border border-green-400/20">
                  <CurrencyDollarIcon class="w-6 h-6 text-green-400" />
                </div>
                <div>
                  <p class="text-sm text-gray-400">Сумма</p>
                  <p class="text-2xl font-bold text-green-400">{{ requestData.user_fee }} ₽</p>
                </div>
              </div>
              <div class="flex items-center gap-3 p-3 bg-gray-900/20 rounded-xl">
                <div class="p-2 bg-amber-400/10 rounded-lg border border-amber-400/20">
                  <ClockIcon class="w-6 h-6 text-amber-400" />
                </div>
                <div>
                  <p class="text-sm text-gray-400">Статус</p>
                  <span :class="requestData.is_paid ? 'text-green-400' : 'text-amber-400'" class="font-medium">
                    {{ requestData.is_paid ? 'Оплачен' : 'Ожидает оплаты' }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Форма оплаты -->
          <div v-if="!requestData.is_paid" class="bg-gray-800/40 backdrop-blur-lg p-6 md:p-8 rounded-2xl border border-gray-700/30 shadow-xl">
            <h2 class="text-xl md:text-2xl font-bold text-gray-200 mb-6 bg-gradient-to-r from-cyan-400/30 to-purple-400/30 w-max px-4 py-1 rounded-full">
              Оплата картой
            </h2>
            <form @submit.prevent="handlePayment" class="space-y-6">
              <div class="space-y-4">
                <div>
                  <label class="block text-gray-400 mb-2">Номер карты</label>
                  <input
                      type="text"
                      v-model="paymentForm.cardNumber"
                      pattern="[0-9]{16}"
                      maxlength="16"
                      required
                      class="w-full p-3.5 bg-gray-900/20 border text-white border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all placeholder-gray-500"
                      placeholder="1234 5678 9012 3456"
                  />
                </div>

                <div class="grid md:grid-cols-2 gap-4">
                  <div class="grid grid-cols-2 gap-3">
                    <div>
                      <label class="block text-gray-400 mb-2">Месяц</label>
                      <input
                          type="text"
                          v-model="paymentForm.cardMonth"
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
                          v-model="paymentForm.cardYear"
                          pattern="[0-9]{4}"
                          maxlength="4"
                          required
                          class="w-full p-3.5 bg-gray-900/20 border text-white border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all placeholder-gray-500"
                          placeholder="YYYY"
                      />
                    </div>
                  </div>

                  <div>
                    <label class="block text-gray-400 mb-2">CVC/CVV</label>
                    <input
                        type="text"
                        v-model="paymentForm.cardCvc"
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
                  :disabled="paymentLoading"
                  class="w-full py-3.5 bg-gradient-to-r from-purple-600 to-blue-500 border border-purple-400/20 rounded-xl font-semibold text-white hover:from-purple-700 hover:to-blue-600 transition-all duration-300 disabled:opacity-50 group"
              >
                <span v-if="paymentLoading" class="flex items-center justify-center">
                  <ArrowPathIcon class="w-5 h-5 mr-2 animate-spin" />
                  Обработка...
                </span>
                <span v-else class="group-hover:translate-x-1 transition-transform">
                  Оплатить {{ requestData.user_fee }} ₽
                </span>
              </button>
            </form>
          </div>
        </div>
      </div>
    </main>

    <!-- Модальное окно успеха -->
    <transition name="fade">
      <div
          v-if="showSuccessModal"
          class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
      >
        <div class="bg-gray-800/95 backdrop-blur-lg p-8 rounded-2xl border border-gray-700/30 shadow-2xl max-w-md w-full text-center">
          <CheckCircleIcon class="w-12 h-12 text-green-400 mx-auto mb-4 animate-pulse" />
          <h3 class="text-xl font-bold text-gray-200 mb-2">Оплата успешна!</h3>
          <p class="text-gray-400 mb-6">Ваш запрос будет рассмотрен диджеем</p>
          <button
              @click="closeSuccessModal"
              class="px-6 py-2.5 bg-purple-400/10 hover:bg-purple-400/20 border border-purple-400/30 text-purple-400 rounded-xl transition-all"
          >
            Закрыть
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import type { TrackRequest } from '@/types';
import {
  ArrowPathIcon,
  MusicalNoteIcon,
  UserIcon,
  TagIcon,
  CurrencyDollarIcon,
  ClockIcon,
  CheckCircleIcon
} from '@heroicons/vue/24/outline';

const route = useRoute();
const paymentToken = computed(() => route.params.token as string);
const requestData = ref<TrackRequest | null>(null);
const loading = ref(false);
const error = ref<string | null>(null);

const paymentForm = reactive({
  cardNumber: '',
  cardMonth: '',
  cardYear: '',
  cardCvc: ''
});

const paymentLoading = ref(false);
const showSuccessModal = ref(false);

async function fetchPaymentInfo() {
  try {
    loading.value = true;
    error.value = null;
    const response = await axios.get(`http://127.0.0.1:8000/api/requests/pay/${paymentToken.value}/`);
    requestData.value = response.data;
  } catch (err: any) {
    console.error('Error fetching payment info:', err);
    error.value = err.response?.data?.detail || 'Ошибка при загрузке информации';
  } finally {
    loading.value = false;
  }
}

async function handlePayment() {
  try {
    paymentLoading.value = true;
    error.value = null;

    await axios.post(`http://127.0.0.1:8000/api/requests/pay/${paymentToken.value}/`, {
      amount: requestData.value?.user_fee
    });

    if (requestData.value) {
      requestData.value.is_paid = true;
    }

    showSuccessModal.value = true;
  } catch (err: any) {
    console.error('Payment error:', err);
    error.value = err.response?.data?.detail || 'Ошибка при обработке платежа';
  } finally {
    paymentLoading.value = false;
  }
}

function closeSuccessModal() {
  showSuccessModal.value = false;
}

onMounted(() => {
  fetchPaymentInfo();
});
</script>
