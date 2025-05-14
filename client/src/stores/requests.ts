import { defineStore } from 'pinia';
import { ref } from 'vue';
import { requestsAPI } from '../api/api';
import type { TrackRequest } from '@/types';

export const useRequestsStore = defineStore('requests', () => {
  const requests = ref<TrackRequest[]>([]);
  const currentRequest = ref<TrackRequest | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const paymentUrl = ref<string | null>(null);

  async function fetchRequests() {
    try {
      loading.value = true;
      error.value = null;
      const response = await requestsAPI.getRequests();
      requests.value = response.data;
    } catch (err: any) {
      console.error('Fetch requests error:', err);
      error.value = err.response?.data?.detail || 'Ошибка при загрузке запросов';
    } finally {
      loading.value = false;
    }
  }

  async function createRequest(venueId: number, data: { track: number; user_fee: number }) {
    try {
      loading.value = true;
      error.value = null;
      const response = await requestsAPI.createRequest(venueId, data);
      currentRequest.value = response.data;
      return response.data;
    } catch (err: any) {
      console.error('Create request error:', err);
      error.value = err.response?.data?.detail || 'Ошибка при создании запроса';
      return null;
    } finally {
      loading.value = false;
    }
  }

  async function payRequest(paymentToken: string, amount: number) {
    try {
      loading.value = true;
      error.value = null;
      const response = await requestsAPI.payRequest(paymentToken, amount);
      if (currentRequest.value && currentRequest.value.payment_token === paymentToken) {
        currentRequest.value.is_paid = true;
      }
      return response.data;
    } catch (err: any) {
      console.error('Pay request error:', err);
      error.value = err.response?.data?.detail || 'Ошибка при оплате запроса';
      return null;
    } finally {
      loading.value = false;
    }
  }

  async function updateRequestStatus(requestId: number, status: 'pending' | 'accepted' | 'rejected') {
    try {
      loading.value = true;
      error.value = null;
      const response = await requestsAPI.updateRequestStatus(requestId, status);
      await fetchRequests();
      return response.data;
    } catch (err: any) {
      console.error('Update request status error:', err);
      error.value = err.response?.data?.detail || 'Ошибка при обновлении статуса запроса';
      return null;
    } finally {
      loading.value = false;
    }
  }

  return {
    requests,
    currentRequest,
    loading,
    error,
    paymentUrl,
    fetchRequests,
    createRequest,
    payRequest,
    updateRequestStatus
  };
}); 