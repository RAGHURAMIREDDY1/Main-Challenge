import { create } from 'zustand'

interface Activity {
  name: string;
  start_time: string;
  end_time: string;
  estimated_cost: number;
  description?: string;
}

interface DecisionLogEntry {
  action: string;
  rationale: string;
  confidence: number;
  tradeoff: string;
  impact: string;
}

interface TripState {
  tripId: string | null;
  destination: string | null;
  activities: Activity[];
  totalBudget: number;
  currentCost: number;
  isGenerating: boolean;
  reasoning: string | null;
  decisionLog: DecisionLogEntry[];
  efficiencyScore: number;
  setDestination: (dest: string) => void;
  setGenerating: (status: boolean) => void;
  updateTrip: (data: { 
    trip_id: string, 
    activities: Activity[], 
    ai_reasoning: string, 
    decision_log: DecisionLogEntry[],
    efficiency_score: number 
  }) => void;
}

export const useTripStore = create<TripState>((set) => ({
  tripId: null,
  destination: null,
  activities: [],
  totalBudget: 2000,
  currentCost: 0,
  isGenerating: false,
  reasoning: null,
  decisionLog: [],
  efficiencyScore: 0,
  setDestination: (dest) => set({ destination: dest }),
  setGenerating: (status) => set({ isGenerating: status }),
  updateTrip: (data) => set({ 
    tripId: data.trip_id,
    activities: data.activities,
    reasoning: data.ai_reasoning,
    decisionLog: data.decision_log,
    efficiencyScore: data.efficiency_score,
    currentCost: data.activities.reduce((sum, act) => sum + act.estimated_cost, 0)
  }),
}));
