import React from 'react';
import { GlassCard } from '../ui/GlassCard';
import { useTripStore } from '@/hooks/useTripState';
import { Activity, Zap, ShieldCheck, TrendingUp, Info } from 'lucide-react';

const OperationsFeed: React.FC = () => {
  const { decisionLog, efficiencyScore, isGenerating } = useTripStore();

  if ((!decisionLog || decisionLog.length === 0) && !isGenerating) return null;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between px-2">
        <h3 className="text-sm font-bold uppercase tracking-wider text-blue-400 flex items-center gap-2">
          <Zap className="w-4 h-4 animate-pulse" />
          Intelligence Operations Feed
        </h3>
        <div className="px-3 py-1 bg-blue-500/20 border border-blue-500/30 rounded-full">
          <span className="text-xs font-mono text-blue-300">Efficiency: {efficiencyScore}%</span>
        </div>
      </div>

      <div className="space-y-3 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">
        {isGenerating && (
          <div className="p-4 rounded-xl border border-dashed border-blue-500/50 bg-blue-500/5 animate-pulse">
            <p className="text-sm text-blue-300 italic">Orchestrating adaptive routes...</p>
          </div>
        )}
        
        {decisionLog.map((entry, idx) => (
          <GlassCard key={idx} className="!p-4 border-l-4 border-l-blue-500">
            <div className="flex justify-between items-start mb-2">
              <span className="px-2 py-0.5 bg-blue-500/20 rounded text-[10px] font-bold text-blue-400 uppercase">
                {entry.action}
              </span>
              <div className="flex items-center gap-1 text-[10px] text-emerald-400 font-mono">
                <ShieldCheck className="w-3 h-3" />
                {Math.round(entry.confidence * 100)}% Confidence
              </div>
            </div>
            
            <p className="text-sm text-gray-200 font-medium mb-2">{entry.rationale}</p>
            
            <div className="grid grid-cols-2 gap-2 mt-3 pt-3 border-t border-white/5">
              <div className="space-y-1">
                <span className="text-[9px] uppercase text-gray-500 flex items-center gap-1">
                  <TrendingUp className="w-3 h-3" /> Impact
                </span>
                <p className="text-xs text-emerald-400 font-bold">{entry.impact}</p>
              </div>
              <div className="space-y-1">
                <span className="text-[9px] uppercase text-gray-500 flex items-center gap-1">
                  <Info className="w-3 h-3" /> Tradeoff
                </span>
                <p className="text-xs text-gray-400 italic">{entry.tradeoff}</p>
              </div>
            </div>
          </GlassCard>
        ))}
      </div>
    </div>
  );
};

export default OperationsFeed;
