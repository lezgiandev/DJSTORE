<template>
  <nav class="bg-gray-900/95 backdrop-blur-xl border-b border-gray-700/30 sticky top-0 z-50 shadow-xl shadow-black/30">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-20">
        <router-link
            to="/"
            class="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 text-2xl font-bold tracking-tighter hover:scale-105 transition-transform duration-300"
        >
          DJ STORE
        </router-link>

        <div class="hidden lg:flex items-center space-x-6">
          <!-- Для неавторизованных -->
          <router-link
              v-if="!authStore.state.isAuthenticated"
              to="/register"
              class="group flex items-center px-4 py-2 bg-gradient-to-r from-purple-600/30 to-blue-500/30 hover:from-purple-600/50 hover:to-blue-500/50 rounded-xl transition-all duration-300 border border-purple-400/20 hover:border-purple-400/40"
          >
            <QrCodeIcon class="w-5 h-5 mr-2 text-purple-400 group-hover:rotate-12 transition-transform" />
            <span class="text-gray-300 group-hover:text-white">Заведение</span>
          </router-link>

          <!-- Для авторизованных -->
          <template v-if="authStore.state.isAuthenticated">
            <router-link
                v-for="nav in mainNav"
                :key="nav.path"
                :to="nav.path"
                class="group flex items-center p-2.5 rounded-xl hover:bg-gray-800/40 transition-colors duration-300 relative"
                active-class="bg-gradient-to-r from-purple-600/20 to-blue-500/20"
            >
              <component
                  :is="nav.icon"
                  class="w-6 h-6 text-gray-300 group-hover:text-purple-400 transition-colors"
              />
              <span
                  class="absolute -bottom-7 left-1/2 -translate-x-1/2 bg-gray-800 px-2 py-1 rounded-md text-xs font-medium text-gray-300 opacity-0 group-hover:opacity-100 transition-opacity shadow-lg border border-gray-700/30"
              >
                {{ nav.title }}
              </span>
            </router-link>

            <button
                @click="authStore.logout()"
                class="flex items-center p-2.5 rounded-xl hover:bg-red-500/10 transition-colors duration-300 group relative"
            >
              <ArrowLeftEndOnRectangleIcon class="w-6 h-6 text-gray-300 group-hover:text-red-400 transition-colors" />
              <span class="absolute -bottom-7 left-1/2 -translate-x-1/2 bg-gray-800 px-2 py-1 rounded-md text-xs font-medium text-gray-300 opacity-0 group-hover:opacity-100 transition-opacity shadow-lg border border-gray-700/30">
                Выйти
              </span>
            </button>
          </template>
        </div>

        <!-- Мобильное меню -->
        <button
            @click="toggleMobileMenu"
            class="lg:hidden p-2.5 rounded-xl hover:bg-gray-800/50 transition-colors duration-300"
        >
          <Bars3BottomRightIcon
              class="w-7 h-7 text-gray-300"
              :class="{ 'rotate-90': isMobileMenuOpen }"
          />
        </button>
      </div>

      <!-- Мобильное меню -->
      <transition
          enter-active-class="transition-all duration-300 ease-out"
          leave-active-class="transition-all duration-200 ease-in"
          enter-from-class="opacity-0 max-h-0"
          enter-to-class="opacity-100 max-h-96"
          leave-from-class="opacity-100 max-h-96"
          leave-to-class="opacity-0 max-h-0"
      >
        <div v-show="isMobileMenuOpen" class="lg:hidden pb-4 space-y-2">
          <router-link
              v-if="!authStore.state.isAuthenticated"
              to="/register"
              @click="isMobileMenuOpen = false"
              class="flex items-center p-4 text-gray-300 hover:text-white hover:bg-gray-800/40 rounded-xl transition-all border border-purple-400/20"
          >
            <QrCodeIcon class="w-6 h-6 mr-3 text-purple-400" />
            Зарегистрировать заведение
          </router-link>

          <template v-if="authStore.state.isAuthenticated">
            <router-link
                v-for="nav in mainNav"
                :key="nav.path"
                :to="nav.path"
                @click="isMobileMenuOpen = false"
                class="flex items-center p-4 text-gray-300 hover:text-white hover:bg-gray-800/40 rounded-xl transition-colors group"
            >
              <component
                  :is="nav.icon"
                  class="w-6 h-6 mr-3 text-purple-400 group-hover:rotate-12 transition-transform"
              />
              {{ nav.title }}
            </router-link>

            <button
                @click="handleMobileLogout"
                class="w-full flex items-center p-4 text-gray-300 hover:text-red-400 hover:bg-red-500/10 rounded-xl transition-colors"
            >
              <ArrowLeftEndOnRectangleIcon class="w-6 h-6 mr-3" />
              Выйти из системы
            </button>
          </template>
        </div>
      </transition>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import {
  QrCodeIcon,
  UserCircleIcon,
  MusicalNoteIcon,
  QueueListIcon,
  CurrencyDollarIcon,
  BanknotesIcon,
  ArrowLeftEndOnRectangleIcon,
  Bars3BottomRightIcon
} from '@heroicons/vue/24/outline';

const authStore = useAuthStore();
const isMobileMenuOpen = ref(false);

const mainNav = [
  { path: '/dashboard', title: 'Профиль', icon: UserCircleIcon },
  { path: '/tracks', title: 'Треки', icon: MusicalNoteIcon },
  { path: '/requests', title: 'Запросы', icon: QueueListIcon },
  { path: '/finance', title: 'Финансы', icon: CurrencyDollarIcon },
  { path: '/withdrawals', title: 'Вывод', icon: BanknotesIcon },
];

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const handleMobileLogout = async () => {
  isMobileMenuOpen.value = false;
  await authStore.logout();
};
</script>