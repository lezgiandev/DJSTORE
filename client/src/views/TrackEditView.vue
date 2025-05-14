<template>
  <div class="min-h-screen bg-gray-900 flex flex-col">
    <NavBar />

    <main class="flex-1 container mx-auto px-4 py-8 md:py-12">
      <div class="max-w-4xl mx-auto">
        <h1 class="text-3xl md:text-4xl font-bold mb-6 md:mb-10 bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent animate-fade-in">
          Редактирование трека
        </h1>

        <div v-if="tracksStore.loading && !tracksStore.currentTrack" class="text-center p-8 bg-gray-800/40 rounded-2xl border border-gray-700/30">
          <div class="inline-flex items-center gap-3 text-gray-400">
            <ArrowPathIcon class="w-6 h-6 animate-spin-once" />
            <span>Загрузка данных...</span>
          </div>
        </div>

        <div v-else-if="tracksStore.error" class="mb-6 p-4 bg-red-400/10 rounded-xl border border-red-400/30 text-red-400">
          {{ tracksStore.error }}
        </div>

        <div v-else-if="tracksStore.currentTrack" class="bg-gray-800/40 backdrop-blur-lg p-6 md:p-8 rounded-2xl border border-gray-700/30 shadow-xl relative z-[10]">
          <form @submit.prevent="handleSubmit" class="space-y-6">
            <div>
              <label class="block text-gray-400 mb-2">Название трека</label>
              <input
                  type="text"
                  v-model="formData.title"
                  required
                  class="w-full p-3.5 bg-gray-900/20 border text-white border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all placeholder-gray-500"
                  placeholder="Введите название"
              />
            </div>

            <div>
              <label class="block text-gray-400 mb-2">Исполнитель</label>
              <input
                  type="text"
                  v-model="formData.artist"
                  required
                  class="w-full p-3.5 bg-gray-900/20 border text-white border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all placeholder-gray-500"
                  placeholder="Введите исполнителя"
              />
            </div>

            <div>
              <label class="block text-gray-400 mb-2">Обложка трека</label>
              <input
                  type="text"
                  v-model="formData.icon"
                  required
                  class="w-full p-3.5 bg-gray-900/20 border text-white border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all placeholder-gray-500"
                  placeholder="Ссылка на изображение"
              />
            </div>

            <div>
              <label class="block text-gray-400 mb-2">Жанр</label>
              <div class="flex gap-2">
                <div class="relative flex-1">
                  <Listbox v-model="formData.genre_id" as="div" class="w-full">
                    <input type="hidden" :value="formData.genre_id" required />
                    <div class="relative z-[999]">
                      <ListboxButton class="w-full pl-4 pr-10 py-3.5 text-left text-white bg-gray-900/20 border border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 appearance-none transition-all placeholder-gray-500">
                        <span class="block truncate">
                          {{ formData.genre_id ? tracksStore.genres.find(g => g.id === Number(formData.genre_id))?.name : 'Выберите жанр' }}
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
                            :value="''"
                            disabled
                            class="relative cursor-pointer select-none"
                          >
                            <span 
                              :class="[
                                active ? 'bg-purple-400/20 text-white' : 'text-gray-300',
                                'block truncate px-4 py-2'
                              ]"
                            >
                              Выберите жанр
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
                    </div>
                  </Listbox>
                </div>
                <button
                    type="button"
                    @click="showAddGenre = true"
                    class="p-3.5 bg-gray-900/20 hover:bg-purple-400/10 border border-gray-700/30 hover:border-purple-400/30 rounded-xl transition-all group"
                >
                  <PlusCircleIcon class="w-6 h-6 text-purple-400 group-hover:rotate-90 transition-transform" />
                </button>
              </div>
            </div>

            <div>
              <label class="block text-gray-400 mb-2">Цена</label>
              <input
                  type="number"
                  v-model.number="formData.price"
                  min="1"
                  required
                  class="w-full p-3.5 bg-gray-900/20 border text-white border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all placeholder-gray-500"
                  placeholder="Стоимость в рублях"
              />
            </div>

            <div class="flex flex-col md:flex-row gap-4 justify-end">
              <router-link
                  to="/tracks"
                  class="px-6 py-3 text-gray-400 hover:text-gray-200 transition-colors text-center"
              >
                Отмена
              </router-link>
              <button
                  type="submit"
                  :disabled="tracksStore.loading"
                  class="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-500 border border-purple-400/20 rounded-xl font-semibold text-white hover:from-purple-700 hover:to-blue-600 transition-all disabled:opacity-50 group"
              >
                <span v-if="tracksStore.loading" class="flex items-center justify-center">
                  <ArrowPathIcon class="w-5 h-5 mr-2 animate-spin" />
                  Сохранение...
                </span>
                <span v-else class="group-hover:translate-x-1 transition-transform">Обновить трек</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </main>

    <!-- Модальное окно добавления жанра -->
    <transition name="fade">
      <div
          v-if="showAddGenre"
          class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
      >
        <div class="bg-gray-800/95 backdrop-blur-lg p-8 rounded-2xl border border-gray-700/30 shadow-2xl max-w-md w-full">
          <h3 class="text-xl font-bold text-gray-200 mb-6 bg-gradient-to-r from-cyan-400/30 to-purple-400/30 w-max px-4 py-1 rounded-full">
            Новый жанр
          </h3>

          <form @submit.prevent="handleAddGenre" class="space-y-6">
            <div>
              <label class="block text-gray-400 mb-2">Название жанра</label>
              <input
                  type="text"
                  v-model="newGenreName"
                  required
                  class="w-full p-3.5 bg-gray-900/20 border text-white border-gray-700/30 rounded-xl focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all placeholder-gray-500"
                  placeholder="Введите название"
              />
            </div>

            <div class="flex flex-col md:flex-row gap-4 justify-end">
              <button
                  type="button"
                  @click="showAddGenre = false"
                  class="px-6 py-3 bg-gray-700/10 hover:bg-gray-700/20 border border-gray-700/30 text-gray-400 rounded-xl transition-all"
              >
                Отмена
              </button>
              <button
                  type="submit"
                  :disabled="tracksStore.loading"
                  class="px-6 py-3 bg-gradient-to-r from-purple-600/30 to-blue-500/30 hover:from-purple-600/50 hover:to-blue-500/50 border border-purple-400/30 text-purple-400 rounded-xl transition-all disabled:opacity-50 group"
              >
                <PlusCircleIcon class="w-5 h-5 mr-2 group-hover:rotate-90 transition-transform" />
                {{ tracksStore.loading ? 'Создание...' : 'Создать' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <Footer />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { useTracksStore } from '../stores/tracks';
import NavBar from "@/components/NavBar.vue";
import Footer from "@/components/Footer.vue";
import {
  PlusCircleIcon,
  ArrowPathIcon,
  ChevronUpDownIcon,
  CheckIcon
} from '@heroicons/vue/24/outline';
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/vue';

const authStore = useAuthStore();
const tracksStore = useTracksStore();
const router = useRouter();
const route = useRoute();

const formData = reactive({
  title: '',
  artist: '',
  icon: '',
  genre_id: '',
  price: 0
});

const showAddGenre = ref(false);
const newGenreName = ref('');

onMounted(async () => {
  await tracksStore.fetchGenres();

  if (authStore.state.profile) {
    const trackId = Number(route.params.id);
    const track = await tracksStore.fetchTrack(authStore.state.profile.id, trackId);

    if (track) {
      formData.title = track.title;
      formData.artist = track.artist;
      formData.icon = track.icon;
      formData.genre_id = track.genre.id;
      formData.price = track.price;
    } else {
      await router.push('/tracks');
    }
  }
});

async function handleSubmit() {
  if (!authStore.state.profile || !tracksStore.currentTrack) return;

  if (!formData.genre_id) {
    tracksStore.error = 'Выберите жанр трека';
    return;
  }

  const trackId = Number(route.params.id);
  const result = await tracksStore.updateTrack(
      authStore.state.profile.id,
      trackId,
      {
        title: formData.title,
        artist: formData.artist,
        icon: formData.icon,
        genre_id: Number(formData.genre_id),
        price: Number(formData.price)
      }
  );

  if (result) await router.push('/tracks');
}

async function handleAddGenre() {
  if (newGenreName.value.trim()) {
    const result = await tracksStore.createGenre(newGenreName.value.trim());
    if (result) {
      formData.genre_id = result.id;
      showAddGenre.value = false;
      newGenreName.value = '';
    }
  }
}
</script>
