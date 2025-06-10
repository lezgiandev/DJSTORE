<template>
  <div class="min-h-screen bg-light-bg dark:bg-gray-900 flex flex-col">
    <NavBar />

    <main class="flex-1 container mx-auto px-4 py-12">
      <div class="max-w-md mx-auto">
        <h1 class="text-4xl md:text-5xl font-bold mb-8 bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent text-center">
          Регистрация заведения
        </h1>

        <div v-if="authStore.error" class="mb-6 p-4 bg-red-400/10 rounded-xl border border-red-400/30 text-red-400 flex items-center">
          <ExclamationCircleIcon class="w-5 h-5 mr-2" />
          {{ authStore.error }}
        </div>

        <form @submit.prevent="handleRegister" class="bg-light-bg-secondary dark:bg-gray-800/50 p-8 rounded-2xl border border-light-border dark:border-gray-700/30 space-y-6">
          <div>
            <label class="block text-light-text-secondary dark:text-gray-400 mb-2">Имя пользователя</label>
            <input
                id="username"
                type="text"
                v-model="formData.username"
                required
                class="w-full p-3 text-light-text dark:text-white bg-light-bg dark:bg-gray-900 border border-light-border dark:border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all"
                placeholder="Введите логин"
            />
          </div>

          <div>
            <label class="block text-light-text-secondary dark:text-gray-400 mb-2">Пароль</label>
            <input
                id="password"
                type="password"
                v-model="formData.password"
                required
                class="w-full p-3 text-light-text dark:text-white bg-light-bg dark:bg-gray-900 border border-light-border dark:border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all"
                placeholder="Введите пароль"
            />
          </div>

          <div>
            <label class="block text-light-text-secondary dark:text-gray-400 mb-2">Email</label>
            <input
                id="email"
                type="email"
                v-model="formData.email"
                required
                class="w-full p-3 text-light-text dark:text-white bg-light-bg dark:bg-gray-900 border border-light-border dark:border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all"
                placeholder="example@mail.com"
            />
          </div>

          <div>
            <label class="block text-light-text-secondary dark:text-gray-400 mb-2">Название заведения</label>
            <input
                id="name"
                type="text"
                v-model="formData.name"
                required
                class="w-full p-3 text-light-text dark:text-white bg-light-bg dark:bg-gray-900 border border-light-border dark:border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all"
                placeholder="Введите название"
            />
          </div>

          <div>
            <label class="block text-light-text-secondary dark:text-gray-400 mb-2">Город</label>
            <input
                id="city"
                type="text"
                v-model="formData.city"
                required
                class="w-full p-3 text-light-text dark:text-white bg-light-bg dark:bg-gray-900 border border-light-border dark:border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all"
                placeholder="Введите город"
            />
          </div>

          <div>
            <label class="block text-light-text-secondary dark:text-gray-400 mb-2">Телефон</label>
            <input
                id="phone"
                type="tel"
                v-model="formData.phone"
                required
                class="w-full p-3 text-light-text dark:text-white bg-light-bg dark:bg-gray-900 border border-light-border dark:border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all"
                placeholder="+7 999 999-99-99"
            />
          </div>

          <button
              type="submit"
              :disabled="authStore.loading"
              class="w-full py-3.5 bg-gradient-to-r from-purple-600 to-blue-500 border border-purple-400/20 rounded-xl font-semibold text-white hover:from-purple-700 hover:to-blue-600 transition-all disabled:opacity-50"
          >
            <span v-if="authStore.loading" class="flex items-center justify-center">
              <ArrowPathIcon class="w-5 h-5 mr-2 animate-spin" />
              Регистрация...
            </span>
            <span v-else>Зарегистрироваться</span>
          </button>

          <p class="text-center text-light-text-secondary dark:text-gray-400">
            Уже есть аккаунт?
            <router-link to="/login" class="text-purple-400 hover:text-purple-300 transition-colors">
              Войти
            </router-link>
          </p>
        </form>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue';
import { useAuthStore } from '../stores/auth';
import type { RegisterData } from '@/types';
import NavBar from "@/components/NavBar.vue";
import Footer from "@/components/Footer.vue";
import { ExclamationCircleIcon, ArrowPathIcon } from '@heroicons/vue/24/outline';

const authStore = useAuthStore();

const formData = reactive<RegisterData>({
  username: '',
  password: '',
  email: '',
  name: '',
  city: '',
  phone: ''
});

async function handleRegister() {
  await authStore.register(formData);
}
</script>