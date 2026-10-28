import { defineConfig } from 'unocss'

export default defineConfig({
  shortcuts: {
    'bw-card': 'bg-white border-2 border-blue-200 rounded-2xl shadow-sm p-4',
    'bw-card-navy': 'bg-slate-900 text-white border-2 border-blue-600 rounded-2xl shadow-md p-4',
    'bw-card-soft': 'bg-blue-50/80 border border-blue-300 rounded-xl p-3.5',
    'bw-badge': 'inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full text-xs font-mono font-bold uppercase tracking-wider bg-blue-100 text-blue-800 border border-blue-300',
    'bw-badge-dark': 'inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full text-xs font-mono font-bold uppercase tracking-wider bg-slate-900 text-blue-200 border border-blue-500',
    'bw-title': 'text-2xl font-extrabold tracking-tight text-slate-900',
    'bw-kpi': 'text-4xl font-extrabold tracking-tight text-blue-700',
  },
})
