<template>
  <div class="min-h-screen bg-light-bg dark:bg-gray-900 flex flex-col">
    <NavBar />

    <main class="flex-1 container mx-auto px-4 py-8 md:py-12">
      <div class="max-w-7xl mx-auto">
        <h1 class="text-3xl md:text-4xl lg:text-5xl font-bold mb-6 md:mb-10 bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent animate-fade-in">
          Управление заведением
        </h1>

        <div v-if="authStore.loading" class="text-center p-8 bg-light-bg-secondary dark:bg-gray-800/50 rounded-2xl border border-light-border dark:border-gray-700/30">
          <div class="animate-pulse flex flex-col items-center space-y-4">
            <div class="h-4 bg-light-bg-tertiary dark:bg-gray-700/50 rounded w-1/4"></div>
            <div class="h-4 bg-light-bg-tertiary dark:bg-gray-700/50 rounded w-1/2"></div>
          </div>
        </div>

        <template v-else>
          <div v-if="authStore.state.profile" class="space-y-6 md:space-y-8">
            <!-- Профиль заведения -->
            <div class="bg-light-bg-secondary dark:bg-gray-800/40 backdrop-blur-lg p-6 md:p-8 rounded-2xl border border-light-border dark:border-gray-700/30 shadow-2xl shadow-black/30">
              <div class="flex flex-col lg:flex-row gap-6 md:gap-8 items-start">
                <!-- Информация -->
                <div class="flex-1 space-y-4 md:space-y-6 w-full">
                  <h2 class="text-xl md:text-2xl font-bold text-light-text dark:text-gray-200 mb-4 bg-gradient-to-r from-purple-400/30 to-blue-400/30 w-max px-4 py-1 rounded-full">
                    Профиль заведения
                  </h2>

                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="p-4 bg-light-bg-tertiary dark:bg-gray-900/20 rounded-xl border border-light-border dark:border-gray-700/30 hover:border-purple-400/30 transition-all group">
                      <div class="flex items-center">
                        <BuildingLibraryIcon class="w-7 h-7 text-purple-400 mr-4 group-hover:rotate-12 transition-transform" />
                        <div>
                          <p class="text-xs md:text-sm text-light-text-secondary dark:text-gray-400">Название</p>
                          <p class="text-lg md:text-xl font-medium text-light-text dark:text-gray-100">{{ authStore.state.profile.name }}</p>
                        </div>
                      </div>
                    </div>

                    <div class="p-4 bg-light-bg-tertiary dark:bg-gray-900/20 rounded-xl border border-light-border dark:border-gray-700/30 hover:border-blue-400/30 transition-all group">
                      <div class="flex items-center">
                        <MapPinIcon class="w-7 h-7 text-blue-400 mr-4 group-hover:rotate-12 transition-transform" />
                        <div>
                          <p class="text-xs md:text-sm text-light-text-secondary dark:text-gray-400">Город</p>
                          <p class="text-lg md:text-xl font-medium text-light-text dark:text-gray-100">{{ authStore.state.profile.city }}</p>
                        </div>
                      </div>
                    </div>

                    <div class="p-4 bg-light-bg-tertiary dark:bg-gray-900/20 rounded-xl border border-light-border dark:border-gray-700/30 hover:border-green-400/30 transition-all group">
                      <div class="flex items-center">
                        <DevicePhoneMobileIcon class="w-7 h-7 text-green-400 mr-4 group-hover:rotate-12 transition-transform" />
                        <div>
                          <p class="text-xs md:text-sm text-light-text-secondary dark:text-gray-400">Телефон</p>
                          <p class="text-lg md:text-xl font-medium text-light-text dark:text-gray-100">{{ authStore.state.profile.phone }}</p>
                        </div>
                      </div>
                    </div>

                    <div class="p-4 bg-light-bg-tertiary dark:bg-gray-900/20 rounded-xl border border-light-border dark:border-gray-700/30 hover:border-amber-400/30 transition-all group">
                      <div class="flex items-center">
                        <CurrencyDollarIcon class="w-7 h-7 text-amber-400 mr-4 group-hover:rotate-12 transition-transform" />
                        <div>
                          <p class="text-xs md:text-sm text-light-text-secondary dark:text-gray-400">Баланс</p>
                          <p class="text-2xl md:text-3xl font-bold text-green-400">{{ authStore.state.profile.balance }} ₽</p>
                        </div>
                      </div>
                    </div>

                    <div class="md:col-span-2 col-span-1">
                      <div
                          class="p-4 rounded-xl transition-all group cursor-pointer
                           bg-gradient-to-r from-purple-400/80 to-blue-400/80
                           hover:from-purple-400 hover:to-blue-400
                           shadow-lg shadow-purple-500/20
                           hover:shadow-purple-500/40
                           relative overflow-hidden
                           border-2 border-purple-400/30
                           hover:border-purple-400/50"
                          @click="downloadQrCode"
                      >
                        <!-- Блестящий эффект при наведении -->
                        <div class="absolute inset-0 opacity-0 group-hover:opacity-30 transition-opacity
                              bg-gradient-to-r from-white/30 via-transparent to-transparent"></div>

                        <div class="flex items-center justify-center space-x-3 relative">
                          <ArrowDownTrayIcon class="w-7 h-7 text-gray-100"/>

                          <div class="text-center">
                            <p class="text-lg md:text-xl font-semibold text-gray-100 drop-shadow-sm">
                              Скачать QR-код
                            </p>
                            <p class="text-xs md:text-sm text-gray-200/90 mt-1">
                              PNG 370x370px
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- QR-код -->
                <div class="lg:w-[400px] w-full space-y-6 lg:border-l lg:border-light-border dark:lg:border-gray-700/30 lg:pl-8">
                  <div class="text-center">
                    <h3 class="text-lg md:text-xl font-semibold text-light-text dark:text-gray-200 mb-4">QR-код для заказа</h3>
                    <div class="p-4 bg-light-bg-tertiary dark:bg-gray-900/30 rounded-2xl border-2 border-purple-400/20 hover:border-purple-400/40 transition-all inline-block shadow-lg shadow-purple-500/10">
                      <img
                          v-if="authStore.state.profile.qr_code"
                          :src="authStore.state.profile.qr_code"
                          alt="QR-код"
                          class="w-48 h-48 md:w-64 md:h-64 object-contain mx-auto"
                      />
                    </div>
                    <p class="text-xs md:text-sm text-light-text-secondary dark:text-gray-400 mt-3 md:mt-4">Отсканируйте код для перехода к заказу</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Статистика и действия -->
            <div class="grid md:grid-cols-2 gap-4 md:gap-6">
              <!-- Статистика -->
              <div class="bg-light-bg-secondary dark:bg-gray-800/40 backdrop-blur-lg p-6 rounded-2xl border border-light-border dark:border-gray-700/30 shadow-xl">
                <h2 class="text-lg md:text-xl font-semibold text-light-text dark:text-gray-200 mb-4">Статистика</h2>
                <div class="space-y-4">
                  <div class="flex justify-between items-center p-3 bg-light-bg-tertiary dark:bg-gray-900/20 rounded-xl border border-purple-400/20 hover:border-purple-400/40 transition-all">
                    <span class="text-light-text-secondary dark:text-gray-400">Всего треков</span>
                    <span class="text-xl md:text-2xl font-bold text-purple-400">{{ tracks.length }}</span>
                  </div>
                  <div class="flex justify-between items-center p-3 bg-light-bg-tertiary dark:bg-gray-900/20 rounded-xl border border-blue-400/20 hover:border-blue-400/40 transition-all">
                    <span class="text-light-text-secondary dark:text-gray-400">Активные запросы</span>
                    <span class="text-xl md:text-2xl font-bold text-blue-400">{{ pendingRequests.length }}</span>
                  </div>
                </div>
              </div>

              <!-- Быстрые действия -->
              <div class="bg-light-bg-secondary dark:bg-gray-800/40 backdrop-blur-lg p-6 rounded-2xl border border-light-border dark:border-gray-700/30 shadow-xl">
                <h2 class="text-lg md:text-xl font-semibold text-light-text dark:text-gray-200 mb-4">Действия</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 md:gap-4">
                  <router-link
                      to="/tracks/add"
                      class="p-4 bg-light-bg-tertiary dark:bg-gray-900/20 hover:bg-gradient-to-br from-purple-400/10 to-blue-400/10 rounded-xl border border-light-border dark:border-gray-700/30 hover:border-purple-400/30 transition-all flex items-center group"
                  >
                    <PlusCircleIcon class="w-6 h-6 md:w-7 md:h-7 text-purple-400 mr-3 group-hover:rotate-90 transition-transform" />
                    <span class="text-light-text dark:text-gray-300 group-hover:text-purple-400 text-sm md:text-base">Добавить трек</span>
                  </router-link>

                  <router-link
                      to="/tracks"
                      class="p-4 bg-light-bg-tertiary dark:bg-gray-900/20 hover:bg-gradient-to-br from-blue-400/10 to-cyan-400/10 rounded-xl border border-light-border dark:border-gray-700/30 hover:border-blue-400/30 transition-all flex items-center group"
                  >
                    <MusicalNoteIcon class="w-6 h-6 md:w-7 md:h-7 text-blue-400 mr-3 group-hover:rotate-12 transition-transform" />
                    <span class="text-light-text dark:text-gray-300 group-hover:text-blue-400 text-sm md:text-base">Управление треками</span>
                  </router-link>

                  <router-link
                      to="/requests"
                      class="p-4 bg-light-bg-tertiary dark:bg-gray-900/20 hover:bg-gradient-to-br from-green-400/10 to-emerald-400/10 rounded-xl border border-light-border dark:border-gray-700/30 hover:border-green-400/30 transition-all flex items-center group"
                  >
                    <InboxIcon class="w-6 h-6 md:w-7 md:h-7 text-green-400 mr-3 group-hover:-rotate-12 transition-transform" />
                    <span class="text-light-text dark:text-gray-300 group-hover:text-green-400 text-sm md:text-base">Запросы треков</span>
                  </router-link>

                  <router-link
                      to="/withdrawals"
                      class="p-4 bg-light-bg-tertiary dark:bg-gray-900/20 hover:bg-gradient-to-br from-amber-400/10 to-orange-400/10 rounded-xl border border-light-border dark:border-gray-700/30 hover:border-amber-400/30 transition-all flex items-center group"
                  >
                    <BanknotesIcon class="w-6 h-6 md:w-7 md:h-7 text-amber-400 mr-3 group-hover:rotate-12 transition-transform" />
                    <span class="text-light-text dark:text-gray-300 group-hover:text-amber-400 text-sm md:text-base">Вывод средств</span>
                  </router-link>
                </div>
              </div>
            </div>
          </div>

          <!-- Ошибка -->
          <div v-else class="text-center p-8 bg-light-bg-secondary dark:bg-gray-800/50 rounded-2xl border border-red-400/30 shadow-xl">
            <div class="max-w-md mx-auto space-y-4">
              <p class="text-light-text dark:text-gray-300 mb-3">Ошибка загрузки профиля</p>
              <button
                  @click="authStore.fetchProfile"
                  class="px-6 py-2.5 bg-red-400/10 hover:bg-red-400/20 text-red-400 rounded-xl transition-all border border-red-400/30 hover:border-red-400/50 flex items-center justify-center mx-auto gap-2"
              >
                <ArrowPathIcon class="w-5 h-5 animate-spin-once" />
                Попробовать снова
              </button>
            </div>
          </div>
        </template>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useTracksStore } from '../stores/tracks';
import { useRequestsStore } from '../stores/requests';
import NavBar from "@/components/NavBar.vue";
import Footer from "@/components/Footer.vue";
import {
  BuildingLibraryIcon,
  MapPinIcon,
  DevicePhoneMobileIcon,
  CurrencyDollarIcon,
  PlusCircleIcon,
  MusicalNoteIcon,
  InboxIcon,
  BanknotesIcon,
  ArrowPathIcon,
  ArrowDownTrayIcon
} from '@heroicons/vue/24/outline';

const authStore = useAuthStore();
const tracksStore = useTracksStore();
const requestsStore = useRequestsStore();

const tracks = computed(() => tracksStore.tracks);
const pendingRequests = computed(() =>
    requestsStore.requests.filter(req => req.status === 'pending')
);

const downloadQrCode = () => {
  if (!authStore.state.profile?.qr_code) {
    console.error('QR code URL is not available');
    return;
  }

  try {
    const link = document.createElement('a');
    link.href = authStore.state.profile.qr_code;
    link.download = `qr-code-${authStore.state.profile.name || 'venue'}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (error) {
    console.error('Error downloading QR code:', error);
  }
};

onMounted(async () => {
  await authStore.init();
  if (authStore.state.profile) {
    await tracksStore.fetchTracks(authStore.state.profile.id);
    await requestsStore.fetchRequests();
  }
});
</script>