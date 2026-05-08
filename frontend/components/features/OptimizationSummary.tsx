import React from 'react';
import { GlassCard } from '../ui/GlassCard';
import { Activity } from '@/hooks/useTripState';
import { Timer, Banknote, Map, ShieldCheck } from 'lucide-react';

interface Props {
  activities: Activity[];
  efficiencyScore: number;
}

const OptimizationSummary: React.FC<Props> = ({ activities, efficiencyScore }) => {
  const totalCost = activities.reduce((sum, a) => sum + a.estimated_cost, 0);
  
  const metrics = [
    { label: 'System Confidence', val: '98%', icon: ShieldCheck, color: 'text-emerald-400' },
    { label: 'Route Efficiency', val: `${efficiencyScore}%`, icon: Map, color: 'text-blue-400' },
    { label: 'Travel Time', val: 'Optimized', icon: Timer, color: 'text-amber-400' },
    { label: 'Total Budget', val: `$${totalCost}`, icon: Banknote, color: 'text-emerald-400' },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {metrics.map((m) => (
        <GlassCard key={m.label} className="!p-4 flex flex-col items-center text-center space-y-2">
          <m.icon className={`w-5 h-5 ${m.color}`} />
          <div>
            <div className="text-xl font-black text-white">{m.val}</div>
            <div className="text-[9px] uppercase tracking-tighter text-gray-500 font-bold">{m.label}</div>
          </div>
        </GlassCard>
      ))}
    </div>
  );
};

export default OptimizationSummary;
