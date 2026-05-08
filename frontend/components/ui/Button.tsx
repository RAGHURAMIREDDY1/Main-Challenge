import { ButtonHTMLAttributes, forwardRef } from "react"
import { cn } from "./GlassCard"

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  isLoading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', isLoading, children, disabled, ...props }, ref) => {
    const variants = {
      primary: "bg-white text-black hover:bg-white/90 shadow-[0_0_20px_rgba(255,255,255,0.2)]",
      secondary: "bg-white/10 text-white hover:bg-white/20 border border-white/10",
      ghost: "bg-transparent text-white/70 hover:text-white hover:bg-white/5"
    }

    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={cn(
          "relative px-6 py-3 rounded-xl font-medium transition-all duration-300 flex items-center justify-center gap-2 overflow-hidden",
          "disabled:opacity-50 disabled:cursor-not-allowed",
          variants[variant],
          className
        )}
        {...props}
      >
        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center bg-inherit z-10">
            <div className="w-5 h-5 border-2 border-current border-t-transparent rounded-full animate-spin" />
          </div>
        )}
        <span className={cn(isLoading && "opacity-0")}>{children}</span>
      </button>
    )
  }
)
Button.displayName = "Button"
