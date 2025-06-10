<template>
  <div class="min-h-screen bg-light-bg dark:bg-gray-900 flex flex-col">
    <NavBar />

    <main class="flex-1 container mx-auto px-4 py-8 md:py-12">
      <div class="max-w-7xl mx-auto">
        <!-- Заголовок с кнопкой -->
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">
          <h1 class="text-3xl md:text-4xl font-bold bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent animate-fade-in">
            Управление треками
          </h1>
          <router-link
              to="/tracks/add"
              class="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-600/30 to-blue-500/30 hover:from-purple-600/50 hover:to-blue-500/50 rounded-xl border border-purple-400/30 hover:border-purple-400/50 transition-all group"
          >
            <PlusCircleIcon class="w-6 h-6 text-purple-400 group-hover:rotate-90 transition-transform" />
            <span class="text-purple-400 group-hover:text-white transition-colors">Добавить трек</span>
          </router-link>
        </div>

        <!-- Фильтры -->
        <div class="bg-light-bg-secondary dark:bg-gray-800/40 backdrop-blur-lg p-6 rounded-2xl border border-light-border dark:border-gray-700/30 shadow-xl mb-8 relative z-[99]">
          <div class="grid md:grid-cols-3 gap-4">
            <div class="relative">
              <Listbox v-model="filters.genre">
                <div class="relative z-[999]">
                  <ListboxButton class="w-full pl-10 pr-4 py-2.5 text-left text-light-text dark:text-white bg-light-bg dark:bg-gray-900/20 border border-light-border dark:border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 appearance-none">
                    <ListBulletIcon class="w-5 h-5 absolute left-3 top-3 text-light-text-secondary dark:text-gray-400 z-10" />
                    <span class="block truncate">
                      {{ filters.genre ? tracksStore.genres.find(g => g.id === filters.genre)?.name : 'Все жанры' }}
                    </span>
                    <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                      <ChevronUpDownIcon class="h-5 w-5 text-light-text-secondary dark:text-gray-400" aria-hidden="true" />
                    </span>
                  </ListboxButton>
                  <transition
                    leave-active-class="transition duration-100 ease-in"
                    leave-from-class="opacity-100"
                    leave-to-class="opacity-0"
                  >
                    <ListboxOptions class="absolute z-[9999] mt-1 max-h-60 w-full overflow-auto rounded-xl bg-light-bg-secondary dark:bg-gray-800/95 backdrop-blur-lg py-1 text-base shadow-lg border border-light-border dark:border-gray-700/30 focus:outline-none">
                      <ListboxOption
                        v-slot="{ active, selected }"
                        :value="null"
                        class="relative cursor-pointer select-none"
                      >
                        <span 
                          :class="[
                            active ? 'bg-purple-400/20 text-light-text dark:text-white' : 'text-light-text-secondary dark:text-gray-300',
                            'block truncate px-4 py-2'
                          ]"
                        >
                          Все жанры
                          <CheckIcon v-if="filters.genre === null" class="h-5 w-5 inline-block ml-2 text-purple-400" aria-hidden="true" />
                        </span>
                      </ListboxOption>
                      <ListboxOption
                        v-for="genre in tracksStore.genres"
                        :key="genre.id"
                        :value="genre.id"
                        v-slot="{ active, selected }"
                        class="relative cursor-pointer select-none"
                      >
                        <span 
                          :class="[
                            active ? 'bg-purple-400/20 text-light-text dark:text-white' : 'text-light-text-secondary dark:text-gray-300',
                            'block truncate px-4 py-2'
                          ]"
                        >
                          {{ genre.name }}
                          <CheckIcon v-if="selected" class="h-5 w-5 inline-block ml-2 text-purple-400" aria-hidden="true" />
                        </span>
                      </ListboxOption>
                    </ListboxOptions>
                  </transition>
                </div>
              </Listbox>
            </div>

            <div class="relative">
              <MagnifyingGlassIcon class="w-5 h-5 absolute left-3 top-3 text-light-text-secondary dark:text-gray-400 z-10" />
              <input
                  type="text"
                  v-model="filters.search"
                  placeholder="Поиск по названию или исполнителю"
                  class="w-full pl-10 pr-4 py-2.5 bg-light-bg dark:bg-gray-900/20 border text-light-text dark:text-white border-light-border dark:border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20"
              />
            </div>

            <div class="flex gap-2">
              <button
                  @click="applyFilters"
                  class="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 bg-purple-400/10 hover:bg-purple-400/20 border border-purple-400/30 rounded-xl transition-all group"
              >
                <FunnelIcon class="w-5 h-5 text-purple-400 group-hover:rotate-12 transition-transform" />
                <span class="text-purple-400">Применить</span>
              </button>
              <button
                  @click="resetFilters"
                  class="px-4 py-2.5 bg-light-bg dark:bg-gray-700/10 hover:bg-light-bg-secondary dark:hover:bg-gray-700/20 border border-light-border dark:border-gray-700/30 rounded-xl transition-all group"
              >
                <ArrowPathIcon class="w-5 h-5 text-light-text-secondary dark:text-gray-400 group-hover:rotate-180 transition-transform" />
              </button>
            </div>
          </div>
        </div>

        <!-- Контент треков -->
        <div class="bg-light-bg-secondary dark:bg-gray-800/40 backdrop-blur-lg z-0 rounded-2xl border border-light-border dark:border-gray-700/30 shadow-xl overflow-hidden">
          <div v-if="tracksStore.loading" class="p-8 text-center">
            <div class="inline-flex items-center gap-3 text-light-text-secondary dark:text-gray-400">
              <ArrowPathIcon class="w-6 h-6 animate-spin-once" />
              <span>Загрузка треков...</span>
            </div>
          </div>

          <div v-else-if="tracksStore.tracks.length === 0" class="p-8 text-center">
            <p class="text-light-text-secondary dark:text-gray-400 mb-4">Нет доступных треков</p>
            <router-link
                to="/tracks/add"
                class="text-purple-400 hover:text-purple-300 transition-colors"
            >
              Добавить первый трек
            </router-link>
          </div>

          <div v-else>
            <!-- Таблица для десктопов -->
            <div class="hidden md:block overflow-x-auto">
              <table class="w-full">
                <thead class="bg-light-bg dark:bg-gray-900/30 border-b border-light-border dark:border-gray-700/30">
                <tr>
                  <th class="px-6 py-4 text-left text-sm font-medium text-light-text-secondary dark:text-gray-400">Трек</th>
                  <th class="px-6 py-4 text-left text-sm font-medium text-light-text-secondary dark:text-gray-400">Жанр</th>
                  <th class="px-6 py-4 text-left text-sm font-medium text-light-text-secondary dark:text-gray-400">Цена</th>
                  <th class="px-6 py-4 text-right text-sm font-medium text-light-text-secondary dark:text-gray-400">Действия</th>
                </tr>
                </thead>
                <tbody class="divide-y divide-light-border dark:divide-gray-700/30">
                <tr
                    v-for="track in tracksStore.tracks"
                    :key="track.id"
                    class="hover:bg-light-bg dark:hover:bg-gray-700/10 transition-colors group"
                >
                  <td class="px-6 py-4">
                    <div class="flex items-center gap-4">
                      <div class="relative w-12 h-12 rounded-xl overflow-hidden shrink-0 border border-light-border dark:border-gray-700/30">
                        <img
                            :src="track.icon"
                            :alt="track.title"
                            class="w-full h-full object-cover"
                        >
                        <div class="absolute inset-0 bg-gradient-to-t from-gray-900/60 to-transparent"></div>
                        <MusicalNoteIcon class="absolute bottom-2 right-2 w-4 h-4 text-purple-400" />
                      </div>
                      <div>
                        <p class="font-medium text-light-text dark:text-gray-100">{{ track.title }}</p>
                        <p class="text-sm text-light-text-secondary dark:text-gray-400">{{ track.artist }}</p>
                      </div>
                    </div>
                  </td>

                  <td class="px-6 py-4">
                      <span class="px-3 py-1 bg-light-bg dark:bg-gray-900/50 rounded-full text-sm text-purple-400 border border-purple-400/20">
                        {{ track.genre.name }}
                      </span>
                  </td>

                  <td class="px-6 py-4">
                    <span class="text-green-400 font-medium">{{ track.price }} ₽</span>
                  </td>

                  <td class="px-6 py-4 text-right">
                    <div class="flex justify-end gap-2">
                      <router-link
                          :to="`/tracks/${track.id}/edit`"
                          class="p-2 bg-blue-400/10 hover:bg-blue-400/20 border border-blue-400/30 rounded-lg transition-colors group/edit"
                      >
                        <PencilSquareIcon class="w-5 h-5 text-blue-400 group-hover/edit:rotate-12 transition-transform" />
                      </router-link>

                      <button
                          @click="confirmDelete(track)"
                          class="p-2 bg-red-400/10 hover:bg-red-400/20 border border-red-400/30 rounded-lg transition-colors group/delete"
                      >
                        <TrashIcon class="w-5 h-5 text-red-400 group-hover/delete:rotate-12 transition-transform" />
                      </button>
                    </div>
                  </td>
                </tr>
                </tbody>
              </table>
            </div>

            <!-- Мобильные карточки -->
            <div class="md:hidden p-4 space-y-4">
              <div
                  v-for="track in tracksStore.tracks"
                  :key="track.id"
                  class="bg-light-bg dark:bg-gray-800/30 rounded-xl border border-light-border dark:border-gray-700/30 hover:border-purple-400/30 transition-all group"
              >
                <div class="flex items-start p-4 gap-3">
                  <div class="relative w-16 h-16 rounded-xl overflow-hidden shrink-0 border border-light-border dark:border-gray-700/30">
                    <img
                        :src="track.icon"
                        :alt="track.title"
                        class="w-full h-full object-cover"
                    >
                    <div class="absolute inset-0 bg-gradient-to-t from-gray-900/60 to-transparent"></div>
                    <MusicalNoteIcon class="absolute bottom-2 right-2 w-4 h-4 text-purple-400" />
                  </div>

                  <div class="flex-1 min-w-0">
                    <h3 class="font-medium text-light-text dark:text-gray-100 mb-1 truncate">{{ track.title }}</h3>
                    <p class="text-sm text-light-text-secondary dark:text-gray-400 mb-2">{{ track.artist }}</p>

                    <div class="flex flex-wrap items-center gap-2 mb-2">
                      <span class="px-3 py-1 bg-light-bg dark:bg-gray-900/50 rounded-full text-xs text-purple-400 border border-purple-400/20">
                        {{ track.genre.name }}
                      </span>
                      <span class="text-green-400 font-medium text-sm">{{ track.price }} ₽</span>
                    </div>
                  </div>
                </div>

                <div class="flex justify-between items-center px-4 py-3 bg-light-bg-secondary dark:bg-gray-900/20 border-t border-light-border dark:border-gray-700/30">
                  <router-link
                      :to="`/tracks/${track.id}/edit`"
                      class="flex items-center gap-1.5 text-blue-400 text-sm hover:text-blue-300 transition-colors"
                  >
                    <PencilSquareIcon class="w-4 h-4" />
                    <span>Редактировать</span>
                  </router-link>

                  <button
                      @click="confirmDelete(track)"
                      class="flex items-center gap-1.5 text-red-400 text-sm hover:text-red-300 transition-colors"
                  >
                    <TrashIcon class="w-4 h-4" />
                    <span>Удалить</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Модальное окно -->
    <transition name="fade">
      <div
          v-if="showDeleteModal"
          class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
      >
        <div class="bg-light-bg-secondary dark:bg-gray-800/95 backdrop-blur-lg p-8 rounded-2xl border border-light-border dark:border-gray-700/30 shadow-2xl max-w-md w-full">
          <div class="text-center mb-6">
            <ExclamationTriangleIcon class="w-12 h-12 text-red-400 mx-auto mb-4 animate-pulse" />
            <h3 class="text-xl font-bold text-light-text dark:text-gray-200 mb-2">Удалить трек?</h3>
            <p class="text-light-text-secondary dark:text-gray-400">
              Трек <span class="text-purple-400">"{{ trackToDelete?.title }}"</span> будет удалён безвозвратно
            </p>
          </div>

          <div class="flex justify-center gap-4">
            <button
                @click="cancelDelete"
                class="px-6 py-2.5 bg-light-bg dark:bg-gray-700/10 hover:bg-light-bg-secondary dark:hover:bg-gray-700/20 border border-light-border dark:border-gray-700/30 text-light-text-secondary dark:text-gray-400 rounded-xl transition-all"
            >
              Отмена
            </button>
            <button
                @click="deleteTrack"
                :disabled="tracksStore.loading"
                class="px-6 py-2.5 bg-red-400/10 hover:bg-red-400/20 border border-red-400/30 text-red-400 rounded-xl transition-all disabled:opacity-50"
            >
              <TrashIcon v-if="!tracksStore.loading" class="w-5 h-5 mr-2 inline" />
              <ArrowPathIcon v-else class="w-5 h-5 mr-2 animate-spin inline" />
              {{ tracksStore.loading ? 'Удаление...' : 'Удалить' }}
            </button>
          </div>
        </div>
      </div>
    </transition>

    <Footer />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useTracksStore } from '../stores/tracks';
import type { Track } from "@/types";
import NavBar from "@/components/NavBar.vue";
import Footer from "@/components/Footer.vue";
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/vue';
import {
  PlusCircleIcon,
  ListBulletIcon,
  MagnifyingGlassIcon,
  FunnelIcon,
  ArrowPathIcon,
  MusicalNoteIcon,
  PencilSquareIcon,
  TrashIcon,
  ExclamationTriangleIcon,
  ChevronUpDownIcon,
  CheckIcon
} from '@heroicons/vue/24/outline';

const authStore = useAuthStore();
const tracksStore = useTracksStore();

const filters = reactive({
  genre: null as number | null,
  search: ''
});

const showDeleteModal = ref(false);
const trackToDelete = ref<Track | null>(null);

async function applyFilters() {
  if (authStore.state.profile) {
    const params = {
      ...(filters.genre ? { genre: filters.genre } : {}),
      ...(filters.search ? { search: filters.search } : {})
    };
    await tracksStore.fetchTracks(authStore.state.profile.id, params);
  }
}

function resetFilters() {
  filters.genre = null;
  filters.search = '';
  if (authStore.state.profile) {
    tracksStore.fetchTracks(authStore.state.profile.id);
  }
}

function confirmDelete(track: Track) {
  trackToDelete.value = track;
  showDeleteModal.value = true;
}

function cancelDelete() {
  trackToDelete.value = null;
  showDeleteModal.value = false;
}

async function deleteTrack() {
  if (trackToDelete.value && authStore.state.profile) {
    await tracksStore.deleteTrack(authStore.state.profile.id, trackToDelete.value.id);
    showDeleteModal.value = false;
    trackToDelete.value = null;
  }
}

onMounted(async () => {
  await tracksStore.fetchGenres();
  if (authStore.state.profile) {
    await tracksStore.fetchTracks(authStore.state.profile.id);
  }
});
</script>
