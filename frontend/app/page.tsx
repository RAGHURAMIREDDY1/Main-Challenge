"use client"
import { motion, AnimatePresence } from "framer-motion"
import { TripIntakeForm } from "@/components/features/TripIntakeForm"
import { useTripStore } from "@/hooks/useTripState"
import { TripAPI } from "@/services/api"
import { GlassCard } from "@/components/ui/GlassCard"

export default function Home() {
  const { isGenerating, setGenerating, updateActivities, activities, destination, setDestination, reasoning } = useTripStore();

  const handleGenerate = async (dest: string, days: number) => {
    setGenerating(true);
    setDestination(dest);
    try {
      const response = await TripAPI.generate(dest, days, 2000);
      updateActivities(response.activities.map((act: any, i: number) => ({
        id: String(i),
        name: act.name,
        startTime: act.start_time,
        endTime: act.end_time,
        cost: act.estimated_cost
      })), response.ai_reasoning);
    } catch (error) {
      console.error("Failed to generate trip:", error);
      alert("Failed to connect to the AI Orchestrator Backend. Is it running on port 8000?");
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col items-center justify-center px-4 py-20 relative">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="w-full max-w-3xl space-y-8"
      >
        <div className="text-center space-y-4">
          <h1 className="text-5xl md:text-7xl font-bold tracking-tighter bg-clip-text text-transparent bg-gradient-to-b from-white to-white/40">
            Orchestrate Your Escape.
          </h1>
          <p className="text-lg md:text-xl text-white/50 max-w-xl mx-auto font-light">
            AI-native travel planning that adapts in real-time. Where to next?
          </p>
        </div>

        <TripIntakeForm onGenerate={handleGenerate} isGenerating={isGenerating} />

        {/* Display results beautifully when ready */}
        <AnimatePresence>
          {activities.length > 0 && !isGenerating && (
            <motion.div 
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              className="mt-12 space-y-4"
            >
              <h2 className="text-2xl font-semibold text-white/90">Your {destination} Itinerary</h2>
              
              {reasoning && (
                <GlassCard className="p-4 mb-6 border-accent-violet/30 bg-accent-violet/5">
                  <h3 className="text-xs font-semibold text-accent-violet mb-2 uppercase tracking-wider flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-accent-violet animate-pulse" />
                    Gemini Reasoning & Maps Context
                  </h3>
                  <p className="text-white/70 text-sm leading-relaxed italic">"{reasoning}"</p>
                </GlassCard>
              )}

              <div className="grid gap-4">
                {activities.map((act) => (
                  <GlassCard key={act.id} className="p-4 flex justify-between items-center">
                    <div>
                      <h3 className="font-medium text-lg text-white/90">{act.name}</h3>
                      <p className="text-white/50 text-sm">{act.startTime} - {act.endTime}</p>
                    </div>
                    <div className="text-accent-cyan font-semibold">
                      ${act.cost}
                    </div>
                  </GlassCard>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <div className="flex flex-wrap justify-center gap-4 text-sm text-white/40 pt-8">
          <span className="px-3 py-1 rounded-full border border-white/10 bg-white/5 cursor-pointer hover:bg-white/10 hover:text-white transition-colors">Weekend in Paris</span>
          <span className="px-3 py-1 rounded-full border border-white/10 bg-white/5 cursor-pointer hover:bg-white/10 hover:text-white transition-colors">Tech tour in SF</span>
          <span className="px-3 py-1 rounded-full border border-white/10 bg-white/5 cursor-pointer hover:bg-white/10 hover:text-white transition-colors">Foodie trip to Rome</span>
        </div>
      </motion.div>
    </div>
  );
}
