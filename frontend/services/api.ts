const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const TripAPI = {
  async generate(destination: string, days: number, budget: number) {
    const res = await fetch(`${API_BASE}/trips/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        destination, 
        start_date: new Date().toISOString().split('T')[0],
        end_date: new Date(Date.now() + days * 86400000).toISOString().split('T')[0],
        budget_usd: budget 
      })
    });
    
    if (!res.ok) throw new Error('Failed to generate trip');
    return res.json();
  }
};
