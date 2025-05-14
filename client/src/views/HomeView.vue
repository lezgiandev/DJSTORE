<template>
  <div class="min-h-screen bg-gray-900 flex flex-col">
    <NavBar />

    <main class="flex-1">
      <!-- Hero Section -->
      <section class="relative py-20 bg-gradient-to-b from-gray-800 to-gray-900">
        <div class="container mx-auto px-4 text-center">
          <div class="max-w-4xl mx-auto">
            <h1 class="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent animate-fade-in">
              DJ STORE
            </h1>
            <p class="text-xl md:text-2xl text-gray-400 mb-12 mx-auto">
              Управляй музыкальной атмосферой своего заведения. Принимай запросы, создавай плейлисты и взаимодействуй с публикой через уникальные QR-коды!
            </p>

            <!-- Auth Section -->
            <div class="space-y-6">
              <div v-if="authStore.state.isAuthenticated" class="animate-slide-up">
                <div class="bg-gray-800/50 p-6 rounded-2xl shadow-xl border border-gray-700/30 mb-4">
                  <p class="text-lg text-gray-300 mb-2 flex items-center justify-center gap-2">
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
                <div class="flex gap-4 justify-center flex-wrap">
                  <router-link
                      to="/register"
                      class="flex items-center px-8 py-3.5 bg-gradient-to-r from-purple-600 to-blue-500 rounded-xl font-medium text-white hover:from-purple-700 hover:to-blue-600 transition-all duration-300 group shadow-lg shadow-purple-500/10 hover:shadow-purple-500/20"
                  >
                    <QrCodeIcon class="w-5 h-5 mr-2 group-hover:rotate-12 transition-transform" />
                    Зарегистрировать заведение
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Features Grid -->
      <section class="py-20 bg-gray-800/50">
        <div class="container mx-auto px-4">
          <h2 class="text-3xl md:text-4xl font-bold text-white mb-16 text-center">Возможности платформы</h2>

          <div class="grid md:grid-cols-3 gap-8">
            <!-- Feature 1 -->
            <div class="bg-gray-900/50 p-8 rounded-2xl border border-gray-700/20 hover:border-cyan-500/30 transition-all duration-300 group">
              <div class="w-14 h-14 mb-6 rounded-xl bg-gradient-to-r from-purple-500 to-blue-500 flex items-center justify-center">
                <QrCodeIcon class="w-8 h-8 text-white" />
              </div>
              <h3 class="text-xl font-bold text-white mb-3">Уникальные QR-коды</h3>
              <p class="text-gray-400 leading-relaxed">Генерируйте персональные коды для каждого заведения и управляйте доступом</p>
            </div>

            <!-- Feature 2 -->
            <div class="bg-gray-900/50 p-8 rounded-2xl border border-gray-700/20 hover:border-cyan-500/30 transition-all duration-300 group">
              <div class="w-14 h-14 mb-6 rounded-xl bg-gradient-to-r from-blue-500 to-cyan-500 flex items-center justify-center">
                <QueueListIcon class="w-8 h-8 text-white" />
              </div>
              <h3 class="text-xl font-bold text-white mb-3">Управление запросами</h3>
              <p class="text-gray-400 leading-relaxed">Просматривайте и утверждайте трек-листы в реальном времени</p>
            </div>

            <!-- Feature 3 -->
            <div class="bg-gray-900/50 p-8 rounded-2xl border border-gray-700/20 hover:border-cyan-500/30 transition-all duration-300 group">
              <div class="w-14 h-14 mb-6 rounded-xl bg-gradient-to-r from-cyan-500 to-emerald-500 flex items-center justify-center">
                <CurrencyDollarIcon class="w-8 h-8 text-white" />
              </div>
              <h3 class="text-xl font-bold text-white mb-3">Монетизация</h3>
              <p class="text-gray-400 leading-relaxed">Устанавливайте минимальные ставки и получайте платежи мгновенно</p>
            </div>
          </div>
        </div>
      </section>

      <!-- How It Works -->
      <section class="py-20 bg-gray-900">
        <div class="container mx-auto px-4">
          <div class="max-w-7xl mx-auto">
            <h2 class="text-3xl md:text-4xl font-bold text-white mb-16 text-center">Процесс работы</h2>

            <div class="grid md:grid-cols-2 gap-8">
              <!-- DJ Column -->
              <div class="bg-gray-800/30 p-8 rounded-2xl border border-gray-700/20">
                <h3 class="text-2xl font-bold text-cyan-400 mb-6 text-center">Для диджеев</h3>
                <div class="space-y-6">
                  <div class="flex gap-4 items-start p-5 bg-gray-900/50 rounded-xl hover:bg-gray-800/40 transition-all">
                    <div class="text-cyan-400 text-2xl font-bold w-12 flex-shrink-0">1</div>
                    <div>
                      <h4 class="text-lg font-semibold text-white mb-2">Регистрация заведения</h4>
                      <p class="text-gray-400 text-sm">Создайте профиль вашего клуба или бара с полной информацией</p>
                    </div>
                  </div>
                  <div class="flex gap-4 items-start p-5 bg-gray-900/50 rounded-xl hover:bg-gray-800/40 transition-all">
                    <div class="text-cyan-400 text-2xl font-bold w-12 flex-shrink-0">2</div>
                    <div>
                      <h4 class="text-lg font-semibold text-white mb-2">Генерация QR-кода</h4>
                      <p class="text-gray-400 text-sm">Получите уникальный код для размещения в заведении</p>
                    </div>
                  </div>
                  <div class="flex gap-4 items-start p-5 bg-gray-900/50 rounded-xl hover:bg-gray-800/40 transition-all">
                    <div class="text-cyan-400 text-2xl font-bold w-12 flex-shrink-0">3</div>
                    <div>
                      <h4 class="text-lg font-semibold text-white mb-2">Управление треками</h4>
                      <p class="text-gray-400 text-sm">Добавляйте треки в очередь и управляйте запросами</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Visitor Column -->
              <div class="bg-gray-800/30 p-8 rounded-2xl border border-gray-700/20">
                <h3 class="text-2xl font-bold text-purple-400 mb-6 text-center">Для посетителей</h3>
                <div class="space-y-6">
                  <div class="flex gap-4 items-start p-5 bg-gray-900/50 rounded-xl hover:bg-gray-800/40 transition-all">
                    <div class="text-purple-400 text-2xl font-bold w-12 flex-shrink-0">1</div>
                    <div>
                      <h4 class="text-lg font-semibold text-white mb-2">Сканирование кода</h4>
                      <p class="text-gray-400 text-sm">Наведите камеру на QR-код в заведении</p>
                    </div>
                  </div>
                  <div class="flex gap-4 items-start p-5 bg-gray-900/50 rounded-xl hover:bg-gray-800/40 transition-all">
                    <div class="text-purple-400 text-2xl font-bold w-12 flex-shrink-0">2</div>
                    <div>
                      <h4 class="text-lg font-semibold text-white mb-2">Выбор трека</h4>
                      <p class="text-gray-400 text-sm">Найдите нужный трек через удобный поиск</p>
                    </div>
                  </div>
                  <div class="flex gap-4 items-start p-5 bg-gray-900/50 rounded-xl hover:bg-gray-800/40 transition-all">
                    <div class="text-purple-400 text-2xl font-bold w-12 flex-shrink-0">3</div>
                    <div>
                      <h4 class="text-lg font-semibold text-white mb-2">Оплата и очередь</h4>
                      <p class="text-gray-400 text-sm">Укажите сумму и отправьте запрос диджею</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- QR Demo Section -->
      <section class="py-20 bg-gradient-to-br from-gray-800 to-gray-900">
        <div class="container mx-auto px-4">
          <div class="flex flex-col md:flex-row items-center justify-between gap-12">
            <div class="flex-1 max-w-xl">
              <h2 class="text-3xl md:text-4xl font-bold text-white mb-6">Ваш уникальный QR-код</h2>
              <p class="text-gray-400 text-lg mb-8">
                После регистрации заведения автоматически генерируется персонализированный QR-код,
                который можно распечатать или отобразить на экране. Посетители сканируют его,
                чтобы получить доступ к системе запросов треков.
              </p>
              <ul class="space-y-4 text-gray-300">
                <li class="flex items-center gap-3">
                  <CheckCircleIcon class="w-6 h-6 text-cyan-400" />
                  Автоматическая генерация
                </li>
                <li class="flex items-center gap-3">
                  <CheckCircleIcon class="w-6 h-6 text-cyan-400" />
                  Простое взаимодействие с клиентами
                </li>
                <li class="flex items-center gap-3">
                  <CheckCircleIcon class="w-6 h-6 text-cyan-400" />
                  Интеграция с системой оплаты
                </li>
              </ul>
            </div>
            <div class="flex-1 max-w-md relative">
              <div class="relative p-8 bg-white/5 rounded-3xl transform rotate-3 hover:rotate-0 transition-all duration-500">
                <div class="absolute inset-0 border-2 border-cyan-400/30 rounded-3xl transform -rotate-6 -m-4"></div>
                <img src="/qr-demo.png" alt="QR Code Example" class="rounded-2xl w-full h-auto shadow-2xl">
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