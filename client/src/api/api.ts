import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (username: string, password: string) => 
    api.post('token/', { username, password }),
  
  register: (data: {
    username: string,
    password: string,
    email: string,
    name: string,
    city: string,
    phone: string
  }) => api.post('register/', data),
  
  getProfile: () => api.get('profile/'),
  
  updateProfile: (data: {
    name?: string,
    city?: string,
    phone?: string
  }) => api.patch('profile/', data),
};

export const tracksAPI = {
  getTracks: (venueId: number, params?: { genre?: number, search?: string }) => 
    api.get(`venue/${venueId}/tracks/`, { params }),
  
  addTrack: (venueId: number, data: {
    title: string,
    genre_id: number,
    icon: string,
    artist: string,
    price: number
  }) => api.post(`venue/${venueId}/tracks/`, data),
  
  getTrack: (venueId: number, trackId: number) => 
    api.get(`venue/${venueId}/tracks/${trackId}/`),
  
  updateTrack: (venueId: number, trackId: number, data: {
    title?: string,
    genre_id?: number,
    icon: string,
    artist?: string,
    price?: number
  }) => api.patch(`venue/${venueId}/tracks/${trackId}/`, data),
  
  deleteTrack: (venueId: number, trackId: number) => 
    api.delete(`venue/${venueId}/tracks/${trackId}/`),
};

export const requestsAPI = {
  createRequest: (venueId: number, data: {
    track: number,
    user_fee: number
  }) => api.post(`venue/${venueId}/request/`, data),
  
  payRequest: (paymentToken: string, amount: number) => 
    api.post(`requests/pay/${paymentToken}/`, { amount }),
  
  getRequests: () => api.get('requests/'),
  
  updateRequestStatus: (requestId: number, status: 'pending' | 'accepted' | 'rejected') => 
    api.patch(`requests/${requestId}/`, { status }),
};

export const withdrawalsAPI = {
  createWithdrawal: (data: {
    amount: number,
    card_number: string,
    card_expiry_year: string,
    card_expiry_month: string,
    card_csc: string
  }) => api.post('withdrawals/', data),
  
  getWithdrawalsHistory: () => api.get('withdrawals/history/'),
};

export const withdrawalsMockAPI = {
  createWithdrawal: (data: {
    amount: number,
  }) => api.post('mock-withdraw/', data),
};

export const genresAPI = {
  getGenres: () => api.get('genres/'),
  
  createGenre: (name: string) => api.post('genres/', { name }),
};

export const transactionsAPI = {
  getTransactions: () => api.get('transactions/'),
}; 