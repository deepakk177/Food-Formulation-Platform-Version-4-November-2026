import { create } from 'zustand';

export interface User {
  username: string;
  email: string;
  role: string;
}

export interface Project {
  id: string;
  name: string;
  category: string;
  status: string;
  query?: string;
  created_at: string;
  updated_at: string;
  version?: string;
  formulation_id?: string;
}

export interface Ingredient {
  name: string;
  category: string;
  protein: number;
  fat: number;
  carbs: number;
  calories: number;
  functional_role: string;
  allergen: string;
}

interface AppState {
  user: User | null;
  projects: Project[];
  ingredients: Ingredient[];
  token: string | null;
  loading: boolean;
  setUser: (user: User | null) => void;
  setToken: (token: string | null) => void;
  setProjects: (projects: Project[]) => void;
  setIngredients: (ingredients: Ingredient[]) => void;
  fetchProjects: () => Promise<void>;
  fetchIngredients: () => Promise<void>;
  initializeAuth: () => void;
  logout: () => void;
}

export const useStore = create<AppState>((set, get) => ({
  user: null,
  projects: [],
  ingredients: [],
  token: null,
  loading: false,
  setUser: (user) => set({ user }),
  setToken: (token) => {
    if (token) {
      if (typeof window !== 'undefined') {
        localStorage.setItem('tf_token', token);
      }
    } else {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('tf_token');
        localStorage.removeItem('tf_user');
      }
    }
    set({ token });
  },
  setProjects: (projects) => set({ projects }),
  setIngredients: (ingredients) => set({ ingredients }),
  
  initializeAuth: () => {
    if (typeof window !== 'undefined') {
      const storedToken = localStorage.getItem('tf_token');
      const storedUser = localStorage.getItem('tf_user');
      if (storedToken && storedUser) {
        set({ token: storedToken, user: JSON.parse(storedUser) });
      }
    }
  },

  fetchProjects: async () => {
    set({ loading: true });
    try {
      const api_url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${api_url}/api/projects`);
      if (response.ok) {
        const data = await response.json();
        set({ projects: data });
      }
    } catch (err) {
      console.error("Zustand: Failed to fetch projects", err);
    } finally {
      set({ loading: false });
    }
  },

  fetchIngredients: async () => {
    try {
      const api_url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${api_url}/api/ingredients`);
      if (response.ok) {
        const data = await response.json();
        set({ ingredients: data });
      }
    } catch (err) {
      console.error("Zustand: Failed to fetch ingredients", err);
    }
  },

  logout: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('tf_token');
      localStorage.removeItem('tf_user');
    }
    set({ user: null, token: null, projects: [] });
  },
}));
