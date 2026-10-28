---
theme: default
title: เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม Smart Money Concepts (SMC)
info: |
  ## เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม Smart Money Concepts (SMC)
  A Financial Market Structure Analysis and Visualization Tool Using Smart Money Concepts Algorithms
  AUCC 2026 Presentation — Designed by พาร์ค (Slidev Specialist)
aspectRatio: 16/9
canvasWidth: 980
colorSchema: light
transition: slide-left
mdc: true
lineNumbers: true
fonts:
  sans: Sarabun, Inter, sans-serif
  mono: JetBrains Mono, Consolas, monospace
---

<!-- SLIDE 1: COVER (BLUE - WHITE THEME) -->
<div class="h-full w-full flex flex-col justify-between p-8 rounded-3xl bg-gradient-to-br from-white via-blue-50/70 to-blue-100/80 border-2 border-blue-200 shadow-lg relative overflow-hidden">
  <!-- Decorative Blue Accent Shapes -->
  <div class="absolute -top-20 -right-20 w-72 h-72 rounded-full bg-blue-600/10 blur-2xl pointer-events-none"></div>
  <div class="absolute -bottom-24 -left-20 w-80 h-80 rounded-full bg-blue-800/10 blur-2xl pointer-events-none"></div>

  <div class="flex items-center justify-between z-10">
    <span class="bw-badge">AUCC 2026 • RESEARCH PRESENTATION</span>
    <span class="bw-badge-dark">BLUE &amp; WHITE FINTECH EDITION</span>
  </div>

  <div class="my-auto z-10">
    <h1 class="!text-3xl !leading-snug font-extrabold text-slate-900 mb-3">
      เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงิน<br/>
      <span class="text-blue-700">ด้วยอัลกอริทึม Smart Money Concepts (SMC)</span>
    </h1>
    <p class="text-base font-medium text-blue-900/80 font-mono">
      A Financial Market Structure Analysis and Visualization Tool Using Smart Money Concepts Algorithms
    </p>

    <div class="grid grid-cols-4 gap-3 mt-6">
      <div class="bg-white/90 border border-blue-200 rounded-xl p-2.5 text-center shadow-sm">
        <div class="text-xs font-mono text-blue-600 font-bold">MARKET DATA</div>
        <div class="text-sm font-bold text-slate-800">MetaTrader 5 OHLCV</div>
      </div>
      <div class="bg-white/90 border border-blue-200 rounded-xl p-2.5 text-center shadow-sm">
        <div class="text-xs font-mono text-blue-600 font-bold">ALGORITHMS</div>
        <div class="text-sm font-bold text-slate-800">Swing • CHoCH • OB • FVG</div>
      </div>
      <div class="bg-white/90 border border-blue-200 rounded-xl p-2.5 text-center shadow-sm">
        <div class="text-xs font-mono text-blue-600 font-bold">CONFLUENCE</div>
        <div class="text-sm font-bold text-slate-800">7-Timeframe Scoring</div>
      </div>
      <div class="bg-white/90 border border-blue-200 rounded-xl p-2.5 text-center shadow-sm">
        <div class="text-xs font-mono text-blue-600 font-bold">EVALUATION</div>
        <div class="text-sm font-bold text-slate-800">Backtest &amp; User Study</div>
      </div>
    </div>
  </div>

  <div class="flex items-center justify-between pt-4 border-t border-blue-200 text-xs text-slate-700 z-10">
    <div>
      <strong class="text-slate-900">ผู้วิจัย:</strong> นายนวพรหม ภูผาผิว (663450040-2)
    </div>
    <div class="font-semibold text-blue-800">
      หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาวิทยาการคอมพิวเตอร์และสารสนเทศ มหาวิทยาลัยขอนแก่น
    </div>
  </div>
</div>

---
layout: default
---

<!-- SLIDE 2: ความเป็นมาและความสำคัญของปัญหา -->
<div class="mb-2">
  <span class="bw-badge">01 • BACKGROUND &amp; SIGNIFICANCE</span>
  <h1 class="!text-2xl font-extrabold text-slate-900 mt-1">ความเป็นมาและความสำคัญของปัญหา</h1>
</div>

<div class="grid grid-cols-12 gap-4 mt-3">
  <!-- KPI Highlight Box -->
  <div class="col-span-4 bw-card-navy flex flex-col justify-between">
    <div>
      <div class="text-xs font-mono uppercase tracking-wider text-blue-300">สถิติจาก ESMA (European Securities)</div>
      <div class="text-5xl font-extrabold text-white my-3">60%–80%</div>
      <div class="text-sm font-semibold text-blue-100 leading-relaxed">
        ของเทรดเดอร์รายย่อยสูญเสียเงินทุนจากการขาดเครื่องมือวิเคราะห์โครงสร้างตลาดเชิงลึกและการใช้อารมณ์ตัดสินใจ
      </div>
    </div>
    <div class="mt-4 pt-3 border-t border-blue-700/60 text-xs text-blue-200 font-mono">
      Retail Trader Loss Rate in Leveraged Financial Markets
    </div>
  </div>

  <!-- 3 Problem & Solution Cards -->
  <div class="col-span-8 grid grid-cols-1 gap-3">
    <div class="bw-card flex items-start gap-3">
      <div class="w-9 h-9 rounded-lg bg-blue-700 text-white font-mono font-bold flex items-center justify-center shrink-0">1</div>
      <div>
        <h3 class="text-base font-bold text-slate-900">ข้อจำกัดของอินดิเคเตอร์พื้นฐาน (Lagging Indicators)</h3>
        <p class="text-xs text-slate-600 leading-relaxed mt-0.5">
          เครื่องมือทั่วไปอย่าง Moving Average หรือ RSI คำนวณจากค่าเฉลี่ยย้อนหลัง ทำให้เกิดความล่าช้า (Lag) และไม่สามารถระบุร่องรอยคำสั่งซื้อขายของสถาบันการเงินขนาดใหญ่ (Institutional Footprint) ได้
        </p>
      </div>
    </div>

    <div class="bw-card flex items-start gap-3">
      <div class="w-9 h-9 rounded-lg bg-blue-600 text-white font-mono font-bold flex items-center justify-center shrink-0">2</div>
      <div>
        <h3 class="text-base font-bold text-slate-900">อคติและความล่าช้าจากการตีกราฟ SMC ด้วยมือ (Manual &amp; Subjective Bias)</h3>
        <p class="text-xs text-slate-600 leading-relaxed mt-0.5">
          การหาจุด Swing High/Low, BOS, CHoCH, Order Block และ FVG ด้วยสายตาใช้เวลานาน ตีความไม่ตรงกันในแต่ละบุคคล และไม่สามารถเฝ้าติดตามพร้อมกันทั้ง 7 กรอบเวลา (W1 ถึง M5) ได้อย่างต่อเนื่อง
        </p>
      </div>
    </div>

    <div class="bw-card-soft flex items-start gap-3 border-2 border-blue-500">
      <div class="w-9 h-9 rounded-lg bg-slate-900 text-white font-mono font-bold flex items-center justify-center shrink-0">3</div>
      <div>
        <h3 class="text-base font-bold text-blue-900">แนวทางการแก้ปัญหาด้วยอัลกอริทึมเชิงวิศวกรรม (Algorithmic SMC Engine)</h3>
        <p class="text-xs text-slate-700 leading-relaxed mt-0.5">
          แปลงนิยามทฤษฎี SMC ให้เป็นสมการคณิตศาสตร์และ Finite State Machine ที่แม่นยำ 100% วาดโซนราคาอัตโนมัติบนกราฟอินเทอร์แอคทีฟ พร้อมระบบให้คะแนนพหุกรอบเวลาและจำลอง Backtest ย้อนหลัง
        </p>
      </div>
    </div>
  </div>
</div>

---
layout: default
---

<!-- SLIDE 3: วัตถุประสงค์ของโครงการ -->
<div class="mb-3">
  <span class="bw-badge">02 • PROJECT OBJECTIVES</span>
  <h1 class="!text-2xl font-extrabold text-slate-900 mt-1">วัตถุประสงค์ของโครงการวิจัย</h1>
</div>

<div class="grid grid-cols-2 gap-6 mt-4">
  <!-- Objective 1 -->
  <div class="bw-card border-t-8 border-t-blue-700 flex flex-col justify-between p-5">
    <div>
      <div class="flex items-center justify-between mb-3">
        <span class="px-3 py-1 rounded-lg bg-blue-700 text-white font-mono text-xs font-bold">OBJECTIVE 01</span>
        <span class="text-xs font-mono text-blue-700 font-bold">Interactive Visualization</span>
      </div>
      <h2 class="text-lg font-extrabold text-slate-900 mb-2 leading-snug">
        ออกแบบและพัฒนาเว็บแอปพลิเคชันแสดงกราฟแท่งเทียนและโครงสร้างตลาดแบบอินเทอร์แอคทีฟ
      </h2>
      <p class="text-xs text-slate-600 leading-relaxed mb-4">
        พัฒนาระบบที่สามารถดึงข้อมูลราคาจาก MetaTrader 5 มาคำนวณและวาดองค์ประกอบตามทฤษฎี Smart Money Concepts บนกราฟได้อย่างอัตโนมัติและแม่นยำ:
      </p>
      <div class="grid grid-cols-2 gap-2 text-xs">
        <div class="p-2 rounded-lg bg-blue-50 border border-blue-200 font-semibold text-blue-900">✔ Swing High / Swing Low</div>
        <div class="p-2 rounded-lg bg-blue-50 border border-blue-200 font-semibold text-blue-900">✔ BOS &amp; CHoCH Structure</div>
        <div class="p-2 rounded-lg bg-blue-50 border border-blue-200 font-semibold text-blue-900">✔ Order Blocks (OB + ATR)</div>
        <div class="p-2 rounded-lg bg-blue-50 border border-blue-200 font-semibold text-blue-900">✔ Fair Value Gap (FVG)</div>
        <div class="p-2 rounded-lg bg-blue-50 border border-blue-200 font-semibold text-blue-900">✔ Liquidity (EQH / EQL)</div>
        <div class="p-2 rounded-lg bg-blue-50 border border-blue-200 font-semibold text-blue-900">✔ Premium / Discount Zone</div>
      </div>
    </div>
  </div>

  <!-- Objective 2 -->
  <div class="bw-card border-t-8 border-t-slate-900 flex flex-col justify-between p-5">
    <div>
      <div class="flex items-center justify-between mb-3">
        <span class="px-3 py-1 rounded-lg bg-slate-900 text-white font-mono text-xs font-bold">OBJECTIVE 02</span>
        <span class="text-xs font-mono text-slate-800 font-bold">Multi-TF Scanner &amp; Backtest</span>
      </div>
      <h2 class="text-lg font-extrabold text-slate-900 mb-2 leading-snug">
        พัฒนาระบบสแกนแนวโน้มพหุกรอบเวลาและระบบทดสอบย้อนหลังอัตโนมัติ (Backtesting)
      </h2>
      <p class="text-xs text-slate-600 leading-relaxed mb-4">
        สร้างเครื่องมือช่วยตัดสินใจเชิงปริมาณที่สังเคราะห์แนวโน้มจากหลายกรอบเวลาพร้อมกัน และจำลองการซื้อขายย้อนหลังเพื่อวัดผลทางสถิติ:
      </p>
      <div class="space-y-2 text-xs">
        <div class="p-2.5 rounded-lg bg-slate-50 border border-blue-200">
          <strong class="text-blue-900">• Multi-Timeframe Confluence (7 TFs):</strong> คำนวณคะแนนถ่วงน้ำหนักตั้งแต่ W1, D1, H4, H1, M30, M15 ถึง M5 เพื่อสรุปสัญญาณ Strong BUY / SELL
        </div>
        <div class="p-2.5 rounded-lg bg-slate-50 border border-blue-200">
          <strong class="text-blue-900">• H4 SMC Setup Radar:</strong> เรดาร์ตรวจจับระยะห่างราคาปัจจุบันกับโซน OB และ FVG ที่ยังไม่ถูกทำลาย (Unmitigated)
        </div>
        <div class="p-2.5 rounded-lg bg-slate-50 border border-blue-200">
          <strong class="text-blue-900">• Automated Backtesting Engine:</strong> จำลองเข้าออเดอร์ตามโซน SMC พร้อมคำนวณ Win Rate, Profit Factor, Max Drawdown และ Equity Curve
        </div>
      </div>
    </div>
  </div>
</div>

---
layout: default
---

<!-- SLIDE 4: ขอบเขตของงาน (SCOPE OF WORK) -->
<div class="mb-2">
  <span class="bw-badge">03 • SCOPE OF WORK</span>
  <h1 class="!text-2xl font-extrabold text-slate-900 mt-1">ขอบเขตของงานวิจัย (Scope of Work)</h1>
</div>

<div class="grid grid-cols-2 gap-3.5 mt-3">
  <div class="bw-card">
    <div class="flex items-center gap-2 mb-2">
      <span class="px-2.5 py-0.5 rounded bg-blue-700 text-white font-mono text-xs font-bold">SCOPE 1</span>
      <h3 class="text-sm font-extrabold text-slate-900">ขอบเขตด้านข้อมูลและกรอบเวลา (Data &amp; Timeframes)</h3>
    </div>
    <ul class="text-xs text-slate-700 space-y-1.5 leading-relaxed">
      <li>• เชื่อมต่อข้อมูลราคา OHLCV จากโปรแกรม <strong>MetaTrader 5 (MT5)</strong></li>
      <li>• รองรับการวิเคราะห์คู่เงินหลักและทองคำ เช่น <code class="text-blue-700 font-bold">XAUUSD</code>, <code class="text-blue-700 font-bold">EURUSD</code>, <code class="text-blue-700 font-bold">GBPUSD</code>, <code class="text-blue-700 font-bold">USDJPY</code></li>
      <li>• วิเคราะห์ครอบคลุม <strong>7 กรอบเวลา (Timeframes)</strong> ได้แก่ <code>W1</code>, <code>D1</code>, <code>H4</code>, <code>H1</code>, <code>M30</code>, <code>M15</code> และ <code>M5</code></li>
    </ul>
  </div>

  <div class="bw-card">
    <div class="flex items-center gap-2 mb-2">
      <span class="px-2.5 py-0.5 rounded bg-blue-700 text-white font-mono text-xs font-bold">SCOPE 2</span>
      <h3 class="text-sm font-extrabold text-slate-900">ขอบเขตด้านอัลกอริทึม SMC (Algorithmic Modules)</h3>
    </div>
    <ul class="text-xs text-slate-700 space-y-1.5 leading-relaxed">
      <li>• <strong>Structure &amp; Extrema:</strong> ตรวจจับจุดกลับตัว <code>Swing High/Low</code> และโครงสร้าง <code>BOS / CHoCH</code></li>
      <li>• <strong>Institutional Zones:</strong> ตรวจจับโซน <code>Order Block (OB)</code> กรองด้วย ATR และช่องว่าง <code>Fair Value Gap (FVG)</code> พร้อมเช็คสถานะ <code>Mitigated</code></li>
      <li>• <strong>Liquidity &amp; Valuation:</strong> ระบุระดับ <code>EQH/EQL</code>, โซน <code>Premium/Equilibrium/Discount</code> และ <code>SMT Divergence</code></li>
    </ul>
  </div>

  <div class="bw-card">
    <div class="flex items-center gap-2 mb-2">
      <span class="px-2.5 py-0.5 rounded bg-slate-900 text-white font-mono text-xs font-bold">SCOPE 3</span>
      <h3 class="text-sm font-extrabold text-slate-900">ขอบเขตด้านการแสดงผลและแดชบอร์ด (Visualization)</h3>
    </div>
    <ul class="text-xs text-slate-700 space-y-1.5 leading-relaxed">
      <li>• วาดกราฟแท่งเทียนพร้อมเลเยอร์ SMC Overlay ที่เลือกเปิด-ปิด (Toggle) ได้อย่างอิสระ</li>
      <li>• แสดงตาราง <strong>Multi-Timeframe Trend Dashboard</strong> คำนวณคะแนนถ่วงน้ำหนักสุทธิ (-13 ถึง +13)</li>
      <li>• แสดงระบบ <strong>H4 SMC Setup Radar</strong> แจ้งเตือนเมื่อราคาเข้าใกล้โซนสำคัญภายในระยะ 0.3%</li>
    </ul>
  </div>

  <div class="bw-card">
    <div class="flex items-center gap-2 mb-2">
      <span class="px-2.5 py-0.5 rounded bg-slate-900 text-white font-mono text-xs font-bold">SCOPE 4</span>
      <h3 class="text-sm font-extrabold text-slate-900">ขอบเขตด้านการจำลอง Backtest และประเมินผล</h3>
    </div>
    <ul class="text-xs text-slate-700 space-y-1.5 leading-relaxed">
      <li>• จำลองการเข้าซื้อขายย้อนหลังตามเงื่อนไขโครงสร้าง SMC พร้อมตั้งค่า Risk% และ R:R Ratio</li>
      <li>• รายงานผลสถิติ <strong>Win Rate, Total Trades, Net Profit, Profit Factor, Max Drawdown</strong></li>
      <li>• ประเมินความพึงพอใจการใช้งานระบบโดยกลุ่มตัวอย่างผู้ใช้งานจริง 3 ด้าน (Likert Scale 5 ระดับ)</li>
    </ul>
  </div>
</div>

---
layout: default
---

<!-- SLIDE 5: TECH STACK -->
<div class="mb-2">
  <span class="bw-badge">04 • TECHNOLOGY STACK</span>
  <h1 class="!text-2xl font-extrabold text-slate-900 mt-1">สถาปัตยกรรมและเทคโนโลยีที่ใช้พัฒนา (TECH STACK)</h1>
</div>

<div class="grid grid-cols-3 gap-4 mt-4">
  <!-- Column 1: Backend -->
  <div class="bw-card border-t-4 border-t-blue-800">
    <div class="text-xs font-mono font-bold text-blue-700 uppercase">1. Backend &amp; API Layer</div>
    <h3 class="text-base font-extrabold text-slate-900 mt-1 mb-3">Python &amp; FastAPI Server</h3>
    <div class="space-y-2.5 text-xs">
      <div class="p-2.5 rounded-lg bg-blue-50/70 border border-blue-200">
        <div class="font-bold text-slate-900">Python 3.10+</div>
        <div class="text-slate-600">ภาษาหลักสำหรับประมวลผลอัลกอริทึมเชิงปริมาณและโครงสร้างตลาด</div>
      </div>
      <div class="p-2.5 rounded-lg bg-blue-50/70 border border-blue-200">
        <div class="font-bold text-slate-900">FastAPI + Uvicorn</div>
        <div class="text-slate-600">RESTful API ความเร็วสูง แยก Router ชัดเจน (<code>/api/chart</code>, <code>/api/dashboard</code>, <code>/api/backtest</code>)</div>
      </div>
      <div class="p-2.5 rounded-lg bg-blue-50/70 border border-blue-200">
        <div class="font-bold text-slate-900">Pydantic Models</div>
        <div class="text-slate-600">ตรวจสอบความถูกต้องของพารามิเตอร์และโครงสร้างข้อมูล JSON</div>
      </div>
    </div>
  </div>

  <!-- Column 2: Quantitative & Data -->
  <div class="bw-card border-t-4 border-t-blue-600">
    <div class="text-xs font-mono font-bold text-blue-600 uppercase">2. Quantitative &amp; Data Engine</div>
    <h3 class="text-base font-extrabold text-slate-900 mt-1 mb-3">NumPy, Pandas &amp; MT5</h3>
    <div class="space-y-2.5 text-xs">
      <div class="p-2.5 rounded-lg bg-blue-50/70 border border-blue-200">
        <div class="font-bold text-slate-900">NumPy Vectorized Arrays</div>
        <div class="text-slate-600">คำนวณ ATR, Cumulative Mean และสแกนแท่งเทียนด้วย Array Slicing ความเร็วสูง</div>
      </div>
      <div class="p-2.5 rounded-lg bg-blue-50/70 border border-blue-200">
        <div class="font-bold text-slate-900">Pandas DataFrame</div>
        <div class="text-slate-600">จัดการข้อมูลอนุกรมเวลา (Time-Series OHLCV) และการแปลง Timeframe</div>
      </div>
      <div class="p-2.5 rounded-lg bg-blue-50/70 border border-blue-200">
        <div class="font-bold text-slate-900">MetaTrader 5 Python API</div>
        <div class="text-slate-600">ดึงข้อมูลราคาตลาดจริงแบบเรียลไทม์และย้อนหลังจากโบรกเกอร์โดยตรง</div>
      </div>
    </div>
  </div>

  <!-- Column 3: Frontend -->
  <div class="bw-card border-t-4 border-t-slate-900">
    <div class="text-xs font-mono font-bold text-slate-700 uppercase">3. Frontend &amp; Visualization</div>
    <h3 class="text-base font-extrabold text-slate-900 mt-1 mb-3">Angular &amp; HTML5 Canvas</h3>
    <div class="space-y-2.5 text-xs">
      <div class="p-2.5 rounded-lg bg-slate-50 border border-blue-200">
        <div class="font-bold text-slate-900">Angular + TypeScript</div>
        <div class="text-slate-600">พัฒนา Single-Page Application (SPA) จัดการ State และ Component แบบ Reactive</div>
      </div>
      <div class="p-2.5 rounded-lg bg-slate-50 border border-blue-200">
        <div class="font-bold text-slate-900">TradingView Lightweight Charts</div>
        <div class="text-slate-600">เรนเดอร์กราฟแท่งเทียนที่ลื่นไหล รองรับการซูมและเลื่อนดูข้อมูลย้อนหลัง</div>
      </div>
      <div class="p-2.5 rounded-lg bg-slate-50 border border-blue-200">
        <div class="font-bold text-slate-900">Custom HTML5 Canvas Overlay</div>
        <div class="text-slate-600">วาดกล่องโซน OB, FVG, ป้ายกำกับ BOS/CHoCH และเส้น EQH/EQL ทับบนกราฟอย่างแม่นยำ</div>
      </div>
    </div>
  </div>
</div>

---
layout: default
---

<!-- SLIDE 6: DATA FLOW DIAGRAM -->
<div class="flex items-center justify-between mb-1">
  <div>
    <span class="bw-badge">05 • SYSTEM DATA FLOW</span>
    <h1 class="!text-xl font-extrabold text-slate-900 mt-0.5">แผนภาพการไหลของข้อมูล (Data Flow Architecture)</h1>
  </div>
  <span class="text-xs font-mono text-blue-700 bg-blue-50 px-3 py-1 rounded-full border border-blue-200">
    Input → MT5 OHLCV → SMC Engine → Interactive UI
  </span>
</div>

<div class="bg-white rounded-2xl border-2 border-blue-200 p-2 shadow-sm">
  <img src="/images/data_flow.svg" alt="System Data Flow Diagram" class="w-full h-[355px] object-contain mx-auto" />
</div>

---
layout: default
---

<!-- SLIDE 7: วิธีใช้งาน (HOW TO USE) -->
<div class="mb-2">
  <span class="bw-badge">06 • USER WORKFLOW</span>
  <h1 class="!text-2xl font-extrabold text-slate-900 mt-1">วิธีการใช้งานระบบ (4 ขั้นตอนการทำงานหลัก)</h1>
</div>

<div class="grid grid-cols-4 gap-3.5 mt-4">
  <div class="bw-card flex flex-col justify-between border-t-4 border-t-blue-800">
    <div>
      <div class="w-10 h-10 rounded-xl bg-blue-800 text-white font-mono font-extrabold text-lg flex items-center justify-center mb-3">01</div>
      <h3 class="text-sm font-extrabold text-slate-900 mb-1.5">เลือกสินทรัพย์และกรอบเวลา</h3>
      <p class="text-xs text-slate-600 leading-relaxed">
        ผู้ใช้เลือกคู่เงินหรือทองคำ (เช่น <code>XAUUSD</code>) และเลือก Timeframe ที่ต้องการวิเคราะห์ (<code>M5</code> ถึง <code>W1</code>) จากแถบเมนูด้านบน ระบบจะดึงแท่งเทียนล่าสุดจาก MT5 ทันที
      </p>
    </div>
    <div class="mt-3 pt-2 border-t border-blue-100 text-[11px] font-mono text-blue-700 font-bold">
      Symbol &amp; TF Selection
    </div>
  </div>

  <div class="bw-card flex flex-col justify-between border-t-4 border-t-blue-600">
    <div>
      <div class="w-10 h-10 rounded-xl bg-blue-600 text-white font-mono font-extrabold text-lg flex items-center justify-center mb-3">02</div>
      <h3 class="text-sm font-extrabold text-slate-900 mb-1.5">วิเคราะห์กราฟ SMC อัตโนมัติ</h3>
      <p class="text-xs text-slate-600 leading-relaxed">
        ระบบวาดจุด Swing High/Low, เส้น BOS/CHoCH, กล่องโซน Order Block และช่องว่าง FVG บนกราฟให้อัตโนมัติ พร้อมปุ่ม Toggle เลือกเปิด/ปิดโซนที่ถูกทำลายแล้ว (Mitigated) ได้
      </p>
    </div>
    <div class="mt-3 pt-2 border-t border-blue-100 text-[11px] font-mono text-blue-700 font-bold">
      Interactive SMC Overlay
    </div>
  </div>

  <div class="bw-card flex flex-col justify-between border-t-4 border-t-blue-500">
    <div>
      <div class="w-10 h-10 rounded-xl bg-blue-500 text-white font-mono font-extrabold text-lg flex items-center justify-center mb-3">03</div>
      <h3 class="text-sm font-extrabold text-slate-900 mb-1.5">ตรวจตาราง 7-TF &amp; H4 Radar</h3>
      <p class="text-xs text-slate-600 leading-relaxed">
        ดูตารางสรุปเทรนด์ทั้ง 7 กรอบเวลา คะแนนรวมถ่วงน้ำหนัก สัญญาณแนะนำ (<code>Strong BUY/SELL</code>) โซนราคาถูก/แพง (Discount/Premium) และเรดาร์แจ้งเตือนโซน H4
      </p>
    </div>
    <div class="mt-3 pt-2 border-t border-blue-100 text-[11px] font-mono text-blue-700 font-bold">
      Confluence &amp; Setup Radar
    </div>
  </div>

  <div class="bw-card flex flex-col justify-between border-t-4 border-t-slate-900">
    <div>
      <div class="w-10 h-10 rounded-xl bg-slate-900 text-white font-mono font-extrabold text-lg flex items-center justify-center mb-3">04</div>
      <h3 class="text-sm font-extrabold text-slate-900 mb-1.5">รันจำลองการเทรดย้อนหลัง</h3>
      <p class="text-xs text-slate-600 leading-relaxed">
        เปิดหน้าต่าง Backtest ตั้งค่าเงินทุนเริ่มต้นและความเสี่ยง ระบบจะจำลองการเข้าเทรดตามสัญญาณ SMC พร้อมแสดงจุดเข้า-ออกบนกราฟ และสรุป Win Rate / PnL ทันที
      </p>
    </div>
    <div class="mt-3 pt-2 border-t border-blue-100 text-[11px] font-mono text-slate-800 font-bold">
      Backtest &amp; Performance KPI
    </div>
  </div>
</div>

<div class="mt-4 bw-card-soft flex items-center justify-between">
  <div class="text-xs text-blue-950">
    <strong>💡 จุดเด่นด้านประสบการณ์ผู้ใช้ (UX):</strong> ลดขั้นตอนการตีกราฟด้วยมือจากเดิมที่ต้องใช้เวลา 15–20 นาทีต่อคู่เงิน เหลือเพียง <strong>คลิกเดียว (&lt; 1 วินาที)</strong>
  </div>
  <span class="px-3 py-1 rounded-full bg-blue-700 text-white font-mono text-xs font-bold">Real-Time Response</span>
</div>

---
layout: default
---

<!-- SLIDE 8: HIGHLIGHT & EVALUATION RESULTS -->
<div class="mb-2">
  <span class="bw-badge">07 • PROJECT HIGHLIGHTS &amp; EVALUATION</span>
  <h1 class="!text-2xl font-extrabold text-slate-900 mt-1">จุดเด่นของโครงงาน (Highlights) และผลการประเมินความพึงพอใจ</h1>
</div>

<div class="grid grid-cols-12 gap-4 mt-3">
  <!-- Left 7 Cols: Engineering Highlights -->
  <div class="col-span-7 space-y-2.5">
    <div class="bw-card">
      <div class="text-xs font-mono font-bold text-blue-700">HIGHLIGHT 01 • ZERO SUBJECTIVE BIAS</div>
      <h3 class="text-sm font-extrabold text-slate-900 mt-0.5">มาตรฐานการตรวจจับโครงสร้างตลาดแบบ Deterministic 100%</h3>
      <p class="text-xs text-slate-600 mt-0.5">
        ใช้ Finite State Machine และเกณฑ์ราคาปิด (Body Break) แยกแยะ BOS และ CHoCH อย่างเป็นระบบ ขจัดอคติทางอารมณ์และการตีกราฟไม่ตรงกันของเทรดเดอร์
      </p>
    </div>

    <div class="bw-card">
      <div class="text-xs font-mono font-bold text-blue-700">HIGHLIGHT 02 • QUANTITATIVE NOISE FILTERING</div>
      <h3 class="text-sm font-extrabold text-slate-900 mt-0.5">คัดกรองเฉพาะโซนสถาบันคุณภาพสูงด้วย ATR &amp; Cumulative Mean</h3>
      <p class="text-xs text-slate-600 mt-0.5">
        กรองแท่ง Order Block ที่ผันผวนผิดปกติออกด้วยเกณฑ์ <code>&lt; 2 × ATR</code> และกรองช่องว่าง FVG ด้วยเกณฑ์ <code>BarDelta &gt; 2 × Cumulative Mean</code> พร้อมอัปเดตสถานะ Mitigation อัตโนมัติ
      </p>
    </div>

    <div class="bw-card">
      <div class="text-xs font-mono font-bold text-blue-700">HIGHLIGHT 03 • 7-TIMEFRAME CONFLUENCE MATRIX</div>
      <h3 class="text-sm font-extrabold text-slate-900 mt-0.5">ผสานมุมมองภาพใหญ่ (W1/D1) เข้ากับจังหวะเข้าเทรด (M15/M5)</h3>
      <p class="text-xs text-slate-600 mt-0.5">
        คำนวณคะแนนถ่วงน้ำหนัก 7 กรอบเวลาพร้อมกัน ช่วยให้ผู้ใช้งานเทรดตามทิศทางของสถาบันการเงินรายใหญ่และไม่สวนเทรนด์หลัก
      </p>
    </div>
  </div>

  <!-- Right 5 Cols: User Evaluation Results (Table 3) -->
  <div class="col-span-5 bw-card-navy flex flex-col justify-between">
    <div>
      <div class="flex items-center justify-between">
        <span class="text-xs font-mono text-blue-300 uppercase">User Evaluation • ตารางที่ 3</span>
        <span class="px-2 py-0.5 rounded bg-blue-600 text-white text-[11px] font-mono font-bold">Likert 5 ระดับ</span>
      </div>
      <h3 class="text-base font-extrabold text-white mt-1 mb-3">ผลการประเมินความพึงพอใจของผู้ใช้งานที่มีต่อระบบ</h3>

      <div class="space-y-3">
        <div class="p-3 rounded-xl bg-white/10 border border-blue-400/30 flex items-center justify-between">
          <div>
            <div class="text-xs font-bold text-white">1. ความเหมาะสมต่อการแก้ปัญหา</div>
            <div class="text-[11px] text-blue-200">ลดเวลาตีกราฟและลดอคติในการตัดสินใจ</div>
          </div>
          <div class="text-right">
            <div class="text-2xl font-extrabold text-blue-300">4.52</div>
            <div class="text-[10px] font-mono text-blue-200">S.D. = 0.51 (ดีมาก)</div>
          </div>
        </div>

        <div class="p-3 rounded-xl bg-white/10 border border-blue-400/30 flex items-center justify-between">
          <div>
            <div class="text-xs font-bold text-white">2. การออกแบบส่วนติดต่อผู้ใช้ (GUI)</div>
            <div class="text-[11px] text-blue-200">กราฟอ่านง่าย สีโซนชัดเจน ใช้งานสะดวก</div>
          </div>
          <div class="text-right">
            <div class="text-2xl font-extrabold text-blue-300">4.48</div>
            <div class="text-[10px] font-mono text-blue-200">S.D. = 0.54 (ดี)</div>
          </div>
        </div>

        <div class="p-3 rounded-xl bg-white/10 border border-blue-400/30 flex items-center justify-between">
          <div>
            <div class="text-xs font-bold text-white">3. ความเหมาะสมของเทคนิคและฟังก์ชัน</div>
            <div class="text-[11px] text-blue-200">ความถูกต้องของอัลกอริทึม SMC และ 7 Timeframes</div>
          </div>
          <div class="text-right">
            <div class="text-2xl font-extrabold text-blue-300">4.56</div>
            <div class="text-[10px] font-mono text-blue-200">S.D. = 0.50 (ดีมาก)</div>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-3 pt-2 border-t border-blue-700/60 flex items-center justify-between text-xs">
      <span class="text-blue-200 font-semibold">ค่าเฉลี่ยรวมทั้งหมด (Overall Mean)</span>
      <span class="text-lg font-extrabold text-white font-mono">4.52 / 5.00 (ดีมาก)</span>
    </div>
  </div>
</div>

---
layout: default
---

<!-- SLIDE 9: SWING HIGH / LOW (DIAGRAM + EXPLANATION + SOURCE CODE) -->
<div class="flex items-center justify-between mb-1.5">
  <div>
    <span class="bw-badge">08 • ALGORITHM DEEP DIVE 1/5</span>
    <h1 class="!text-xl font-extrabold text-slate-900 mt-0.5">การตรวจจับจุดกลับตัว: SWING HIGH &amp; SWING LOW</h1>
  </div>
  <span class="text-xs font-mono font-bold text-blue-800 bg-blue-100 px-3 py-1 rounded-lg border border-blue-300">
    services/smc_engine.py → detect_swings()
  </span>
</div>

<div class="grid grid-cols-12 gap-3.5 items-start">
  <!-- Left Column: Visual Diagram + Explanation -->
  <div class="col-span-6 space-y-2">
    <div class="bg-white rounded-xl border-2 border-blue-200 p-1.5 shadow-sm">
      <img src="/images/swing_diagram.svg" alt="Swing High Low Diagram" class="w-full h-[225px] object-contain mx-auto" />
    </div>
    <div class="bw-card-soft text-[11.5px] leading-relaxed text-slate-800 space-y-1">
      <div class="font-extrabold text-blue-900 text-xs">หลักการทำงาน (Sliding Window Extremum ขนาด 2N + 1):</div>
      <p>• <strong>หน้าต่างตรวจสอบ:</strong> ใช้จำนวนแท่งเทียน $N$ แท่งทางซ้าย และ $N$ แท่งทางขวาของแท่งที่ $i$ (ค่าเริ่มต้น $N=5$ สำหรับ M5–H4 และ $N=3$ สำหรับ D1–W1)</p>
      <p>• <strong>Swing High ($SH_i$):</strong> เกิดเมื่อราคาสูงสุด <code>highs[i]</code> มีค่ามากที่สุดในช่วงหน้าต่าง <code>highs[i-n : i+n+1]</code></p>
      <p>• <strong>Swing Low ($SL_i$):</strong> เกิดเมื่อราคาต่ำสุด <code>lows[i]</code> มีค่าน้อยที่สุดในช่วงหน้าต่าง <code>lows[i-n : i+n+1]</code></p>
    </div>
  </div>

  <!-- Right Column: Source Code + Code Walkthrough -->
  <div class="col-span-6 space-y-2">
```python {1|2-5|7-10|11-14|15}
def detect_swings(df: pd.DataFrame, n: int = 5) -> tuple[list, list]:
    highs = df["high_price"].values
    lows = df["low_price"].values
    times = df["time_stamp"]
    swing_highs, swing_lows = [], []

    for i in range(n, len(df) - n):
        if highs[i] == max(highs[i - n : i + n + 1]):
            if not swing_highs or swing_highs[-1]["idx"] != i:
                swing_highs.append({
                    "time": str(times.iloc[i]),
                    "price": round(float(highs[i]), 5),
                    "idx": i
                })
        if lows[i] == min(lows[i - n : i + n + 1]):
            if not swing_lows or swing_lows[-1]["idx"] != i:
                swing_lows.append({
                    "time": str(times.iloc[i]),
                    "price": round(float(lows[i]), 5),
                    "idx": i
                })
    return swing_highs, swing_lows
```
    <div class="bw-card !p-2.5 text-[11px] leading-relaxed text-slate-700">
      <div class="font-bold text-slate-900 mb-0.5">คำอธิบายการทำงานของ Source Code:</div>
      <div>1. <strong>บรรทัด 2–4:</strong> ดึงคอลัมน์ราคาออกเป็น <code>NumPy Array</code> เพื่อเข้าถึงตำแหน่ง Index ด้วยความเร็วสูง</div>
      <div>2. <strong>บรรทัด 7:</strong> วนลูปเฉพาะช่วง <code>range(n, len(df) - n)</code> เพื่อป้องกัน Index Out of Bounds และยืนยันว่าแท่งขวาปิดครบ $N$ แท่งแล้ว</div>
      <div>3. <strong>บรรทัด 8–21:</strong> เปรียบเทียบค่าสูงสุด/ต่ำสุดใน Slice <code>[i-n : i+n+1]</code> แล้วเก็บ <code>time</code>, <code>price</code> และ <code>idx</code> ส่งให้โมดูลถัดไป</div>
    </div>
  </div>
</div>

---
layout: default
---

<!-- SLIDE 10: CHOCH & BOS (DIAGRAM + EXPLANATION + SOURCE CODE) -->
<div class="flex items-center justify-between mb-1.5">
  <div>
    <span class="bw-badge">09 • ALGORITHM DEEP DIVE 2/5</span>
    <h1 class="!text-xl font-extrabold text-slate-900 mt-0.5">โครงสร้างตลาดและการกลับตัว: CHOCH &amp; BOS</h1>
  </div>
  <span class="text-xs font-mono font-bold text-blue-800 bg-blue-100 px-3 py-1 rounded-lg border border-blue-300">
    services/smc_engine.py → detect_structure()
  </span>
</div>

<div class="grid grid-cols-12 gap-3.5 items-start">
  <!-- Left Column: Visual Diagram + Explanation -->
  <div class="col-span-6 space-y-2">
    <div class="bg-white rounded-xl border-2 border-blue-200 p-1.5 shadow-sm">
      <img src="/images/choch_diagram.svg" alt="CHoCH and BOS Diagram" class="w-full h-[225px] object-contain mx-auto" />
    </div>
    <div class="bw-card-soft text-[11.5px] leading-relaxed text-slate-800 space-y-1">
      <div class="font-extrabold text-blue-900 text-xs">หลักการทำงานของ Finite State Machine (BOS vs CHoCH):</div>
      <p>• <strong>สถานะแนวโน้ม (State):</strong> ติดตามตัวแปร <code>trend</code> ใน 3 สถานะ คือ <code>"neutral"</code>, <code>"bullish"</code> และ <code>"bearish"</code></p>
      <p>• <strong>BOS (Break of Structure):</strong> ราคาปิดทะลุจุด Swing ในทิศทางเดียวกับเทรนด์ปัจจุบัน (ยืนยันว่าเทรนด์เดิมดำเนินต่อไป)</p>
      <p>• <strong>CHoCH (Change of Character):</strong> ราคาปิดทะลุจุด Swing สวนทางกับเทรนด์ปัจจุบัน (เช่น เดิมเป็น <code>bullish</code> แต่ราคาปิดหลุดต่ำกว่า <code>last_sl</code> → เปลี่ยนสถานะเป็น <code>bearish</code> ทันที)</p>
    </div>
  </div>

  <!-- Right Column: Source Code + Walkthrough -->
  <div class="col-span-6 space-y-2">
```python {1-4|5-7|8-14|15-21}
def detect_structure(df: pd.DataFrame, swing_highs: list, swing_lows: list) -> list:
    events, trend = [], "neutral"
    closes = df["close_price"].values
    last_broken_sh_idx, last_broken_sl_idx = -1, -1

    for i in range(len(df)):
        close = closes[i]
        avail_sh = [s for s in sh_sorted if last_broken_sh_idx < s["idx"] < i]
        if avail_sh and close > avail_sh[-1]["price"]:
            last_sh = avail_sh[-1]
            event_type = "CHoCH" if trend == "bearish" else "BOS"
            events.append({"idx": i, "price": last_sh["price"],
                           "type": event_type, "direction": "bullish"})
            last_broken_sh_idx, trend = last_sh["idx"], "bullish"

        avail_sl = [s for s in sl_sorted if last_broken_sl_idx < s["idx"] < i]
        if avail_sl and close < avail_sl[-1]["price"]:
            last_sl = avail_sl[-1]
            event_type = "CHoCH" if trend == "bullish" else "BOS"
            events.append({"idx": i, "price": last_sl["price"],
                           "type": event_type, "direction": "bearish"})
            last_broken_sl_idx, trend = last_sl["idx"], "bearish"
    return events
```
    <div class="bw-card !p-2.5 text-[11px] leading-relaxed text-slate-700">
      <div class="font-bold text-slate-900 mb-0.5">คำอธิบายการทำงานของ Source Code:</div>
      <div>1. <strong>บรรทัด 8 &amp; 16:</strong> คัดกรองเฉพาะจุด Swing ที่เกิดขึ้นก่อนแท่งที่ <code>i</code> และยังไม่เคยถูกทำลายมาก่อน (<code>s["idx"] &gt; last_broken_idx</code>)</div>
      <div>2. <strong>บรรทัด 9 &amp; 17:</strong> ใช้ราคาปิด <code>close</code> เปรียบเทียบกับจุด Swing ล่าสุดเพื่อกรองไส้เทียนหลอก (Wick Sweep)</div>
      <div>3. <strong>บรรทัด 11 &amp; 19:</strong> ตัดสินชนิดเหตุการณ์ (<code>CHoCH</code> หรือ <code>BOS</code>) จากสถานะ <code>trend</code> ก่อนหน้า พร้อมอัปเดตสถานะใหม่</div>
    </div>
  </div>
</div>

---
layout: default
---

<!-- SLIDE 11: ORDER BLOCK (OB) (DIAGRAM + EXPLANATION + SOURCE CODE) -->
<div class="flex items-center justify-between mb-1.5">
  <div>
    <span class="bw-badge">10 • ALGORITHM DEEP DIVE 3/5</span>
    <h1 class="!text-xl font-extrabold text-slate-900 mt-0.5">การตรวจจับโซนคำสั่งซื้อขายสถาบัน: ORDER BLOCK (OB)</h1>
  </div>
  <span class="text-xs font-mono font-bold text-blue-800 bg-blue-100 px-3 py-1 rounded-lg border border-blue-300">
    services/smc_engine.py → detect_order_blocks()
  </span>
</div>

<div class="grid grid-cols-12 gap-3.5 items-start">
  <!-- Left Column: Visual Diagram + Detailed Explanation -->
  <div class="col-span-6 space-y-2">
    <div class="bg-white rounded-xl border-2 border-blue-200 p-1.5 shadow-sm">
      <img src="/images/ob_diagram.svg" alt="Order Block Diagram" class="w-full h-[225px] object-contain mx-auto" />
    </div>
    <div class="bw-card-soft text-[11.5px] leading-relaxed text-slate-800 space-y-1">
      <div class="font-extrabold text-blue-900 text-xs">หลักการทำงานของอัลกอริทึม Order Block (OB):</div>
      <p>• <strong>1. ค้นหา Origin Candle:</strong> เมื่อเกิด BOS/CHoCH ที่ตำแหน่ง <code>event_pos</code> ระบบจะสแกนย้อนหลังกลับไปไม่เกิน 50 แท่งเพื่อหาแท่งสีตรงข้ามแท่งสุดท้ายก่อนเกิดการพุ่งทะลุโครงสร้าง</p>
      <p>• <strong>2. กรองความผันผวนด้วย ATR:</strong> ข้ามแท่งเทียนที่มีความกว้างผิดปกติ <code>(High - Low) &gt;= 2 * ATR</code> เพื่อให้ได้โซนที่มีนัยสำคัญและไม่กว้างเกินไป</p>
      <p>• <strong>3. ตรวจสอบ Mitigation:</strong> สแกนไปข้างหน้าตั้งแต่แท่ง <code>event_pos</code> หากราคาย้อนกลับมาแตะขอบบน <code>low_arr[k] &lt;= top</code> (Bullish OB) จะตั้งค่า <code>mitigated = True</code></p>
    </div>
  </div>

  <!-- Right Column: Source Code + Code Explanation -->
  <div class="col-span-6 space-y-2">
```python {1-4|5-7|8-11|12-17|18-22}
for event in structure_events:
    event_pos = event.get("idx")
    if event["direction"] == "bullish":
        # สแกนย้อนหลังจากจุดเกิด BOS/CHoCH สูงสุดไม่เกิน 50 แท่ง
        for j in range(event_pos - 1, max(event_pos - 50, -1), -1):
            if use_atr_filter and (high_arr[j] - low_arr[j]) >= 2 * atr[j]:
                continue  # กรองแท่งที่ผันผวนเกิน 2 เท่าของค่า ATR ออก
            if close_arr[j] < open_arr[j]:  # พบแท่งแดงต้นกำเนิด (Origin Candle)
                top = round(float(max(open_arr[j], close_arr[j])), 5)
                bot = round(float(min(open_arr[j], close_arr[j])), 5)

                mitigated, end_time = False, last_timestamp
                for k in range(event_pos, len(df)):
                    if low_arr[k] <= top:   # ราคาลงมาแตะใช้งานโซน OB แล้ว
                        mitigated = True
                        end_time = str(df["time_stamp"].iloc[k])
                        break
                order_blocks.append({
                    "type": "bullish", "top": top, "bottom": bot,
                    "mitigated": mitigated, "start_time": str(df["time_stamp"].iloc[j]),
                    "end_time": end_time, "event_type": event.get("type", "BOS")
                })
                break
```
    <div class="bw-card !p-2.5 text-[11px] leading-relaxed text-slate-700">
      <div class="font-bold text-slate-900 mb-0.5">คำอธิบายการทำงานของ Source Code:</div>
      <div>1. <strong>บรรทัด 5–7:</strong> ลูปถอยหลัง <code>range(event_pos-1, ..., -1)</code> คู่กับตัวกรอง <code>2 * atr[j]</code> ช่วยตัดแท่งข่าวกระชากแรงออก</div>
      <div>2. <strong>บรรทัด 8–10:</strong> เมื่อพบแท่งแดง (<code>close &lt; open</code>) จะดึงขอบเขตเนื้อเทียนเป็นโซน <code>top</code> และ <code>bot</code></div>
      <div>3. <strong>บรรทัด 13–17:</strong> ตรวจเช็คว่าแท่งถัดไปกลับมาทดสอบโซนหรือยัง เพื่อแยกการวาดสีระหว่างโซน <strong>Active</strong> กับ <strong>Mitigated</strong></div>
    </div>
  </div>
</div>

---
layout: default
---

<!-- SLIDE 12: FAIR VALUE GAP (FVG) (DIAGRAM + EXPLANATION + SOURCE CODE) -->
<div class="flex items-center justify-between mb-1.5">
  <div>
    <span class="bw-badge">11 • ALGORITHM DEEP DIVE 4/5</span>
    <h1 class="!text-xl font-extrabold text-slate-900 mt-0.5">การตรวจจับช่องว่างสภาพคล่อง: FAIR VALUE GAP (FVG)</h1>
  </div>
  <span class="text-xs font-mono font-bold text-blue-800 bg-blue-100 px-3 py-1 rounded-lg border border-blue-300">
    services/smc_engine.py → detect_fvg()
  </span>
</div>

<div class="grid grid-cols-12 gap-3.5 items-start">
  <!-- Left Column: Visual Diagram + Explanation -->
  <div class="col-span-6 space-y-2">
    <div class="bg-white rounded-xl border-2 border-blue-200 p-1.5 shadow-sm">
      <img src="/images/fvg_diagram.svg" alt="Fair Value Gap Diagram" class="w-full h-[225px] object-contain mx-auto" />
    </div>
    <div class="bw-card-soft text-[11.5px] leading-relaxed text-slate-800 space-y-1">
      <div class="font-extrabold text-blue-900 text-xs">หลักการทำงานของอัลกอริทึม Fair Value Gap (3-Candle Imbalance):</div>
      <p>• <strong>รูปแบบ 3 แท่งเทียน ($i-2, i-1, i$):</strong> เกิดขึ้นเมื่อแท่งกลาง ($i-1$) พุ่งแรงจนไส้เทียนของแท่งที่ $i-2$ และแท่งที่ $i$ ไม่ซ้อนทับกัน เกิดเป็นช่องว่างราคา (Liquidity Void)</p>
      <p>• <strong>เงื่อนไขช่องว่าง:</strong> Bullish FVG เกิดเมื่อ $\text{Low}_i - \text{High}_{i-2} > 0$ และ Bearish FVG เกิดเมื่อ $\text{Low}_{i-2} - \text{High}_i > 0$</p>
      <p>• <strong>Statistical Displacement Filter:</strong> กรองเฉพาะแท่งกลางที่มีขนาดพุ่งแรงเกิน 2 เท่าของค่าเฉลี่ยสะสม (<code>bar_delta &gt; 2 * cum_mean[i]</code>)</p>
    </div>
  </div>

  <!-- Right Column: Source Code + Code Walkthrough -->
  <div class="col-span-6 space-y-2">
```python {1-4|6-11|12-15|16-22}
def detect_fvg(df: pd.DataFrame, use_auto_threshold: bool = True) -> list:
    # คำนวณขนาดการเปลี่ยนแปลง (%) และค่าเฉลี่ยสะสมด้วย Vectorized NumPy
    bar_deltas = np.abs(close_arr - open_arr) / (np.abs(open_arr) + 1e-10) * 100
    cum_mean = np.cumsum(bar_deltas) / np.arange(1, n + 1)

    for i in range(2, n):
        c0_high, c0_low = float(high_arr[i - 2]), float(low_arr[i - 2])
        c2_high, c2_low = float(high_arr[i]), float(low_arr[i])
        bar_delta = bar_deltas[i - 1]
        threshold = cum_mean[i] * 2 if use_auto_threshold else 0

        gap_up = c2_low - c0_high
        if gap_up > 0 and bar_delta > threshold:
            top, bottom = round(c2_low, 5), round(c0_high, 5)
            mitigated = False
            for k in range(i + 1, n):
                if low_arr[k] <= bottom:  # ราคาลงมาเติมเต็มช่องว่าง FVG ครบแล้ว
                    mitigated = True
                    break
            fvgs.append({"type": "bullish", "top": top, "bottom": bottom,
                         "mitigated": mitigated, "idx": i - 1})
    return fvgs
```
    <div class="bw-card !p-2.5 text-[11px] leading-relaxed text-slate-700">
      <div class="font-bold text-slate-900 mb-0.5">คำอธิบายการทำงานของ Source Code:</div>
      <div>1. <strong>บรรทัด 3–4:</strong> คำนวณ <code>bar_deltas</code> และค่าเฉลี่ยสะสม <code>cum_mean</code> ล่วงหน้าทั้งอาเรย์ด้วย <code>np.cumsum</code> โดยไม่ต้องวนลูปซ้อน</div>
      <div>2. <strong>บรรทัด 12–13:</strong> ตรวจเช็คพร้อมกันทั้งระยะช่องว่าง <code>gap_up &gt; 0</code> และความแรงของแท่งส่ง <code>bar_delta &gt; threshold</code></div>
      <div>3. <strong>บรรทัด 16–19:</strong> ตรวจสอบว่าแท่งถัดไปวิ่งลงมาปิดช่องว่างถึงขอบล่าง (<code>low_arr[k] &lt;= bottom</code>) หรือยัง</div>
    </div>
  </div>
</div>

---
layout: default
---

<!-- SLIDE 13: MULTI-TIMEFRAME CALCULATION (DIAGRAM + EXPLANATION + SOURCE CODE) -->
<div class="flex items-center justify-between mb-1.5">
  <div>
    <span class="bw-badge">12 • ALGORITHM DEEP DIVE 5/5</span>
    <h1 class="!text-xl font-extrabold text-slate-900 mt-0.5">การคำนวณหลาย Timeframe (Multi-Timeframe Confluence 7 TFs)</h1>
  </div>
  <span class="text-xs font-mono font-bold text-blue-800 bg-blue-100 px-3 py-1 rounded-lg border border-blue-300">
    routers/dashboard.py → get_dashboard()
  </span>
</div>

<div class="grid grid-cols-12 gap-3.5 items-start">
  <!-- Left Column: Visual Diagram + Explanation -->
  <div class="col-span-6 space-y-2">
    <div class="bg-white rounded-xl border-2 border-blue-200 p-1.5 shadow-sm">
      <img src="/images/mtf_diagram.svg" alt="Multi-Timeframe Scoring Diagram" class="w-full h-[225px] object-contain mx-auto" />
    </div>
    <div class="bw-card-soft text-[11.5px] leading-relaxed text-slate-800 space-y-1">
      <div class="font-extrabold text-blue-900 text-xs">หลักการคำนวณคะแนนถ่วงน้ำหนัก 7 กรอบเวลา ($S_{\text{total}} = \sum w_k D_k$):</div>
      <p>• <strong>การถ่วงน้ำหนักตามลำดับชั้น:</strong> ให้ความสำคัญกับภาพใหญ่ <code>W1=3, D1=3</code> รองลงมาคือกรอบเวลากลาง <code>H4=2, H1=2</code> และกรอบเวลาเข้าเทรด <code>M30=1, M15=1, M5=1</code> (คะแนนเต็ม $\pm 13$)</p>
      <p>• <strong>การปรับค่า $n$ อัตโนมัติ:</strong> ใช้ <code>n=3</code> สำหรับ <code>W1, D1</code> เพื่อให้จับโครงสร้างใหญ่ได้ไวขึ้น และใช้ <code>n=5</code> สำหรับ <code>H4–M5</code> เพื่อกรองสัญญาณรบกวน</p>
      <p>• <strong>การแปลผลสัญญาณ:</strong> $\ge +5$ (<strong>Strong BUY</strong>), $>0$ (<strong>Weak BUY</strong>), $0$ (<strong>WAIT</strong>), $<0$ (<strong>Weak SELL</strong>), $\le -5$ (<strong>Strong SELL</strong>)</p>
    </div>
  </div>

  <!-- Right Column: Source Code + Code Walkthrough -->
  <div class="col-span-6 space-y-2">
```python {1-4|6-11|13-17|19-24}
@router.get("/dashboard/{symbol}")
def get_dashboard(symbol: str):
    tfs = ["W1", "D1", "H4", "H1", "M30", "M15", "M5"]
    weights = {"W1": 3, "D1": 3, "H4": 2, "H1": 2, "M30": 1, "M15": 1, "M5": 1}
    results, score = {}, 0

    for tf in tfs:
        df = get_market_df(symbol, tf, bars=bars_map.get(tf, 300))
        if df is not None and len(df) > 10:
            sh, sl = detect_swings(df, n=3 if tf in ["W1", "D1"] else 5)
            struct = detect_structure(df, sh, sl)
            trend = struct[-1]["direction"] if struct else "neutral"

        results[tf] = trend
        if trend == "bullish":
            score += weights[tf]
        elif trend == "bearish":
            score -= weights[tf]

    if score >= 5:    signal, rec = "BUY",  "Strong BUY (เทรนด์ขาขึ้นชัดเจน)"
    elif score > 0:   signal, rec = "BUY",  "Weak BUY (เทรนด์หลักเริ่มขึ้น)"
    elif score <= -5: signal, rec = "SELL", "Strong SELL (เทรนด์ขาลงชัดเจน)"
    elif score < 0:   signal, rec = "SELL", "Weak SELL (เทรนด์หลักเริ่มลง)"
    else:             signal, rec = "WAIT", "Sideways (เทรนด์ไม่ชัดเจน)"
    return {"symbol": symbol, "trends": results, "score": score, "signal": signal}
```
    <div class="bw-card !p-2.5 text-[11px] leading-relaxed text-slate-700">
      <div class="font-bold text-slate-900 mb-0.5">คำอธิบายการทำงานของ Source Code:</div>
      <div>1. <strong>บรรทัด 7–12:</strong> วนลูปดึงข้อมูลทั้ง 7 Timeframe แล้วเรียกใช้ <code>detect_swings()</code> และ <code>detect_structure()</code> เพื่อหาทิศทางล่าสุด</div>
      <div>2. <strong>บรรทัด 15–18:</strong> บวกหรือลบคะแนนตามค่าน้ำหนัก <code>weights[tf]</code> ของแต่ละ Timeframe เข้าสู่ตัวแปร <code>score</code></div>
      <div>3. <strong>บรรทัด 20–25:</strong> แปลงคะแนนรวมสุทธิเป็นคำแนะนำการเทรด พร้อมส่งต่อข้อมูลระดับ H4 ไปคำนวณ <strong>SMC Setup Radar</strong> และเป้าหมายสภาพคล่อง <strong>EQH/EQL</strong></div>
    </div>
  </div>
</div>
