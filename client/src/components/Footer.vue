<template>
  <footer class="bg-gray-900/95 backdrop-blur-xl border-t border-gray-700/30 shadow-2xl shadow-black/30">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-10 lg:gap-12">
        <!-- О нас -->
        <div class="space-y-5">
          <h3 class="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 text-2xl font-bold tracking-tighter">
            DJ STORE
          </h3>
          <p class="text-gray-400 leading-relaxed text-sm">
            Интерактивная платформа для управления музыкальными запросами в заведениях через QR-код
          </p>
        </div>

        <!-- Навигация -->
        <div class="space-y-5">
          <h4 class="text-lg font-semibold text-gray-200 bg-gradient-to-r from-purple-400/30 to-blue-400/30 w-max px-4 py-1 rounded-full">
            Навигация
          </h4>
          <ul class="space-y-3">
            <li v-for="link in links" :key="link.name">
              <router-link
                  :to="link.path"
                  class="group flex items-center text-gray-400 hover:text-white transition-all duration-300"
              >
                <div class="w-2 h-2 mr-3 bg-purple-400 rounded-full opacity-0 group-hover:opacity-100 transition-all"/>
                <span class="relative before:absolute before:bottom-0 before:left-0 before:w-0 before:h-px before:bg-gradient-to-r before:from-purple-400 before:to-blue-400 before:transition-all before:duration-300 group-hover:before:w-full">
                  {{ link.name }}
                </span>
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Контакты -->
        <div class="space-y-5">
          <h4 class="text-lg font-semibold text-gray-200 bg-gradient-to-r from-blue-400/30 to-cyan-400/30 w-max px-4 py-1 rounded-full">
            Контакты
          </h4>
          <ul class="space-y-4">
            <li class="flex items-center group">
              <div class="w-9 h-9 flex items-center justify-center bg-purple-400/10 rounded-lg mr-3 group-hover:bg-purple-400/20 transition-all">
                <EnvelopeIcon class="w-5 h-5 text-purple-400 group-hover:scale-110 transition-transform"/>
              </div>
              <span class="text-gray-400 group-hover:text-white transition-colors">support@djvc.com</span>
            </li>
            <li class="flex items-center group">
              <div class="w-9 h-9 flex items-center justify-center bg-blue-400/10 rounded-lg mr-3 group-hover:bg-blue-400/20 transition-all">
                <PhoneIcon class="w-5 h-5 text-blue-400 group-hover:scale-110 transition-transform"/>
              </div>
              <span class="text-gray-400 group-hover:text-white transition-colors">+7 (999) 888-77-66</span>
            </li>
          </ul>
        </div>

        <!-- Соцсети -->
        <div class="space-y-5">
          <h4 class="text-lg font-semibold text-gray-200 bg-gradient-to-r from-cyan-400/30 to-purple-400/30 w-max px-4 py-1 rounded-full">
            Сообщество
          </h4>
          <div class="flex gap-3 flex-wrap">
            <a
                v-for="social in socials"
                :key="social.name"
                :href="social.url"
                class="p-3 bg-gray-800/30 hover:bg-gradient-to-br from-purple-400/10 via-blue-400/10 to-cyan-400/10 rounded-xl transition-all duration-300 group border border-gray-700/30 hover:border-purple-400/30 relative overflow-hidden"
            >
              <div class="absolute inset-0 bg-gradient-to-br from-purple-400/5 to-blue-400/5 opacity-0 group-hover:opacity-100 transition-opacity"/>
              <component
                  :is="social.icon"
                  class="w-6 h-6 text-gray-400 group-hover:text-white transition-colors"
              />
            </a>
          </div>
        </div>
      </div>

      <div class="border-t border-gray-800/50 mt-12 pt-8 text-center">
        <p class="text-gray-500 text-sm">
          © 2025 <span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-cyan-400 font-medium">DJ STORE</span>.
          Все права защищены
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import {
  EnvelopeIcon,
  PhoneIcon,
  GlobeAltIcon,
  MusicalNoteIcon,
  UserGroupIcon,
  QrCodeIcon,
} from '@heroicons/vue/24/outline'

const links = [
  { name: 'Мои треки', path: '/tracks' },
  { name: 'Мои запросы', path: '/requests' },
  { name: 'Мои финансы', path: '/finance' },
  { name: 'Выводы', path: '/withdrawals' }
]

const socials = [
  {
    name: 'VKontakte',
    url: '#',
    icon: UserGroupIcon
  },
  {
    name: 'Telegram',
    url: '#',
    icon: GlobeAltIcon
  },
  {
    name: 'SoundCloud',
    url: '#',
    icon: MusicalNoteIcon
  },
  {
    name: 'QR Guide',
    url: '#',
    icon: QrCodeIcon
  }
]
</script>