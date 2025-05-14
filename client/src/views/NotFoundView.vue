<template>
  <div class="min-h-screen bg-gray-900 flex flex-col">
    <NavBar />

    <main class="flex-1 container mx-auto px-4 py-24 flex items-center justify-center">
      <div class="max-w-2xl text-center">
        <div class="animate-pulse mb-8">
          <ExclamationTriangleIcon class="w-24 h-24 text-red-400 mx-auto" />
        </div>

        <h1 class="text-6xl md:text-8xl font-bold mb-4 bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
          404
        </h1>

        <p class="text-xl md:text-2xl text-gray-400 mb-8">
          Запрашиваемая страница не существует
        </p>

        <router-link
            to="/"
            class="inline-flex items-center px-8 py-3.5 bg-gradient-to-r from-purple-600 to-blue-500 border border-purple-400/20 rounded-xl font-semibold text-white hover:from-purple-700 hover:to-blue-600 transition-all duration-300"
        >
          <ArrowLeftIcon class="w-5 h-5 mr-2" />
          Вернуться на главную
        </router-link>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup lang="ts">
import NavBar from "@/components/NavBar.vue";
import Footer from "@/components/Footer.vue";
import { ExclamationTriangleIcon, ArrowLeftIcon } from '@heroicons/vue/24/outline';
</script>

<style>
.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
</style>