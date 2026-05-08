"use client"
import { motion, AnimatePresence } from "framer-motion"
import { TripIntakeForm } from "@/components/features/TripIntakeForm"
import OperationsFeed from "@/components/features/OperationsFeed"
import DecisionEngineCard from "@/components/features/DecisionEngineCard"
import EvolutionTimeline from "@/components/features/EvolutionTimeline"
import OptimizationSummary from "@/components/features/OptimizationSummary"
import { useTripStore } from "@/hooks/useTripState"
import { TripAPI } from "@/services/api"
import { GlassCard } from "@/components/ui/GlassCard"
import { CloudRain, AlertCircle, RefreshCcw, MapPin, Zap } from "lucide-react"

export default function Home() {
  const { 
    isGenerating, 
    setGenerating, 
    updateTrip, 
    activities, 
    destination, 
    setDestination, 
    reasoning,
    tripId,
    totalBudget,
    efficiencyScore,
    evolutionHistory
  } = useTripStore();

  const handleGenerate = async (dest: string, days: number) => {
    setGenerating(true);
    setDestination(dest);
    try {
      const response = await TripAPI.generate(dest, days, totalBudget);
      updateTrip(response);
    } catch (error) {
      console.error("Failed to generate trip:", error);
      alert("AI Orchestrator Link Error. Ensure Backend is live.");
    } finally {
      setGenerating(false);
    }
  };

  const handleSimulateDisruption = async (event: string) => {
    if (!tripId) return;
    setGenerating(true);
    try {
      const response = await TripAPI.adapt(tripId, event, activities, destination || "", totalBudget);
      updateTrip(response);
    } catch (error) {
      console.error("Adaptation failed:", error);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#050505] text-white selection:bg-blue-500/30 font-sans">
      {/* Dynamic Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-600/10 blur-[120px] rounded-full animate-pulse" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-indigo-600/10 blur-[120px] rounded-full animate-pulse delay-1000" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-6 py-12">
        <header className="flex flex-col md:flex-row justify-between items-end mb-16 gap-6">
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-blue-400 font-black text-xs tracking-[0.4em] uppercase mb-2">
              <Zap className="w-4 h-4 fill-current" /> System Online
            </div>
            <h1 className="text-6xl md:text-8xl font-black tracking-tighter leading-none uppercase">
              Voyage <span className="text-blue-500">Ops</span>
            </h1>
            <p className="text-gray-500 font-medium tracking-widest uppercase text-xs">AI-Native Travel Orchestration Hub</p>
          </div>
          
          <div className="w-full md:w-auto">
            <TripIntakeForm onGenerate={handleGenerate} isGenerating={isGenerating} />
          </div>
        </header>

        <AnimatePresence>
          {activities.length > 0 && !isGenerating && (
            <motion.div 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              className="grid grid-cols-1 lg:grid-cols-12 gap-10"
            >
              {/* Left Column: Itinerary & Evolution */}
              <div className="lg:col-span-8 space-y-12">
                <section className="space-y-6">
                  <OptimizationSummary activities={activities} efficiencyScore={efficiencyScore} />
                  <EvolutionTimeline history={evolutionHistory} />
                </section>

                <section className="space-y-8">
                  <div className="flex items-center justify-between border-b border-white/5 pb-4">
                    <h2 className="text-3xl font-black uppercase tracking-tight italic">Managed Itinerary</h2>
                    <div className="flex gap-3">
                      <button 
                        onClick={() => handleSimulateDisruption("Heavy Rainstorm")}
                        className="px-4 py-2 bg-blue-500/5 hover:bg-blue-500/10 border border-blue-500/20 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all"
                      >
                        Simulate Rain
                      </button>
                      <button 
                        onClick={() => handleSimulateDisruption("Local Strike")}
                        className="px-4 py-2 bg-rose-500/5 hover:bg-rose-500/10 border border-rose-500/20 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all"
                      >
                        Simulate Delay
                      </button>
                    </div>
                  </div>

                  <div className="space-y-6">
                    {activities.map((act, i) => (
                      <GlassCard key={i} className="p-8 border-white/5 hover:border-blue-500/30 transition-all group">
                        <div className="flex flex-col md:flex-row justify-between gap-6 mb-8">
                          <div className="flex gap-6">
                            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-600/20 to-indigo-600/20 flex items-center justify-center shrink-0 border border-white/5">
                              <MapPin className="w-8 h-8 text-blue-500" />
                            </div>
                            <div>
                              <h3 className="text-3xl font-black text-white mb-2">{act.name}</h3>
                              <div className="flex items-center gap-3">
                                <span className="bg-white/5 px-3 py-1 rounded-full text-xs font-mono text-blue-400 border border-white/5">{act.start_time} — {act.end_time}</span>
                                <span className="text-gray-600 text-xs uppercase font-bold tracking-widest">G-Ecosystem Verified</span>
                              </div>
                            </div>
                          </div>
                          <div className="md:text-right flex md:flex-col justify-between items-end">
                            <div className="text-4xl font-black text-white">${act.estimated_cost}</div>
                            <div className="text-[10px] text-gray-500 font-bold uppercase tracking-[0.2em]">Live Est. Cost</div>
                          </div>
                        </div>

                        <DecisionEngineCard activity={act} />
                      </GlassCard>
                    ))}
                  </div>
                </section>
              </div>

              {/* Right Column: Operations Sidebar */}
              <div className="lg:col-span-4 space-y-8">
                <div className="sticky top-12 space-y-8">
                  <div className="p-1 bg-gradient-to-br from-blue-600/20 to-transparent rounded-[2rem]">
                    <GlassCard className="!bg-[#0a0a0a] !p-8 border-white/5">
                      <OperationsFeed />
                    </GlassCard>
                  </div>

                  <GlassCard className="p-8 border-blue-500/10 bg-blue-500/5">
                    <h4 className="text-[10px] font-black text-blue-500 uppercase tracking-[0.3em] mb-4 flex items-center gap-2">
                      <RefreshCcw className="w-4 h-4" /> Operational Summary
                    </h4>
                    <p className="text-sm text-gray-400 font-medium italic leading-relaxed">
                      "{reasoning}"
                    </p>
                  </GlassCard>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
