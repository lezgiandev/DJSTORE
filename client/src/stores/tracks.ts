import { defineStore } from 'pinia';
import { ref } from 'vue';
import { tracksAPI, genresAPI } from '../api/api';
import type { Track, Genre, TrackParams } from '@/types';

export const useTracksStore = defineStore('tracks', () => {
  const tracks = ref<Track[]>([]);
  const genres = ref<Genre[]>([]);
  const currentTrack = ref<Track | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function fetchTracks(venueId: number, params?: TrackParams) {
    try {
      loading.value = true;
      error.value = null;
      const response = await tracksAPI.getTracks(venueId, params);
      tracks.value = response.data;
    } catch (err: any) {
      console.error('Fetch tracks error:', err);
      error.value = err.response?.data?.detail || 'Ошибка при загрузке треков';
    } finally {
      loading.value = false;
    }
  }

  async function fetchTrack(venueId: number, trackId: number) {
    try {
      loading.value = true;
      error.value = null;
      const response = await tracksAPI.getTrack(venueId, trackId);
      currentTrack.value = response.data;
      return response.data;
    } catch (err: any) {
      console.error('Fetch track error:', err);
      error.value = err.response?.data?.detail || 'Ошибка при загрузке трека';
      return null;
    } finally {
      loading.value = false;
    }
  }

  async function addTrack(venueId: number, trackData: {
    title: string;
    genre_id: number;
    icon: string;
    artist: string;
    price: number;
  }) {
    try {
      loading.value = true;
      error.value = null;
      const response = await tracksAPI.addTrack(venueId, trackData);
      await fetchTracks(venueId);
      return response.data;
    } catch (err: any) {
      console.error('Add track error:', err);
      error.value = err.response?.data?.detail || 'Ошибка при добавлении трека';
      return null;
    } finally {
      loading.value = false;
    }
  }

  async function updateTrack(venueId: number, trackId: number, trackData: {
    title?: string;
    genre_id?: number;
    icon: string;
    artist?: string;
    price?: number;
  }) {
    try {
      loading.value = true;
      error.value = null;
      const response = await tracksAPI.updateTrack(venueId, trackId, trackData);
      currentTrack.value = response.data;
      await fetchTracks(venueId);
      return response.data;
    } catch (err: any) {
      console.error('Update track error:', err);
      error.value = err.response?.data?.detail || 'Ошибка при обновлении трека';
      return null;
    } finally {
      loading.value = false;
    }
  }

  async function deleteTrack(venueId: number, trackId: number) {
    try {
      loading.value = true;
      error.value = null;
      await tracksAPI.deleteTrack(venueId, trackId);
      await fetchTracks(venueId);
      return true;
    } catch (err: any) {
      console.error('Delete track error:', err);
      error.value = err.response?.data?.detail || 'Ошибка при удалении трека';
      return false;
    } finally {
      loading.value = false;
    }
  }

  async function fetchGenres() {
    try {
      loading.value = true;
      error.value = null;
      const response = await genresAPI.getGenres();
      genres.value = response.data;
    } catch (err: any) {
      console.error('Fetch genres error:', err);
      error.value = err.response?.data?.detail || 'Ошибка при загрузке жанров';
    } finally {
      loading.value = false;
    }
  }

  async function createGenre(name: string) {
    try {
      loading.value = true;
      error.value = null;
      const response = await genresAPI.createGenre(name);
      await fetchGenres();
      return response.data;
    } catch (err: any) {
      console.error('Create genre error:', err);
      error.value = err.response?.data?.detail || 'Ошибка при создании жанра';
      return null;
    } finally {
      loading.value = false;
    }
  }

  return {
    tracks,
    genres,
    currentTrack,
    loading,
    error,
    fetchTracks,
    fetchTrack,
    addTrack,
    updateTrack,
    deleteTrack,
    fetchGenres,
    createGenre
  };
}); 