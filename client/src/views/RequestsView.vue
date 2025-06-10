<template>
  <div class="min-h-screen bg-light-bg dark:bg-gray-900 flex flex-col">
    <NavBar />

    <main class="flex-1 container mx-auto px-4 py-8">
      <div class="max-w-5xl mx-auto">
        <h1 class="text-3xl md:text-4xl font-bold mb-6 md:mb-8 bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent animate-fade-in">
          Управление запросами
        </h1>

        <!-- Вкладки -->
        <div class="flex mb-6 bg-light-bg-secondary dark:bg-gray-800/40 backdrop-blur-lg rounded-xl border border-light-border dark:border-gray-700/30 overflow-hidden shadow-xl">
          <button
              @click="activeTab = 'incoming'"
              :class="[
              'px-6 py-4 text-sm font-medium flex-1 transition-all flex items-center justify-center gap-2',
              activeTab === 'incoming'
                ? 'bg-gradient-to-r from-purple-500/20 to-blue-500/20 text-light-text dark:text-white border-r border-light-border dark:border-gray-700/30'
                : 'text-light-text-secondary dark:text-gray-400 hover:text-light-text dark:hover:text-gray-300 hover:bg-light-bg dark:hover:bg-gray-800/50'
            ]"
          >
            <InboxIcon class="w-5 h-5" />
            Входящие
          </button>
          <button
              @click="activeTab = 'processed'"
              :class="[
              'px-6 py-4 text-sm font-medium flex-1 transition-all flex items-center justify-center gap-2',
              activeTab === 'processed'
                ? 'bg-gradient-to-r from-blue-500/20 to-cyan-500/20 text-light-text dark:text-white border-l border-light-border dark:border-gray-700/30'
                : 'text-light-text-secondary dark:text-gray-400 hover:text-light-text dark:hover:text-gray-300 hover:bg-light-bg dark:hover:bg-gray-800/50'
            ]"
          >
            <CheckBadgeIcon class="w-5 h-5" />
            Обработанные
          </button>
        </div>

        <!-- Контент -->
        <div class="bg-light-bg-secondary dark:bg-gray-800/40 backdrop-blur-lg rounded-2xl border border-light-border dark:border-gray-700/30 shadow-xl">
          <div v-if="requestsStore.loading" class="p-8 text-center">
            <div class="inline-flex items-center gap-3 text-light-text-secondary dark:text-gray-400">
              <ArrowPathIcon class="w-6 h-6 animate-spin-once" />
              <span>Загрузка запросов...</span>
            </div>
          </div>

          <div v-else-if="requestsStore.error" class="p-4 bg-red-400/10 rounded-xl border border-red-400/30 text-red-400 mx-4 my-6">
            {{ requestsStore.error }}
          </div>

          <div v-else-if="filteredRequests.length === 0" class="p-8 text-center text-light-text-secondary dark:text-gray-400">
            <span v-if="activeTab === 'incoming'">Нет новых запросов</span>
            <span v-else>Нет обработанных запросов</span>
          </div>

          <div v-else class="p-4 space-y-4">
            <div
                v-for="request in filteredRequests"
                :key="request.id"
                class="group bg-light-bg dark:bg-gray-900/20 p-4 rounded-xl border border-light-border dark:border-gray-700/30 hover:border-purple-400/30 transition-all shadow-lg hover:shadow-purple-500/10"
            >
              <div class="flex flex-col md:flex-row gap-4 md:gap-6">
                <!-- Обложка трека -->
                <div class="flex-shrink-0 relative w-full sm:w-32 h-32">
                  <div class="w-full h-full rounded-xl overflow-hidden border border-light-border dark:border-gray-700/30 transform group-hover:scale-[1.02] transition-transform">
                    <img
                        :src="request.track.icon"
                        :alt="request.track.title"
                        class="w-full h-full object-cover"
                    />
                    <div class="absolute inset-0 bg-gradient-to-t from-gray-900/60 to-transparent rounded-xl"></div>
                    <MusicalNoteIcon class="absolute bottom-3 right-3 w-5 h-5 text-purple-400" />
                  </div>
                </div>

                <!-- Информация о треке -->
                <div class="flex-1 min-w-0">
                  <div class="flex flex-col md:flex-row md:items-center justify-between gap-2 mb-3">
                    <h3 class="text-lg md:text-xl font-semibold text-light-text dark:text-gray-100 truncate">
                      {{ request.track.title }}
                    </h3>
                    <span class="text-xs md:text-sm text-purple-400 whitespace-nowrap">
                      {{ formatDate(request.created_at) }}
                    </span>
                  </div>

                  <p class="text-light-text-secondary dark:text-gray-400 text-sm md:text-base mb-3">{{ request.track.artist }}</p>

                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <!-- Левая колонка -->
                    <div class="space-y-3">
                      <!-- Статус и оплата -->
                      <div class="flex flex-wrap gap-3">
                        <div class="flex items-center gap-2">
                          <span class="text-light-text-secondary dark:text-gray-400 text-sm">Статус:</span>
                          <span :class="statusBadgeStyle(request.status)" class="px-3 py-1 rounded-full text-xs md:text-sm font-medium border">
                            {{ getStatusText(request.status) }}
                          </span>
                        </div>
                        <div class="flex items-center gap-2">
                          <span class="text-light-text-secondary dark:text-gray-400 text-sm">Оплата:</span>
                          <span :class="request.is_paid ? 'text-green-400' : 'text-amber-400'" class="text-xs md:text-sm">
                            {{ request.is_paid ? 'Оплачен' : 'Ожидает оплаты' }}
                          </span>
                        </div>
                      </div>

                      <!-- Цены -->
                      <div class="grid grid-cols-2 gap-3">
                        <div class="p-3 bg-light-bg dark:bg-gray-800/50 rounded-lg">
                          <p class="text-xs text-light-text-secondary dark:text-gray-400 mb-1">Предложенная цена</p>
                          <p class="text-base font-bold text-green-400">{{ request.user_fee }} ₽</p>
                        </div>
                        <div class="p-3 bg-light-bg dark:bg-gray-800/50 rounded-lg">
                          <p class="text-xs text-light-text-secondary dark:text-gray-400 mb-1">Минимальная цена</p>
                          <p class="text-base font-bold text-blue-400">{{ request.min_fee }} ₽</p>
                        </div>
                      </div>
                    </div>

                    <!-- Правая колонка -->
                    <div class="flex items-end justify-end md:justify-end">
                      <!-- Действия -->
                      <div class="flex flex-wrap gap-2">
                        <button
                            v-if="request.status === 'pending' && request.is_paid"
                            @click="acceptRequest(request.id)"
                            :disabled="requestsStore.loading"
                            class="flex items-center gap-2 px-4 py-2 bg-green-400/10 hover:bg-green-400/20 border border-green-400/30 rounded-xl transition-all disabled:opacity-50 group/accept"
                        >
                          <CheckIcon class="w-5 h-5 text-green-400 group-hover/accept:rotate-12 transition-transform" />
                          <span class="text-sm text-green-400">Принять</span>
                        </button>

                        <button
                            v-if="request.status === 'pending'"
                            @click="rejectRequest(request.id)"
                            :disabled="requestsStore.loading"
                            class="flex items-center gap-2 px-4 py-2 bg-red-400/10 hover:bg-red-400/20 border border-red-400/30 rounded-xl transition-all disabled:opacity-50 group/reject"
                        >
                          <XMarkIcon class="w-5 h-5 text-red-400 group-hover/reject:rotate-12 transition-transform" />
                          <span class="text-sm text-red-400">Отклонить</span>
                        </button>
                      </div>
                    </div>
                  </div>
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
import { onMounted, ref, computed } from 'vue';
import { useRequestsStore } from '../stores/requests';
import NavBar from "@/components/NavBar.vue";
import Footer from "@/components/Footer.vue";
import {
  ArrowPathIcon,
  MusicalNoteIcon,
  CheckIcon,
  XMarkIcon,
  InboxIcon,
  CheckBadgeIcon
} from '@heroicons/vue/24/outline';

const requestsStore = useRequestsStore();
const activeTab = ref('incoming');

const filteredRequests = computed(() => {
  return activeTab.value === 'incoming'
      ? requestsStore.requests.filter(request => request.status === 'pending')
      : requestsStore.requests.filter(request => request.status !== 'pending');
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

function getStatusText(status: string): string {
  const statusMap: Record<string, string> = {
    'pending': 'Ожидает',
    'accepted': 'Принят',
    'rejected': 'Отклонен'
  };
  return statusMap[status] || status;
}

function statusBadgeStyle(status: string): string {
  const styles: Record<string, string> = {
    'pending': 'bg-amber-400/10 text-amber-400 border-amber-400/20',
    'accepted': 'bg-green-400/10 text-green-400 border-green-400/20',
    'rejected': 'bg-red-400/10 text-red-400 border-red-400/20'
  };
  return styles[status] || 'bg-gray-400/10 text-gray-400 border-gray-400/20';
}

async function acceptRequest(requestId: number) {
  await requestsStore.updateRequestStatus(requestId, 'accepted');
}

async function rejectRequest(requestId: number) {
  await requestsStore.updateRequestStatus(requestId, 'rejected');
}

onMounted(() => {
  requestsStore.fetchRequests();
});
</script>
