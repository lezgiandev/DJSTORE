<template>
  <div class="min-h-screen bg-light-bg dark:bg-gray-900 flex flex-col">
    <NavBar />

    <main class="flex-1">
      <!-- Hero Section -->
      <section class="relative py-20 bg-gradient-to-b from-light-bg-secondary to-light-bg dark:from-gray-800 dark:to-gray-900">
        <div class="container mx-auto px-4 text-center">
          <div class="max-w-4xl mx-auto">
            <h1 class="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent animate-fade-in">
              DJ STORE
            </h1>
            <p class="text-xl md:text-2xl text-light-text-secondary dark:text-gray-400 mb-12 mx-auto">
              Управляй музыкальной атмосферой своего заведения. Принимай запросы, создавай плейлисты и взаимодействуй с публикой через уникальные QR-коды!
            </p>

            <!-- Auth Section -->
            <div class="space-y-6">
              <div v-if="authStore.state.isAuthenticated" class="animate-slide-up">
                <div class="bg-light-bg-secondary dark:bg-gray-800/50 p-6 rounded-2xl shadow-xl border border-light-border dark:border-gray-700/30 mb-4">
                  <p class="text-lg text-light-text dark:text-gray-300 mb-2 flex items-center justify-center gap-2">
                    <UserCircleIcon class="w-6 h-6 text-cyan-400" />
                    {{ authStore.state.profile?.name }}
                  </p>
                  <router-link
                      to="/dashboard"
                      class="inline-flex items-center px-8 py-3.5 bg-gradient-to-r from-blue-600 to-cyan-500 border border-cyan-400/20 rounded-xl font-semibold text-white hover:from-blue-700 hover:to-cyan-600 transition-all duration-300 shadow-lg shadow-cyan-500/10 hover:shadow-cyan-500/20"
                  >
                    <ArrowRightCircleIcon class="w-5 h-5 mr-2" />
                    Панель управления
                  </router-link>
                </div>
              </div>

              <div v-else class="animate-slide-up">
                <div class="flex flex-col sm:flex-row gap-4 justify-center">
                  <router-link
                      to="/register"
                      class="inline-flex items-center justify-center px-8 py-3.5 bg-gradient-to-r from-purple-600 to-blue-500 border border-purple-400/20 rounded-xl font-semibold text-white hover:from-purple-700 hover:to-blue-600 transition-all duration-300 shadow-lg shadow-purple-500/10 hover:shadow-purple-500/20"
                  >
                    <QrCodeIcon class="w-5 h-5 mr-2" />
                    Зарегистрировать заведение
                  </router-link>
                  <router-link
                      to="/login"
                      class="inline-flex items-center justify-center px-8 py-3.5 bg-light-bg-secondary dark:bg-gray-800/50 hover:bg-light-bg-tertiary dark:hover:bg-gray-800/70 border border-light-border dark:border-gray-700/30 rounded-xl font-semibold text-light-text dark:text-gray-300 transition-all duration-300"
                  >
                    Войти в систему
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Features Section -->
      <section class="py-20 bg-light-bg dark:bg-gray-900">
        <div class="container mx-auto px-4">
          <div class="max-w-7xl mx-auto">
            <h2 class="text-3xl md:text-4xl font-bold text-light-text dark:text-white mb-16 text-center">Возможности платформы</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8">
              <!-- Feature 1 -->
              <div class="bg-light-bg-secondary dark:bg-gray-900/50 p-8 rounded-2xl border border-light-border dark:border-gray-700/20 hover:border-purple-400/30 transition-all duration-300 group">
                <div class="w-14 h-14 mb-6 rounded-xl bg-gradient-to-r from-purple-500 to-blue-500 flex items-center justify-center">
                  <QrCodeIcon class="w-8 h-8 text-white" />
                </div>
                <h3 class="text-xl font-bold text-light-text dark:text-white mb-3">QR-коды</h3>
                <p class="text-light-text-secondary dark:text-gray-400 leading-relaxed">Создавайте уникальные QR-коды для каждого заведения</p>
              </div>

              <!-- Feature 2 -->
              <div class="bg-light-bg-secondary dark:bg-gray-900/50 p-8 rounded-2xl border border-light-border dark:border-gray-700/20 hover:border-cyan-400/30 transition-all duration-300 group">
                <div class="w-14 h-14 mb-6 rounded-xl bg-gradient-to-r from-blue-500 to-cyan-500 flex items-center justify-center">
                  <QueueListIcon class="w-8 h-8 text-white" />
                </div>
                <h3 class="text-xl font-bold text-light-text dark:text-white mb-3">Управление запросами</h3>
                <p class="text-light-text-secondary dark:text-gray-400 leading-relaxed">Просматривайте и утверждайте трек-листы в реальном времени</p>
              </div>

              <!-- Feature 3 -->
              <div class="bg-light-bg-secondary dark:bg-gray-900/50 p-8 rounded-2xl border border-light-border dark:border-gray-700/20 hover:border-cyan-400/30 transition-all duration-300 group">
                <div class="w-14 h-14 mb-6 rounded-xl bg-gradient-to-r from-cyan-500 to-emerald-500 flex items-center justify-center">
                  <CurrencyDollarIcon class="w-8 h-8 text-white" />
                </div>
                <h3 class="text-xl font-bold text-light-text dark:text-white mb-3">Монетизация</h3>
                <p class="text-light-text-secondary dark:text-gray-400 leading-relaxed">Устанавливайте минимальные ставки и получайте платежи мгновенно</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- How It Works -->
      <section class="py-20 bg-light-bg-secondary dark:bg-gray-900">
        <div class="container mx-auto px-4">
          <div class="max-w-7xl mx-auto">
            <h2 class="text-3xl md:text-4xl font-bold text-light-text dark:text-white mb-16 text-center">Процесс работы</h2>
            <div class="grid md:grid-cols-2 gap-8 md:gap-12">
              <!-- DJ Column -->
              <div class="bg-light-bg dark:bg-gray-800/30 p-8 rounded-2xl border border-light-border dark:border-gray-700/20">
                <h3 class="text-2xl font-bold text-blue-400 mb-6 text-center">Для диджеев</h3>
                <div class="space-y-4">
                  <div class="flex gap-4 items-start p-5 bg-light-bg-secondary dark:bg-gray-900/50 rounded-xl hover:bg-light-bg-tertiary dark:hover:bg-gray-800/40 transition-all">
                    <div class="text-purple-400 text-2xl font-bold w-12 flex-shrink-0">1</div>
                    <div>
                      <h4 class="text-lg font-semibold text-light-text dark:text-white mb-2">Регистрация</h4>
                      <p class="text-light-text-secondary dark:text-gray-400 text-sm">Создайте аккаунт и добавьте информацию о заведении</p>
                    </div>
                  </div>

                  <div class="flex gap-4 items-start p-5 bg-light-bg-secondary dark:bg-gray-900/50 rounded-xl hover:bg-light-bg-tertiary dark:hover:bg-gray-800/40 transition-all">
                    <div class="text-blue-400 text-2xl font-bold w-12 flex-shrink-0">2</div>
                    <div>
                      <h4 class="text-lg font-semibold text-light-text dark:text-white mb-2">QR-код</h4>
                      <p class="text-light-text-secondary dark:text-gray-400 text-sm">Получите уникальный QR-код для вашего заведения</p>
                    </div>
                  </div>

                  <div class="flex gap-4 items-start p-5 bg-light-bg-secondary dark:bg-gray-900/50 rounded-xl hover:bg-light-bg-tertiary dark:hover:bg-gray-800/40 transition-all">
                    <div class="text-cyan-400 text-2xl font-bold w-12 flex-shrink-0">3</div>
                    <div>
                      <h4 class="text-lg font-semibold text-light-text dark:text-white mb-2">Управление треками</h4>
                      <p class="text-light-text-secondary dark:text-gray-400 text-sm">Добавляйте треки в очередь и управляйте запросами</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Visitor Column -->
              <div class="bg-light-bg dark:bg-gray-800/30 p-8 rounded-2xl border border-light-border dark:border-gray-700/20">
                <h3 class="text-2xl font-bold text-purple-400 mb-6 text-center">Для посетителей</h3>
                <div class="space-y-4">
                  <div class="flex gap-4 items-start p-5 bg-light-bg-secondary dark:bg-gray-900/50 rounded-xl hover:bg-light-bg-tertiary dark:hover:bg-gray-800/40 transition-all">
                    <div class="text-purple-400 text-2xl font-bold w-12 flex-shrink-0">1</div>
                    <div>
                      <h4 class="text-lg font-semibold text-light-text dark:text-white mb-2">Сканирование</h4>
                      <p class="text-light-text-secondary dark:text-gray-400 text-sm">Отсканируйте QR-код в заведении</p>
                    </div>
                  </div>

                  <div class="flex gap-4 items-start p-5 bg-light-bg-secondary dark:bg-gray-900/50 rounded-xl hover:bg-light-bg-tertiary dark:hover:bg-gray-800/40 transition-all">
                    <div class="text-blue-400 text-2xl font-bold w-12 flex-shrink-0">2</div>
                    <div>
                      <h4 class="text-lg font-semibold text-light-text dark:text-white mb-2">Выбор трека</h4>
                      <p class="text-light-text-secondary dark:text-gray-400 text-sm">Выберите трек из каталога или добавьте свой</p>
                    </div>
                  </div>

                  <div class="flex gap-4 items-start p-5 bg-light-bg-secondary dark:bg-gray-900/50 rounded-xl hover:bg-light-bg-tertiary dark:hover:bg-gray-800/40 transition-all">
                    <div class="text-cyan-400 text-2xl font-bold w-12 flex-shrink-0">3</div>
                    <div>
                      <h4 class="text-lg font-semibold text-light-text dark:text-white mb-2">Оплата</h4>
                      <p class="text-light-text-secondary dark:text-gray-400 text-sm">Оплатите запрос и дождитесь воспроизведения</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Demo Section -->
      <section class="py-20 bg-light-bg dark:bg-gray-900">
        <div class="container mx-auto px-4">
          <div class="max-w-7xl mx-auto">
            <div class="flex flex-col md:flex-row items-center gap-8 md:gap-12">
              <div class="flex-1">
                <h2 class="text-3xl md:text-4xl font-bold text-light-text dark:text-white mb-6">
                  Попробуйте прямо сейчас
                </h2>
                <p class="text-lg text-light-text-secondary dark:text-gray-400 mb-8">
                  Создайте аккаунт и получите доступ ко всем возможностям платформы. Управляйте музыкой в вашем заведении с помощью современных технологий.
                </p>
                <router-link
                    to="/register"
                    class="inline-flex items-center px-8 py-3.5 bg-gradient-to-r from-purple-600 to-blue-500 border border-purple-400/20 rounded-xl font-semibold text-white hover:from-purple-700 hover:to-blue-600 transition-all duration-300 shadow-lg shadow-purple-500/10 hover:shadow-purple-500/20"
                >
                  <QrCodeIcon class="w-5 h-5 mr-2" />
                  Начать бесплатно
                </router-link>
              </div>

              <div class="flex-1 max-w-md relative">
                <div class="relative p-8 bg-white/5 dark:bg-white/5 rounded-3xl transform rotate-3 hover:rotate-0 transition-all duration-500">
                  <div class="absolute inset-0 border-2 border-cyan-400/30 rounded-3xl transform -rotate-6 -m-4"></div>
                  <img src="/qr-demo.png" alt="QR Code Example" class="rounded-2xl w-full h-auto shadow-2xl">
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>

    <Footer />
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '../stores/auth';
import NavBar from "@/components/NavBar.vue";
import Footer from "@/components/Footer.vue";
import {
  UserCircleIcon,
  ArrowRightCircleIcon,
  QrCodeIcon,
  QueueListIcon,
  CurrencyDollarIcon,
  CheckCircleIcon
} from '@heroicons/vue/24/outline';

const authStore = useAuthStore();
</script>