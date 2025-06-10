<template>
  <div class="min-h-screen bg-light-bg dark:bg-gray-900 flex flex-col">
    <NavBar />

    <main class="flex-1 container mx-auto px-4 py-12">
      <div class="max-w-md mx-auto">
        <h1 class="text-4xl md:text-5xl font-bold mb-8 bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent text-center">
          Авторизация
        </h1>

        <div v-if="authStore.error" class="mb-6 p-4 bg-red-400/10 rounded-xl border border-red-400/30 text-red-400 flex items-center">
          <ExclamationCircleIcon class="w-5 h-5 mr-2" />
          {{ authStore.error }}
        </div>

        <form @submit.prevent="handleLogin" class="bg-light-bg-secondary dark:bg-gray-800/50 p-8 rounded-2xl border border-light-border dark:border-gray-700/30 space-y-6">
          <div>
            <label class="block text-light-text-secondary dark:text-gray-400 mb-2">Имя пользователя</label>
            <div class="relative">
              <UserCircleIcon class="w-5 h-5 absolute left-3 top-3 text-light-text-secondary dark:text-gray-400" />
              <input
                  id="username"
                  type="text"
                  v-model="username"
                  required
                  class="w-full pl-10 pr-4 py-3 text-light-text dark:text-white bg-light-bg dark:bg-gray-900 border border-light-border dark:border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all"
                  placeholder="Введите логин"
              />
            </div>
          </div>

          <div>
            <label class="block text-light-text-secondary dark:text-gray-400 mb-2">Пароль</label>
            <div class="relative">
              <LockClosedIcon class="w-5 h-5 absolute left-3 top-3 text-light-text-secondary dark:text-gray-400" />
              <input
                  id="password"
                  type="password"
                  v-model="password"
                  required
                  class="w-full pl-10 pr-4 py-3 text-light-text dark:text-white bg-light-bg dark:bg-gray-900 border border-light-border dark:border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all"
                  placeholder="Введите пароль"
              />
            </div>
          </div>

          <button
              type="submit"
              :disabled="authStore.loading"
              class="w-full py-3.5 bg-gradient-to-r from-purple-600 to-blue-500 border border-purple-400/20 rounded-xl font-semibold text-white hover:from-purple-700 hover:to-blue-600 transition-all disabled:opacity-50"
          >
            <span v-if="authStore.loading" class="flex items-center justify-center">
              <ArrowPathIcon class="w-5 h-5 mr-2 animate-spin" />
              Вход...
            </span>
            <span v-else>Войти</span>
          </button>

          <p class="text-center text-light-text-secondary dark:text-gray-400">
            Нет аккаунта?
            <router-link to="/register" class="text-purple-400 hover:text-purple-300 transition-colors">
              Зарегистрироваться
            </router-link>
          </p>
        </form>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import NavBar from "@/components/NavBar.vue";
import Footer from "@/components/Footer.vue";
import {
  ExclamationCircleIcon,
  UserCircleIcon,
  LockClosedIcon,
  ArrowPathIcon
} from '@heroicons/vue/24/outline';

const authStore = useAuthStore();

const username = ref('');
const password = ref('');

async function handleLogin() {
  await authStore.login(username.value, password.value);
}
</script>