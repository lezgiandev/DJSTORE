export interface Genre {
  id: number;
  name: string;
}

export interface Track {
  id: number;
  title: string;
  icon: string;
  genre: Genre;
  artist: string;
  price: number;
}

export interface TrackRequest {
  id: number;
  payment_url: string;
  track: Track;
  user_fee: number;
  min_fee: number;
  status: 'pending' | 'accepted' | 'rejected';
  is_paid: boolean;
  payment_token: string;
  created_at: string;
}

export interface VenueProfile {
  id: number;
  name: string;
  city: string;
  phone: string;
  qr_code: string;
  balance: number;
}

export interface Transaction {
  id: number;
  amount: number;
  transaction_type: string;
  created_at: string;
}

export interface Withdrawal {
  id: number;
  amount: number;
  bank_card_token: string;
  fee: number;
  status: 'pending' | 'processing' | 'succeeded' | 'canceled' | 'failed';
  yookassa_payout_id: string;
  created_at: string;
}

export interface AuthResponse {
  access: string;
  refresh: string;
}

export interface UserState {
  isAuthenticated: boolean;
  profile: VenueProfile | null;
}

export interface TrackParams {
  genre?: number;
  search?: string;
}

export interface RegisterData {
  username: string;
  password: string;
  email: string;
  name: string;
  city: string;
  phone: string;
} 