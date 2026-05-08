import { HTMLAttributes, forwardRef } from "react"
import { twMerge } from "tailwind-merge"
import { clsx, type ClassValue } from "clsx"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

interface GlassCardProps extends HTMLAttributes<HTMLDivElement> {
  hoverEffect?: boolean;
}

export const GlassCard = forwardRef<HTMLDivElement, GlassCardProps>(
  ({ className, hoverEffect = false, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          "glass-panel transition-all duration-300",
          hoverEffect && "hover:bg-white/[0.05] hover:border-white/20 hover:scale-[1.01] hover:shadow-[0_0_30px_rgba(138,43,226,0.1)]",
          className
        )}
        {...props}
      />
    )
  }
)
GlassCard.displayName = "GlassCard"
