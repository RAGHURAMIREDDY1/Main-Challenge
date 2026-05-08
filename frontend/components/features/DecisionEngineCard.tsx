import React from 'react';
import { Activity } from '@/hooks/useTripState';
import { BarChart3, Brain, Compass, Clock, XCircle, CheckCircle2 } from 'lucide-react';

interface Props {
  activity: Activity;
}

const DecisionEngineCard: React.FC<Props> = ({ activity }) => {
  const scores = [
    { label: 'AI Confidence', val: activity.scores.confidence, color: 'bg-blue-500' },
    { label: 'Budget Fit', val: activity.scores.budget_fit, color: 'bg-emerald-500' },
    { label: 'Weather Suitability', val: activity.scores.weather_suitability, color: 'bg-amber-500' },
    { label: 'Efficiency', val: activity.scores.efficiency, color: 'bg-indigo-500' },
    { label: 'Preference Match', val: activity.scores.preference_match, color: 'bg-rose-500' },
  ];

  return (
    <div className="mt-4 pt-4 border-t border-white/10 space-y-4">
      {/* Scores Grid */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
        {scores.map((s) => (
          <div key={s.label} className="space-y-1">
            <div className="flex justify-between text-[9px] uppercase tracking-wider text-white/40">
              <span>{s.label}</span>
              <span>{Math.round(s.val * 100)}%</span>
            </div>
            <div className="h-1 w-full bg-white/10 rounded-full overflow-hidden">
              <div 
                className={`h-full ${s.color} transition-all duration-1000`} 
                style={{ width: `${s.val * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>

      {/* Rationale Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-white/5 p-4 rounded-xl border border-white/5">
        <div className="space-y-3">
          <div className="flex gap-2 items-start">
            <Brain className="w-4 h-4 text-blue-400 mt-1 shrink-0" />
            <div>
              <p className="text-[10px] uppercase font-bold text-blue-400/80">Selection Rationale</p>
              <p className="text-xs text-gray-300 leading-relaxed">{activity.rationale.selection_why}</p>
            </div>
          </div>
          <div className="flex gap-2 items-start">
            <Compass className="w-4 h-4 text-emerald-400 mt-1 shrink-0" />
            <div>
              <p className="text-[10px] uppercase font-bold text-emerald-400/80">Optimization Logic</p>
              <p className="text-xs text-gray-300 leading-relaxed">{activity.rationale.optimization_logic}</p>
            </div>
          </div>
        </div>
        
        <div className="space-y-3">
          <div className="flex gap-2 items-start">
            <XCircle className="w-4 h-4 text-rose-400 mt-1 shrink-0" />
            <div>
              <p className="text-[10px] uppercase font-bold text-rose-400/80">Alternatives Rejected</p>
              <p className="text-xs text-gray-300 leading-relaxed italic">{activity.rationale.alternatives_rejected}</p>
            </div>
          </div>
          <div className="flex gap-2 items-start">
            <Clock className="w-4 h-4 text-amber-400 mt-1 shrink-0" />
            <div>
              <p className="text-[10px] uppercase font-bold text-amber-400/80">Timing Rationale</p>
              <p className="text-xs text-gray-300 leading-relaxed">{activity.rationale.timing_rationale}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DecisionEngineCard;
