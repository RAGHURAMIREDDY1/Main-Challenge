import { useState } from "react"
import { GlassCard } from "@/components/ui/GlassCard"
import { Button } from "@/components/ui/Button"
import { MapPin, Calendar } from "lucide-react"

interface TripIntakeFormProps {
  onGenerate: (destination: string, days: number) => void;
  isGenerating: boolean;
}

export function TripIntakeForm({ onGenerate, isGenerating }: TripIntakeFormProps) {
  const [destination, setDestination] = useState("");
  const [days, setDays] = useState("3");

  return (
    <GlassCard className="p-2 flex flex-col md:flex-row gap-2 w-full">
      <div className="flex-1 flex items-center gap-3 px-4 py-2 bg-black/20 rounded-xl">
        <MapPin className="w-5 h-5 text-accent-cyan" />
        <input 
          type="text" 
          value={destination}
          onChange={(e) => setDestination(e.target.value)}
          placeholder="e.g. Tokyo, Japan" 
          className="bg-transparent border-none outline-none w-full text-white placeholder:text-white/30"
        />
      </div>
      
      <div className="w-full md:w-[1px] h-[1px] md:h-12 bg-border my-2 md:my-0" />
      
      <div className="flex-1 flex items-center gap-3 px-4 py-2 bg-black/20 rounded-xl">
        <Calendar className="w-5 h-5 text-accent-violet" />
        <input 
          type="number" 
          value={days}
          onChange={(e) => setDays(e.target.value)}
          placeholder="3 days" 
          className="bg-transparent border-none outline-none w-full text-white placeholder:text-white/30"
        />
      </div>

      <Button 
        className="w-full md:w-auto" 
        onClick={() => onGenerate(destination || "Paris", parseInt(days) || 3)}
        isLoading={isGenerating}
      >
        Generate Trip
      </Button>
    </GlassCard>
  )
}
