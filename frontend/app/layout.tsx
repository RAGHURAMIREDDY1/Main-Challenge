import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "AI Travel Copilot | Premium Orchestration",
  description: "Dynamic AI-powered trip planning and orchestration platform.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.variable} min-h-screen flex flex-col bg-background overflow-x-hidden selection:bg-accent-violet/30`}>
        <div className="absolute inset-0 bg-hero-glow pointer-events-none -z-10" />
        <nav className="w-full border-b border-border bg-background/50 backdrop-blur-md sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded-full bg-gradient-to-tr from-accent-violet to-accent-cyan animate-pulse shadow-[0_0_15px_rgba(138,43,226,0.5)]" />
              <span className="font-semibold tracking-tight text-lg">Voyage.ai</span>
            </div>
            <div className="text-sm text-white/50 hover:text-white transition-colors cursor-pointer">
              Sign In
            </div>
          </div>
        </nav>
        <main className="flex-1 flex flex-col">
          {children}
        </main>
      </body>
    </html>
  );
}
