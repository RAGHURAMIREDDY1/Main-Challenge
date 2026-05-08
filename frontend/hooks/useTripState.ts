import { create } from 'zustand'

interface Activity {
  id: string;
  name: string;
  startTime: string;
  endTime: string;
  cost: number;
}

interface TripState {
  destination: string | null;
  activities: Activity[];
  totalBudget: number;
  currentCost: number;
  isGenerating: boolean;
  reasoning: string | null;
  setDestination: (dest: string) => void;
  setGenerating: (status: boolean) => void;
  updateActivities: (activities: Activity[], reasoning?: string) => void;
}

export const useTripStore = create<TripState>((set) => ({
  destination: null,
  activities: [],
  totalBudget: 2000,
  currentCost: 0,
  isGenerating: false,
  reasoning: null,
  setDestination: (dest) => set({ destination: dest }),
  setGenerating: (status) => set({ isGenerating: status }),
  updateActivities: (activities, reasoning) => set({ 
    activities,
    reasoning: reasoning || null,
    currentCost: activities.reduce((sum, act) => sum + act.cost, 0)
  }),
}));
