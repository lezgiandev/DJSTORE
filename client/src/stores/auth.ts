import { defineStore } from 'pinia';
import { ref } from 'vue';
import { authAPI } from '../api/api';
import type { AuthResponse, UserState, VenueProfile, RegisterData } from '@/types';
import { useRouter } from 'vue-router';

export const useAuthStore = defineStore('auth', () => {
  const state = ref<UserState>({
    isAuthenticated: !!localStorage.getItem('access_token'),
    profile: null
  });
  const loading = ref(false);
  const error = ref<string | null>(null);
  const router = useRouter();

  async function login(username: string, password: string) {
    try {
      loading.value = true;
      error.value = null;
      const response = await authAPI.login(username, password);
      const data = response.data as AuthResponse;
      
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      
      state.value.isAuthenticated = true;
      await fetchProfile();
      await router.push('/dashboard');
    } catch (err: any) {
      console.error('Login error:', err);
      error.value = err.response?.data?.detail || 'Ошибка при авторизации';
      state.value.isAuthenticated = false;
      state.value.profile = null;
    } finally {
      loading.value = false;
    }
  }

  async function register(userData: RegisterData) {
    try {
      loading.value = true;
      error.value = null;
      await authAPI.register(userData);
      await login(userData.username, userData.password);
    } catch (err: any) {
      console.error('Registration error:', err);
      error.value = err.response?.data?.detail || 'Ошибка при регистрации';
    } finally {
      loading.value = false;
    }
  }

  async function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    state.value.isAuthenticated = false;
    state.value.profile = null;
    await router.push('/login');
  }

  async function fetchProfile() {
    try {
      loading.value = true;
      error.value = null;
      if (!state.value.isAuthenticated) {
        return;
      }
      const response = await authAPI.getProfile();
      state.value.profile = response.data as VenueProfile;
    } catch (err: any) {
      console.error('Fetch profile error:', err);
      error.value = err.response?.data?.detail || 'Ошибка при загрузке профиля';
      if (err.response?.status === 401) {
        await logout();
      }
    } finally {
      loading.value = false;
    }
  }

  async function updateProfile(data: { name?: string; city?: string; phone?: string }) {
    try {
      loading.value = true;
      error.value = null;
      const response = await authAPI.updateProfile(data);
      state.value.profile = response.data as VenueProfile;
    } catch (err: any) {
      console.error('Update profile error:', err);
      error.value = err.response?.data?.detail || 'Ошибка при обновлении профиля';
    } finally {
      loading.value = false;
    }
  }

  async function init() {
    if (state.value.isAuthenticated && !state.value.profile) {
      await fetchProfile();
    }
  }

  return { 
    state, 
    loading, 
    error, 
    login, 
    register, 
    logout, 
    fetchProfile, 
    updateProfile,
    init
  };
}); 