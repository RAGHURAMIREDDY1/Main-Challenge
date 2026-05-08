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
  setDestination: (dest: string) => void;
  setGenerating: (status: boolean) => void;
  updateActivities: (activities: Activity[]) => void;
}

export const useTripStore = create<TripState>((set) => ({
  destination: null,
  activities: [],
  totalBudget: 2000,
  currentCost: 0,
  isGenerating: false,
  setDestination: (dest) => set({ destination: dest }),
  setGenerating: (status) => set({ isGenerating: status }),
  updateActivities: (activities) => set({ 
    activities,
    currentCost: activities.reduce((sum, act) => sum + act.cost, 0)
  }),
}));
