<template>
  <nav class="bg-white/95 dark:bg-gray-900/95 backdrop-blur-xl border-b border-light-border dark:border-gray-700/30 sticky top-0 z-50 shadow-xl shadow-black/10 dark:shadow-black/30">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-20">
        <router-link
            to="/"
            class="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 text-2xl font-bold tracking-tighter hover:scale-105 transition-transform duration-300"
        >
          DJ STORE
        </router-link>

        <div class="hidden lg:flex items-center space-x-6">
          <!-- Кнопка переключения темы -->
          <button
              @click="themeStore.toggleTheme"
              class="p-2 text-light-text-secondary dark:text-gray-400 hover:text-light-text dark:hover:text-gray-200 transition-colors"
              :title="themeStore.isDark ? 'Светлая тема' : 'Тёмная тема'"
          >
            <SunIcon v-if="themeStore.isDark" class="w-6 h-6" />
            <MoonIcon v-else class="w-6 h-6" />
          </button>

          <!-- Для неавторизованных -->
          <router-link
              v-if="!authStore.state.isAuthenticated"
              to="/register"
              class="group flex items-center px-4 py-2 bg-gradient-to-r from-purple-600/30 to-blue-500/30 hover:from-purple-600/50 hover:to-blue-500/50 rounded-xl transition-all duration-300 border border-purple-400/20 hover:border-purple-400/40"
          >
            <QrCodeIcon class="w-5 h-5 mr-2 text-purple-400 group-hover:rotate-12 transition-transform" />
            <span class="text-light-text dark:text-gray-300 group-hover:text-white">Заведение</span>
          </router-link>

          <!-- Для авторизованных -->
          <template v-else>
            <router-link
                v-for="item in mainNav"
                :key="item.path"
                :to="item.path"
                class="group flex items-center text-light-text-secondary dark:text-gray-400 hover:text-light-text dark:hover:text-white transition-all duration-300"
            >
              <div class="w-2 h-2 mr-3 bg-purple-400 rounded-full opacity-0 group-hover:opacity-100 transition-all"/>
              <span class="relative before:absolute before:bottom-0 before:left-0 before:w-0 before:h-px before:bg-gradient-to-r before:from-purple-400 before:to-blue-400 before:transition-all before:duration-300 group-hover:before:w-full">
                {{ item.title }}
              </span>
            </router-link>

            <button
                @click="authStore.logout"
                class="group flex items-center text-light-text-secondary dark:text-gray-400 hover:text-red-500 transition-all duration-300"
            >
              <div class="w-2 h-2 mr-3 bg-red-400 rounded-full opacity-0 group-hover:opacity-100 transition-all"/>
              <span class="relative before:absolute before:bottom-0 before:left-0 before:w-0 before:h-px before:bg-red-400 before:transition-all before:duration-300 group-hover:before:w-full">
                Выйти
              </span>
            </button>
          </template>
        </div>

        <!-- Мобильное меню -->
        <div class="lg:hidden">
          <button
              @click="toggleMobileMenu"
              class="p-2 text-light-text-secondary dark:text-gray-400 hover:text-light-text dark:hover:text-gray-200 transition-colors"
          >
            <Bars3BottomRightIcon class="w-6 h-6" />
          </button>
        </div>
      </div>

      <!-- Мобильное меню -->
      <transition
          enter-active-class="transition duration-200 ease-out"
          enter-from-class="transform scale-95 opacity-0"
          enter-to-class="transform scale-100 opacity-100"
          leave-active-class="transition duration-100 ease-in"
          leave-from-class="transform scale-100 opacity-100"
          leave-to-class="transform scale-95 opacity-0"
      >
        <div
            v-if="isMobileMenuOpen"
            class="lg:hidden absolute top-20 inset-x-0 bg-white/95 dark:bg-gray-900/95 backdrop-blur-xl border-b border-light-border dark:border-gray-700/30 shadow-xl"
        >
          <div class="px-4 py-3 space-y-1">
            <!-- Кнопка переключения темы в мобильном меню -->
            <button
                @click="themeStore.toggleTheme"
                class="w-full flex items-center p-4 text-light-text-secondary dark:text-gray-300 hover:text-light-text dark:hover:text-gray-200 rounded-xl transition-colors"
            >
              <SunIcon v-if="themeStore.isDark" class="w-6 h-6 mr-3" />
              <MoonIcon v-else class="w-6 h-6 mr-3" />
              {{ themeStore.isDark ? 'Светлая тема' : 'Тёмная тема' }}
            </button>

            <!-- Для неавторизованных -->
            <router-link
                v-if="!authStore.state.isAuthenticated"
                to="/register"
                class="flex items-center p-4 text-light-text-secondary dark:text-gray-300 hover:text-light-text dark:hover:text-white rounded-xl transition-colors"
            >
              <QrCodeIcon class="w-6 h-6 mr-3" />
              Заведение
            </router-link>

            <!-- Для авторизованных -->
            <template v-else>
              <router-link
                  v-for="item in mainNav"
                  :key="item.path"
                  :to="item.path"
                  class="flex items-center p-4 text-light-text-secondary dark:text-gray-300 hover:text-light-text dark:hover:text-white rounded-xl transition-colors"
              >
                <component :is="item.icon" class="w-6 h-6 mr-3" />
                {{ item.title }}
              </router-link>

              <button
                  @click="handleMobileLogout"
                  class="w-full flex items-center p-4 text-light-text-secondary dark:text-gray-300 hover:text-red-500 rounded-xl transition-colors"
              >
                <ArrowLeftEndOnRectangleIcon class="w-6 h-6 mr-3" />
                Выйти из системы
              </button>
            </template>
          </div>
        </div>
      </transition>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useThemeStore } from '@/stores/theme';
import {
  QrCodeIcon,
  UserCircleIcon,
  MusicalNoteIcon,
  QueueListIcon,
  CurrencyDollarIcon,
  BanknotesIcon,
  ArrowLeftEndOnRectangleIcon,
  Bars3BottomRightIcon,
  SunIcon,
  MoonIcon
} from '@heroicons/vue/24/outline';

const authStore = useAuthStore();
const themeStore = useThemeStore();
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