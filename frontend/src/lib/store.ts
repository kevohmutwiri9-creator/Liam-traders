import { create } from 'zustand';
import { userAPI } from './api';

interface User {
  id: number;
  email: string;
  full_name: string;
  level: number;
  total_tasks_completed: number;
  quality_score: number;
  available_balance: number;
  pending_balance: number;
  total_earnings: number;
  referral_code?: string;
  referral_earnings?: number;
  total_referrals?: number;
  phone_number?: string;
  bio?: string;
  location?: string;
  date_of_birth?: string;
  is_staff?: boolean;
  is_active?: boolean;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  setAuth: (user: User, token: string) => void;
  logout: () => void;
  updateUser: (user: Partial<User>) => void;
  refreshUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  setAuth: (user, token) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
    set({ user, token, isAuthenticated: true });
  },
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('refresh_token');
    set({ user: null, token: null, isAuthenticated: false });
  },
  updateUser: (updatedUser) => {
    set((state) => ({
      user: state.user ? { ...state.user, ...updatedUser } : null,
    }));
  },
  refreshUser: async () => {
    const { token } = get();
    if (!token) return;
    
    try {
      const res = await userAPI.getProfile();
      const updatedUser = res.data;
      localStorage.setItem('user', JSON.stringify(updatedUser));
      set({ user: updatedUser });
    } catch (error) {
      console.error('Failed to refresh user:', error);
      // Don't logout on refresh failure - could be temporary network issue
    }
  },
}));

// Initialize from localStorage
if (typeof window !== 'undefined') {
  const token = localStorage.getItem('token');
  const userStr = localStorage.getItem('user');
  if (token && userStr) {
    useAuthStore.getState().setAuth(JSON.parse(userStr), token);
  }
  
  // Poll for user updates every 30 seconds
  setInterval(() => {
    const { isAuthenticated, refreshUser } = useAuthStore.getState();
    if (isAuthenticated) {
      refreshUser();
    }
  }, 30000);
}
