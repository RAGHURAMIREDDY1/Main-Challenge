"use client"
import { motion, AnimatePresence } from "framer-motion"
import { TripIntakeForm } from "@/components/features/TripIntakeForm"
import OperationsFeed from "@/components/features/OperationsFeed"
import { useTripStore } from "@/hooks/useTripState"
import { TripAPI } from "@/services/api"
import { GlassCard } from "@/components/ui/GlassCard"
import { CloudRain, AlertCircle, RefreshCcw } from "lucide-react"

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
    totalBudget
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
    <div className="min-h-screen flex flex-col items-center px-4 py-20 relative overflow-x-hidden">
      {/* Background Decor */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[600px] bg-blue-500/10 blur-[120px] pointer-events-none rounded-full" />
      
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-6xl z-10"
      >
        <div className="text-center mb-12 space-y-4">
          <h1 className="text-5xl md:text-8xl font-black tracking-tighter bg-clip-text text-transparent bg-gradient-to-b from-white to-white/30 leading-none mb-4">
            TRAVEL OPS CENTER
          </h1>
          <p className="text-lg md:text-xl text-blue-400/60 max-w-2xl mx-auto font-medium uppercase tracking-[0.2em]">
            Adaptive AI Travel Orchestration Engine
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Main Controls & Itinerary */}
          <div className="lg:col-span-7 space-y-8">
            <GlassCard className="p-8">
              <TripIntakeForm onGenerate={handleGenerate} isGenerating={isGenerating} />
            </GlassCard>

            <AnimatePresence>
              {activities.length > 0 && !isGenerating && (
                <motion.div 
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="space-y-6"
                >
                  <div className="flex items-center justify-between">
                    <h2 className="text-2xl font-bold text-white/90">Managed Itinerary</h2>
                    <div className="flex gap-2">
                      <button 
                        onClick={() => handleSimulateDisruption("Heavy Rainstorm")}
                        className="flex items-center gap-2 px-3 py-1.5 bg-blue-500/10 hover:bg-blue-500/20 border border-blue-500/30 rounded-lg text-xs font-bold text-blue-400 transition-all"
                      >
                        <CloudRain className="w-3.5 h-3.5" /> Simulate Rain
                      </button>
                      <button 
                        onClick={() => handleSimulateDisruption("Local Transit Strike")}
                        className="flex items-center gap-2 px-3 py-1.5 bg-red-500/10 hover:bg-red-500/20 border border-red-500/30 rounded-lg text-xs font-bold text-red-400 transition-all"
                      >
                        <AlertCircle className="w-3.5 h-3.5" /> Simulate Delay
                      </button>
                    </div>
                  </div>

                  <div className="space-y-3">
                    {activities.map((act, i) => (
                      <GlassCard key={i} className="p-4 flex justify-between items-center group hover:border-blue-500/50 transition-colors">
                        <div>
                          <h3 className="font-bold text-lg text-white/90">{act.name}</h3>
                          <div className="flex items-center gap-2 text-white/40 text-sm">
                            <span className="font-mono text-blue-400/80">{act.start_time} - {act.end_time}</span>
                            <span>•</span>
                            <span className="italic">{act.description || 'Verified via Google Maps'}</span>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-xl font-black text-white/90">${act.estimated_cost}</div>
                          <div className="text-[10px] text-blue-400/60 uppercase font-bold tracking-widest">Estimated</div>
                        </div>
                      </GlassCard>
                    ))}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Operations Feed & Intelligence */}
          <div className="lg:col-span-5 space-y-6">
            <OperationsFeed />
            
            <AnimatePresence>
              {reasoning && !isGenerating && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                >
                  <GlassCard className="p-6 bg-blue-500/5 border-blue-500/20">
                    <h3 className="text-xs font-black text-blue-400 mb-3 uppercase tracking-[0.2em] flex items-center gap-2">
                      <RefreshCcw className="w-3.5 h-3.5" /> Executive Summary
                    </h3>
                    <p className="text-sm text-gray-300 leading-relaxed font-medium italic">
                      "{reasoning}"
                    </p>
                  </GlassCard>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
