<template>
  <div class="min-h-screen bg-gray-900 flex flex-col">
    <main class="flex-1 container mx-auto px-4 py-8 md:py-12">
      <div class="max-w-7xl mx-auto">
        <h1 class="text-3xl md:text-4xl font-bold mb-6 md:mb-10 bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent animate-fade-in">
          Заказ трека
        </h1>

        <div v-if="loading" class="text-center p-8 bg-gray-800/40 rounded-2xl border border-gray-700/30">
          <div class="inline-flex items-center gap-3 text-gray-400">
            <ArrowPathIcon class="w-6 h-6 animate-spin-once" />
            <span>Загрузка треков...</span>
          </div>
        </div>

        <div v-else-if="error" class="mb-6 p-4 bg-red-400/10 rounded-xl border border-red-400/30 text-red-400">
          {{ error }}
        </div>

        <div v-else-if="tracks.length === 0" class="p-8 bg-gray-800/40 rounded-2xl border border-gray-700/30 text-gray-400 text-center">
          В этом заведении нет доступных треков
        </div>

        <div v-else class="space-y-8">
          <!-- Фильтры -->
          <div class="bg-gray-800/40 backdrop-blur-lg p-6 rounded-2xl border border-gray-700/30 shadow-xl relative z-10">
            <div class="grid md:grid-cols-2 gap-4">
              <div class="relative">
                <MagnifyingGlassIcon class="w-5 h-5 absolute left-3 top-3.5 text-gray-400 z-10" />
                <input
                    id="search"
                    type="text"
                    v-model="searchQuery"
                    @input="filterTracks"
                    placeholder="Поиск по названию или исполнителю"
                    class="w-full pl-10 pr-4 py-2.5 text-white bg-gray-900/20 border border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all"
                />
              </div>

              <div class="relative">
                <ListBulletIcon class="w-5 h-5 absolute left-3 top-3.5 text-gray-400 z-10" />
                <div class="relative z-[999]">
                  <Listbox v-model="selectedGenre" @update:modelValue="filterTracks">
                    <ListboxButton class="w-full pl-10 pr-4 py-2.5 text-left text-white bg-gray-900/20 border border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 appearance-none transition-all">
                      <span class="block truncate">
                        {{ selectedGenre ? genres.find(g => g.id === selectedGenre)?.name : 'Все жанры' }}
                      </span>
                      <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                        <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                      </span>
                    </ListboxButton>
                    <transition
                      leave-active-class="transition duration-100 ease-in"
                      leave-from-class="opacity-100"
                      leave-to-class="opacity-0"
                    >
                      <ListboxOptions class="absolute z-[9999] mt-1 max-h-60 w-full overflow-auto rounded-xl bg-gray-800/95 backdrop-blur-lg py-1 text-base shadow-lg border border-gray-700/30 focus:outline-none">
                        <ListboxOption
                          v-slot="{ active, selected }"
                          :value="null"
                          class="relative cursor-pointer select-none"
                        >
                          <span 
                            :class="[
                              active ? 'bg-purple-400/20 text-white' : 'text-gray-300',
                              'block truncate px-4 py-2'
                            ]"
                          >
                            Все жанры
                            <CheckIcon v-if="selectedGenre === null" class="h-5 w-5 inline-block ml-2 text-purple-400" aria-hidden="true" />
                          </span>
                        </ListboxOption>
                        <ListboxOption
                          v-for="genre in genres"
                          :key="genre.id"
                          :value="genre.id"
                          v-slot="{ active, selected }"
                          class="relative cursor-pointer select-none"
                        >
                          <span 
                            :class="[
                              active ? 'bg-purple-400/20 text-white' : 'text-gray-300',
                              'block truncate px-4 py-2'
                            ]"
                          >
                            {{ genre.name }}
                            <CheckIcon v-if="selected" class="h-5 w-5 inline-block ml-2 text-purple-400" aria-hidden="true" />
                          </span>
                        </ListboxOption>
                      </ListboxOptions>
                    </transition>
                  </Listbox>
                </div>
              </div>
            </div>
          </div>

          <!-- Список треков -->
          <div class="bg-gray-800/40 backdrop-blur-lg rounded-2xl border border-gray-700/30 shadow-xl overflow-hidden z-0 relative">
            <div class="hidden md:grid grid-cols-12 gap-4 px-6 py-4 bg-gray-900/30 border-b border-gray-700/30">
              <div class="col-span-5 text-gray-400 font-medium">Трек</div>
              <div class="col-span-2 text-gray-400 font-medium">Жанр</div>
              <div class="col-span-2 text-gray-400 font-medium">Цена</div>
              <div class="col-span-3"></div>
            </div>

            <div class="grid gap-2 p-4">
              <div
                  v-for="track in filteredTracks"
                  :key="track.id"
                  class="group bg-gray-900/20 hover:bg-gray-800/40 rounded-xl border border-gray-700/30 hover:border-purple-400/30 transition-all"
              >
                <!-- Мобильная версия -->
                <div class="md:hidden p-4 space-y-4">
                  <div class="flex items-center gap-4">
                    <div class="relative flex-shrink-0 w-16 h-16">
                      <img
                          :src="track.icon"
                          :alt="track.title"
                          class="w-full h-full rounded-xl object-cover border border-gray-700/30 shadow-lg"
                      />
                      <div class="absolute inset-0 bg-gradient-to-t from-gray-900/60 to-transparent rounded-xl"></div>
                      <MusicalNoteIcon class="absolute bottom-2 right-2 w-4 h-4 text-purple-400" />
                    </div>
                    <div class="flex-1 min-w-0">
                      <h3 class="font-medium text-gray-100 truncate">{{ track.title }}</h3>
                      <p class="text-sm text-gray-400">{{ track.artist }}</p>
                    </div>
                  </div>
                  <div class="flex items-center justify-between">
                    <span class="px-3 py-1 bg-gray-800/50 rounded-full text-sm text-purple-400 border border-purple-400/20">
                      {{ track.genre.name }}
                    </span>
                    <span class="text-green-400 font-medium">{{ track.price }} ₽</span>
                  </div>
                  <button
                      @click="selectTrack(track)"
                      class="w-full py-2 bg-purple-400/10 hover:bg-purple-400/20 border border-purple-400/30 rounded-lg transition-all"
                  >
                    <span class="text-purple-400 group-hover:text-purple-300">Выбрать</span>
                  </button>
                </div>

                <!-- Десктоп версия -->
                <div class="hidden md:grid grid-cols-12 gap-4 items-center p-4">
                  <div class="col-span-5">
                    <div class="flex items-center gap-4">
                      <div class="relative flex-shrink-0 w-12 h-12">
                        <img
                            :src="track.icon"
                            :alt="track.title"
                            class="w-full h-full rounded-xl object-cover border border-gray-700/30 shadow-lg"
                        />
                        <div class="absolute inset-0 bg-gradient-to-t from-gray-900/60 to-transparent rounded-xl"></div>
                        <MusicalNoteIcon class="absolute bottom-2 right-2 w-4 h-4 text-purple-400" />
                      </div>
                      <div>
                        <h3 class="font-medium text-gray-100">{{ track.title }}</h3>
                        <p class="text-sm text-gray-400">{{ track.artist }}</p>
                      </div>
                    </div>
                  </div>
                  <div class="col-span-2">
                    <span class="px-3 py-1 bg-gray-800/50 rounded-full text-sm text-purple-400 border border-purple-400/20">
                      {{ track.genre.name }}
                    </span>
                  </div>
                  <div class="col-span-2 text-green-400 font-medium">
                    {{ track.price }} ₽
                  </div>
                  <div class="col-span-3 text-right">
                    <button
                        @click="selectTrack(track)"
                        class="px-4 py-2 bg-purple-400/10 hover:bg-purple-400/20 border border-purple-400/30 rounded-lg transition-all group/btn"
                    >
                      <span class="text-purple-400 group-hover/btn:text-purple-300">Выбрать</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Модальное окно выбора цены -->
    <transition name="fade">
      <div
          v-if="showPriceModal"
          class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
      >
        <div class="bg-gray-800/95 backdrop-blur-lg p-8 rounded-2xl border border-gray-700/30 shadow-2xl max-w-md w-full">
          <h3 class="text-xl font-bold text-gray-200 mb-4 truncate">
            {{ selectedTrack?.title }} - {{ selectedTrack?.artist }}
          </h3>

          <form @submit.prevent="createRequest" class="space-y-6">
            <div>
              <label class="block text-gray-400 mb-2">Ваша цена</label>
              <input
                  type="number"
                  v-model.number="userFee"
                  :min="selectedTrack?.price || 0"
                  required
                  class="w-full p-3.5 bg-gray-900/20 border text-white border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all"
                  :placeholder="`Минимум ${selectedTrack?.price} ₽`"
              />
            </div>

            <div class="flex flex-col sm:flex-row gap-4">
              <button
                  type="button"
                  @click="cancelTrackSelection"
                  class="px-6 py-2.5 bg-gray-700/10 hover:bg-gray-700/20 border border-gray-700/30 text-gray-400 rounded-xl transition-all"
              >
                Отмена
              </button>
              <button
                  type="submit"
                  :disabled="requestLoading || userFee < (selectedTrack?.price || 0)"
                  class="px-6 py-2.5 bg-gradient-to-r from-purple-600/30 to-blue-500/30 hover:from-purple-600/50 hover:to-blue-500/50 border border-purple-400/30 text-purple-400 rounded-xl transition-all disabled:opacity-50"
              >
                <ArrowPathIcon v-if="requestLoading" class="w-5 h-5 mr-2 animate-spin inline" />
                {{ requestLoading ? 'Обработка...' : 'Заказать' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- Модальное окно результата -->
    <transition name="fade">
      <div
          v-if="showResultModal"
          class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
      >
        <div class="bg-gray-800/95 backdrop-blur-lg p-8 rounded-2xl border border-gray-700/30 shadow-2xl max-w-md w-full">
          <div class="text-center mb-6">
            <CheckCircleIcon class="w-12 h-12 text-green-400 mx-auto mb-4 animate-pulse" />
            <h3 class="text-xl font-bold text-gray-200 mb-2">Запрос успешно создан!</h3>
          </div>

          <div class="space-y-4 mb-6">
            <div class="p-4 bg-gray-900/20 rounded-xl">
              <p class="text-gray-100 font-medium truncate">{{ currentRequest?.track.title }}</p>
              <p class="text-sm text-gray-400">{{ currentRequest?.track.artist }}</p>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div class="p-3 bg-gray-900/20 rounded-lg">
                <p class="text-xs text-gray-400 mb-1">Ваша цена</p>
                <p class="text-green-400 font-medium">{{ currentRequest?.user_fee }} ₽</p>
              </div>
              <div class="p-3 bg-gray-900/20 rounded-lg">
                <p class="text-xs text-gray-400 mb-1">Статус</p>
                <span :class="currentRequest?.is_paid ? 'text-green-400' : 'text-amber-400'" class="font-medium">
                  {{ currentRequest?.is_paid ? 'Оплачен' : 'Ожидает оплаты' }}
                </span>
              </div>
            </div>
          </div>

          <div class="flex flex-col gap-3">
            <button
                v-if="!currentRequest?.is_paid"
                @click="goToPayment"
                class="w-full py-2.5 bg-green-400/10 hover:bg-green-400/20 border border-green-400/30 text-green-400 rounded-xl transition-all"
            >
              Перейти к оплате
            </button>
            <button
                @click="closeResultModal"
                class="w-full py-2.5 bg-gray-700/10 hover:bg-gray-700/20 border border-gray-700/30 text-gray-400 rounded-xl transition-all"
            >
              Закрыть
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import type { Track, Genre, TrackRequest } from '@/types';
import {
  ArrowPathIcon,
  MusicalNoteIcon,
  MagnifyingGlassIcon,
  ListBulletIcon,
  CheckCircleIcon,
  ChevronUpDownIcon,
  CheckIcon
} from '@heroicons/vue/24/outline';
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/vue';

const route = useRoute();
const router = useRouter();

const venueId = computed(() => Number(route.params.id));
const tracks = ref<Track[]>([]);
const genres = ref<Genre[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

const searchQuery = ref('');
const selectedGenre = ref<number | null>(null);
const filteredTracks = ref<Track[]>([]);

const showPriceModal = ref(false);
const selectedTrack = ref<Track | null>(null);
const userFee = ref(0);
const requestLoading = ref(false);

const showResultModal = ref(false);
const currentRequest = ref<TrackRequest | null>(null);

async function fetchTracks() {
  try {
    loading.value = true;
    error.value = null;
    
    const response = await axios.get(`http://127.0.0.1:8000/api/venue/${venueId.value}/tracks/`);
    tracks.value = response.data;
    filteredTracks.value = response.data;

    const uniqueGenres: Record<number, Genre> = {};
    
    tracks.value.forEach(track => {
      uniqueGenres[track.genre.id] = track.genre;
    });
    
    genres.value = Object.values(uniqueGenres);
  } catch (err: any) {
    console.error('Error fetching tracks:', err);
    error.value = err.response?.data?.detail || 'Ошибка при загрузке треков';
  } finally {
    loading.value = false;
  }
}

function filterTracks() {
  filteredTracks.value = tracks.value.filter(track => {
    const matchesSearch = !searchQuery.value || 
      track.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      track.artist.toLowerCase().includes(searchQuery.value.toLowerCase());
    
    const matchesGenre = !selectedGenre.value || track.genre.id === selectedGenre.value;
    
    return matchesSearch && matchesGenre;
  });
}

function selectTrack(track: Track) {
  selectedTrack.value = track;
  userFee.value = track.price;
  showPriceModal.value = true;
}

function cancelTrackSelection() {
  selectedTrack.value = null;
  userFee.value = 0;
  showPriceModal.value = false;
}

async function createRequest() {
  if (!selectedTrack.value) {
    return;
  }
  
  try {
    requestLoading.value = true;
    
    const response = await axios.post(`http://127.0.0.1:8000/api/venue/${venueId.value}/request/`, {
      track: selectedTrack.value.id,
      user_fee: userFee.value
    });
    
    currentRequest.value = response.data;
    showPriceModal.value = false;
    showResultModal.value = true;
  } catch (err: any) {
    console.error('Error creating track request:', err);
    error.value = err.response?.data?.detail || 'Ошибка при создании запроса на трек';
  } finally {
    requestLoading.value = false;
  }
}

function goToPayment() {
  if (currentRequest.value) {
    router.push(`/request/pay/${currentRequest.value.payment_token}`);
  }
}

function closeResultModal() {
  showResultModal.value = false;
  currentRequest.value = null;
}

onMounted(() => {
  fetchTracks();
});
</script> 