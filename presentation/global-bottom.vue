<template>
  <footer
    v-if="$nav.currentLayout !== 'cover' && $nav.currentLayout !== 'end'"
    class="absolute bottom-0 left-0 right-0 px-8 py-2 flex justify-between items-center text-[11px] text-slate-500 bg-white/90 border-t border-blue-100 pointer-events-none z-10"
  >
    <div class="flex items-center gap-2 font-mono font-semibold text-blue-900">
      <span class="w-2 h-2 rounded-full bg-blue-600"></span>
      <span>AUCC 2026 • Smart Money Concepts (SMC) Market Structure Analysis &amp; Visualization Tool</span>
    </div>
    <div class="font-mono font-bold text-blue-700">
      Slide {{ $nav.currentPage }} / {{ $nav.total }}
    </div>
  </footer>
</template>
