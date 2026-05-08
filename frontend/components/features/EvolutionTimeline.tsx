import React from 'react';
import { GlassCard } from '../ui/GlassCard';
import { History, ArrowRight } from 'lucide-react';
import { Activity } from '@/hooks/useTripState';

interface Props {
  history: Activity[][];
}

const EvolutionTimeline: React.FC<Props> = ({ history }) => {
  if (history.length < 1) return null;

  return (
    <div className="space-y-4">
      <h3 className="text-xs font-bold uppercase tracking-[0.3em] text-blue-400 flex items-center gap-2">
        <History className="w-4 h-4" />
        Itinerary Evolution
      </h3>
      
      <div className="flex items-center gap-4 overflow-x-auto pb-4 custom-scrollbar">
        {history.map((version, idx) => (
          <React.Fragment key={idx}>
            <GlassCard className="min-w-[200px] !p-3 opacity-60 hover:opacity-100 transition-opacity cursor-pointer">
              <p className="text-[10px] font-mono text-gray-500 mb-2">Step {idx + 1}: {idx === 0 ? 'AI Draft' : 'Optimized Plan'}</p>
              <div className="space-y-1">
                {version.slice(0, 2).map((act, i) => (
                  <div key={i} className="text-[10px] text-white/70 truncate">• {act.name}</div>
                ))}
                {version.length > 2 && <div className="text-[9px] text-gray-600">+{version.length - 2} more...</div>}
              </div>
            </GlassCard>
            {idx < history.length - 1 && <ArrowRight className="w-4 h-4 text-gray-700 shrink-0" />}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};

export default EvolutionTimeline;
