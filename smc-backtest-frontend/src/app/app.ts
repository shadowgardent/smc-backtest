import { Component, AfterViewInit, OnDestroy, Inject, PLATFORM_ID, HostListener, ElementRef } from '@angular/core';
import { isPlatformBrowser, CommonModule } from '@angular/common';
import { MarketData, SmcDataResponse, PriceZone, EqualLevel, DiscountZone, LiveCandleResponse, DashboardResponse, BacktestResponse } from './market-data';
import {
  createChart, createSeriesMarkers,
  IChartApi, ISeriesApi, ISeriesMarkersPluginApi,
  CandlestickSeries, Time, SeriesMarker, CrosshairMode
} from 'lightweight-charts';

@Component({
  selector: 'app-root',
  imports: [CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App implements AfterViewInit, OnDestroy {
  activeTimeframe: string = 'M5';
  activeSymbol: string = 'EURUSD';
  symbols: string[] = ['EURUSD', 'XAUUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD'];

  // Layer Toggles (Default OFF)
  showSwings: boolean = false;
  showInternalSwings: boolean = false;
  showStructure: boolean = false;
  showInternalStructure: boolean = false;
  showOrderBlocks: boolean = false;
  showInternalOrderBlocks: boolean = false;
  showFVG: boolean = false;
  showEqualHL: boolean = false;
  showZones: boolean = false;
  showStrongWeakHL: boolean = false;

  isLayersOpen: boolean = false;

  isLoadingChart: boolean = false;
  isLoadingSmc: boolean = false;
  currentPrice: number | null = null;
  isLive: boolean = true;
  private lastChartTime: number = 0;

  private chart!: IChartApi;
  private candlestickSeries!: ISeriesApi<'Candlestick'>;
  private markersPlugin!: ISeriesMarkersPluginApi<Time>;
  private smcCanvas!: HTMLCanvasElement;
  private smcCtx!: CanvasRenderingContext2D;
  smcData: SmcDataResponse | null = null;
  private isBrowser: boolean;
  private liveInterval: ReturnType<typeof setInterval> | null = null;

  constructor(
    private marketData: MarketData, 
    @Inject(PLATFORM_ID) private platformId: Object,
    private eRef: ElementRef
  ) {
    this.isBrowser = isPlatformBrowser(platformId);
  }

  @HostListener('document:click', ['$event'])
  clickout(event: Event) {
    // ปิด Context Menu ถ้าคลิกซ้าย
    if (this.showContextMenu) {
      this.showContextMenu = false;
    }

    if (this.isLayersOpen) {
      // ตรวจสอบว่าจุดที่คลิกอยู่ข้างใน dropdown หรือไม่
      const clickedInside = this.eRef.nativeElement.querySelector('.dropdown-container')?.contains(event.target);
      if (!clickedInside) {
        this.isLayersOpen = false;
      }
    }
  }

  // ---- Context Menu ----
  showContextMenu: boolean = false;
  contextMenuX: number = 0;
  contextMenuY: number = 0;

  onRightClick(event: MouseEvent): void {
    event.preventDefault(); // ปิดเมนูคลิกขวาปกติของเบราว์เซอร์
    this.showContextMenu = true;
    this.contextMenuX = event.clientX;
    this.contextMenuY = event.clientY;
  }

  resetChartView(): void {
    this.showContextMenu = false;
    if (this.chart && this.candlestickSeries) {
      this.chart.timeScale().fitContent(); // ซูมแกนเวลาให้พอดี
      this.chart.priceScale('right').applyOptions({ autoScale: true }); // รีเซ็ตแกนราคา
      setTimeout(() => this.drawSmcOverlay(), 20);
    }
  }

  private getPlotDimensions(): { width: number; height: number } {
    const container = document.getElementById('chartContainer');
    const fullW = container ? container.clientWidth : (this.smcCanvas ? this.smcCanvas.clientWidth : 0);
    const fullH = container ? container.clientHeight : (this.smcCanvas ? this.smcCanvas.clientHeight : 0);
    const priceScaleW = this.chart ? (this.chart.priceScale('right').width() || 65) : 65;
    const timeScaleH = this.chart ? (this.chart.timeScale().height() || 28) : 28;
    return {
      width: Math.max(0, fullW - priceScaleW),
      height: Math.max(0, fullH - timeScaleH),
    };
  }

  ngAfterViewInit(): void {
    if (!this.isBrowser) return;
    const container = document.getElementById('chartContainer') as HTMLElement;
    this.chart = createChart(container, {
      width: container.clientWidth, height: container.clientHeight,
      layout: { background: { color: '#131722' }, textColor: '#9ca3af' },
      grid: { vertLines: { color: '#1e2130' }, horzLines: { color: '#1e2130' } },
      timeScale: { timeVisible: true, borderColor: '#2a2e39' },
      rightPriceScale: { borderColor: '#2a2e39' },
      crosshair: { 
        mode: CrosshairMode.Normal, // เปลี่ยนเป็น Normal เพื่อให้ลากอิสระ ไม่ดูด
        vertLine: { color: '#4a5568', width: 1, style: 2 }, 
        horzLine: { color: '#4a5568', width: 1, style: 2 } 
      },
    });
    this.candlestickSeries = this.chart.addSeries(CandlestickSeries, {
      upColor: '#26a69a', downColor: '#ef5350', borderVisible: false,
      wickUpColor: '#26a69a', wickDownColor: '#ef5350',
    });
    this.markersPlugin = createSeriesMarkers(this.candlestickSeries, []);
    this.setupSmcCanvas();
    this.chart.timeScale().subscribeVisibleLogicalRangeChange(() => { this.drawSmcOverlay(); });
    this.chart.timeScale().subscribeSizeChange(() => { this.onResize(); });
    container.addEventListener('pointermove', (e: PointerEvent) => {
      if (e.buttons > 0) this.drawSmcOverlay();
    });
    container.addEventListener('wheel', () => {
      requestAnimationFrame(() => this.drawSmcOverlay());
    }, { passive: true });
    window.addEventListener('resize', this.onResize);
    setTimeout(() => {
      this.loadData(this.activeTimeframe);
    }, 0);
  }

  ngOnDestroy(): void {
    if (this.isBrowser) {
      this.stopLiveUpdate();
      window.removeEventListener('resize', this.onResize);
      if (this.chart) this.chart.remove();
    }
  }

  private setupSmcCanvas(): void {
    const container = document.getElementById('chartContainer') as HTMLElement;
    this.smcCanvas = document.getElementById('smcCanvas') as HTMLCanvasElement;
    if (!container || !this.smcCanvas) return;
    const dpr = (this.isBrowser && window.devicePixelRatio) || 1;
    this.smcCanvas.width = container.clientWidth * dpr;
    this.smcCanvas.height = container.clientHeight * dpr;
    this.smcCanvas.style.width = `${container.clientWidth}px`;
    this.smcCanvas.style.height = `${container.clientHeight}px`;
    this.smcCtx = this.smcCanvas.getContext('2d')!;
    this.smcCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  private onResize = () => {
    const container = document.getElementById('chartContainer');
    if (!container) return;
    const newWidth = container.clientWidth;
    const newHeight = container.clientHeight;
    if (this.chart) this.chart.applyOptions({ width: newWidth, height: newHeight });
    if (this.smcCanvas && this.smcCtx) {
      const dpr = (this.isBrowser && window.devicePixelRatio) || 1;
      this.smcCanvas.width = newWidth * dpr;
      this.smcCanvas.height = newHeight * dpr;
      this.smcCanvas.style.width = `${newWidth}px`;
      this.smcCanvas.style.height = `${newHeight}px`;
      this.smcCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
      this.drawSmcOverlay();
    }
  };

  // ---- Navigation ----
  currentPage: 'chart' | 'dashboard' | 'backtest' = 'chart';

  // ---- Backtest ----
  backtestSymbol: string = 'EURUSD';
  backtestTimeframe: string = 'M15';
  backtestBars: number = 35000;
  backtestRiskReward: number = 3.0;
  backtestRiskPercent: number = 1.0;
  backtestStrategyMode: string = 'hybrid_partial_tp';
  backtestMaxTrades: number = 300;
  backtestUseBreakEven: boolean = true;
  backtestBreakEvenRr: number = 1.0;
  isLoadingBacktest: boolean = false;
  backtestData: BacktestResponse | null = null;

  openBacktest(): void {
    this.currentPage = 'backtest';
    this.backtestSymbol = this.activeSymbol;
    if (!this.backtestData) {
      this.runBacktest();
    }
  }

  runBacktest(): void {
    this.isLoadingBacktest = true;
    this.marketData.runBacktest(
      this.backtestSymbol,
      this.backtestTimeframe,
      this.backtestBars,
      this.backtestRiskReward,
      this.backtestRiskPercent,
      this.backtestStrategyMode,
      this.backtestMaxTrades,
      this.backtestUseBreakEven,
      this.backtestBreakEvenRr
    ).subscribe({
      next: (res) => {
        this.isLoadingBacktest = false;
        this.backtestData = res;
      },
      error: (err) => {
        this.isLoadingBacktest = false;
        console.error('Backtest error:', err);
      }
    });
  }

  // ---- Dashboard ----
  isLoadingDashboard: boolean = false;
  dashboardData: DashboardResponse | null = null;
  dashboardSymbol: string = 'EURUSD';

  // ---- Matrix ----
  isLoadingMatrix: boolean = false;
  matrixData: DashboardResponse[] = [];

  openDashboard(): void {
    this.currentPage = 'dashboard';
    this.dashboardSymbol = this.activeSymbol; // Sync กับกราฟตอนเปิดครั้งแรก
    this.loadDashboard();
    this.loadMatrix();
  }

  loadMatrix(): void {
    this.isLoadingMatrix = true;
    this.matrixData = [];
    let loadedCount = 0;
    
    this.symbols.forEach(sym => {
      this.marketData.getDashboardData(sym).subscribe({
        next: (res) => {
          this.matrixData.push(res);
          loadedCount++;
          if (loadedCount === this.symbols.length) {
            this.isLoadingMatrix = false;
            // Sort matrix by score (descending)
            this.matrixData.sort((a, b) => b.score - a.score);
          }
        },
        error: (err) => {
          console.error(`Error loading dashboard for ${sym}`, err);
          loadedCount++;
          if (loadedCount === this.symbols.length) this.isLoadingMatrix = false;
        }
      });
    });
  }

  loadDashboard(): void {
    this.isLoadingDashboard = true;
    this.dashboardData = null;
    this.marketData.getDashboardData(this.dashboardSymbol).subscribe({
      next: (res) => {
        this.dashboardData = res;
        this.isLoadingDashboard = false;
      },
      error: (err) => {
        console.error('Error loading dashboard', err);
        this.isLoadingDashboard = false;
      }
    });
  }

  // ---- Data Loading ----

  loadData(timeframe: string, symbol?: string): void {
    this.activeTimeframe = timeframe;
    if (symbol) this.activeSymbol = symbol;
    this.isLayersOpen = false; // ปิด dropdown อัตโนมัติเมื่อเปลี่ยนกราฟ
    
    // หยุดอัปเดต Live ชั่วคราวระหว่างเปลี่ยนกราฟ เพื่อป้องกันข้อมูลตีกัน
    this.stopLiveUpdate();
    
    this.isLoadingChart = true;
    this.smcData = null;
    this.markersPlugin.setMarkers([]);
    this.clearCanvas();
    
    // ตั้งค่าทศนิยมของแกนราคาตามคู่เงิน
    let precision = 5;
    let minMove = 0.00001;
    if (this.activeSymbol.includes('JPY')) {
      precision = 3;
      minMove = 0.001;
    } else if (this.activeSymbol.includes('XAU') || this.activeSymbol.includes('GOLD')) {
      precision = 2;
      minMove = 0.01;
    }
    if (this.candlestickSeries) {
      this.candlestickSeries.applyOptions({
        priceFormat: { type: 'price', precision: precision, minMove: minMove }
      });
    }

    this.marketData.getMarketData(this.activeSymbol, timeframe).subscribe({
      next: (response) => {
        if (!this.isBrowser || !this.candlestickSeries) return;
        this.isLoadingChart = false;
        const chartData = response.data
          .map((item) => ({ time: Math.floor(new Date(item.time_stamp).getTime() / 1000) as Time, open: item.open_price, high: item.high_price, low: item.low_price, close: item.close_price }))
          .sort((a, b) => (a.time as number) - (b.time as number));
        if (chartData.length > 0) {
          this.lastChartTime = chartData[chartData.length - 1].time as number;
        }
        this.candlestickSeries.setData(chartData);
        this.chart.timeScale().fitContent();
        this.loadSmcData(timeframe);
      },
      error: (err) => { this.isLoadingChart = false; console.error('Error fetching market data', err); },
    });
  }

  private loadSmcData(timeframe: string): void {
    this.isLoadingSmc = true;
    this.markersPlugin.setMarkers([]);
    this.clearCanvas();
    this.marketData.getSmcData(this.activeSymbol, timeframe).subscribe({
      next: (smcData) => {
        this.isLoadingSmc = false;
        this.smcData = smcData;
        this.renderSmcLayers();
        // เริ่ม real-time polling หลังโหลดข้อมูลครั้งแรกเสร็จ
        this.startLiveUpdate();
      },
      error: (err) => { this.isLoadingSmc = false; console.error('Error fetching SMC data', err); },
    });
  }

  // ---- SMC Rendering ----

  private renderSmcLayers(): void {
    if (!this.isBrowser || !this.smcData) return;
    this.applyMarkers();
    this.drawSmcOverlay();
  }

  private toTime(t: string): Time {
    return Math.floor(new Date(t).getTime() / 1000) as Time;
  }

  private applyMarkers(): void {
    if (!this.smcData) return;
    const markers: SeriesMarker<Time>[] = [];

    // Swing H/L
    if (this.showSwings) {
      for (const sh of this.smcData.swing_highs) {
        markers.push({ time: this.toTime(sh.time), position: 'aboveBar', color: '#ef5350', shape: 'arrowDown', text: 'H', size: 1 });
      }
      for (const sl of this.smcData.swing_lows) {
        markers.push({ time: this.toTime(sl.time), position: 'belowBar', color: '#26a69a', shape: 'arrowUp', text: 'L', size: 1 });
      }
    }

    // Internal Swing H/L (เล็กกว่า)
    if (this.showInternalSwings) {
      for (const sh of this.smcData.internal_highs) {
        markers.push({ time: this.toTime(sh.time), position: 'aboveBar', color: '#f87171', shape: 'arrowDown', text: 'h', size: 0 });
      }
      for (const sl of this.smcData.internal_lows) {
        markers.push({ time: this.toTime(sl.time), position: 'belowBar', color: '#34d399', shape: 'arrowUp', text: 'l', size: 0 });
      }
    }

    // Strong/Weak H/L
    if (this.showStrongWeakHL && this.smcData.strong_weak_hl) {
      const hl = this.smcData.strong_weak_hl;
      if (hl.strong_high) {
        markers.push({ time: this.toTime(hl.strong_high.time), position: 'aboveBar', color: '#f59e0b', shape: 'arrowDown', text: hl.strong_high.label, size: 1 });
      }
      if (hl.strong_low) {
        markers.push({ time: this.toTime(hl.strong_low.time), position: 'belowBar', color: '#f59e0b', shape: 'arrowUp', text: hl.strong_low.label, size: 1 });
      }
    }

    markers.sort((a, b) => (a.time as number) - (b.time as number));
    this.markersPlugin.setMarkers(markers);
  }

  private syncCanvasSize(): void {
    const container = document.getElementById('chartContainer');
    if (!container || !this.smcCanvas || !this.smcCtx) return;
    const w = container.clientWidth;
    const h = container.clientHeight;
    if (w <= 0 || h <= 0) return;
    const dpr = (this.isBrowser && window.devicePixelRatio) || 1;
    const targetW = Math.round(w * dpr);
    const targetH = Math.round(h * dpr);
    if (this.smcCanvas.width !== targetW || this.smcCanvas.height !== targetH) {
      this.smcCanvas.width = targetW;
      this.smcCanvas.height = targetH;
      this.smcCanvas.style.width = `${w}px`;
      this.smcCanvas.style.height = `${h}px`;
    }
    this.smcCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  private drawSmcOverlay(): void {
    if (!this.smcCtx || !this.chart || !this.candlestickSeries) return;
    this.syncCanvasSize();
    this.clearCanvas();
    if (!this.smcData) return;

    const { width: plotW, height: plotH } = this.getPlotDimensions();
    if (plotW <= 0 || plotH <= 0) return;

    this.smcCtx.save();
    this.smcCtx.beginPath();
    this.smcCtx.rect(0, 0, plotW, plotH);
    this.smcCtx.clip();

    // Premium/Discount Zones (วาดก่อนเพื่อให้อยู่ล่างสุด)
    if (this.showZones && this.smcData.zones) {
      const z = this.smcData.zones;
      if (z.premium)     this.drawHorizontalZone(z.premium,     'rgba(239,83,80,0.08)',   '#ef5350', plotW, plotH);
      if (z.equilibrium) this.drawHorizontalZone(z.equilibrium, 'rgba(156,163,175,0.08)', '#9ca3af', plotW, plotH);
      if (z.discount)    this.drawHorizontalZone(z.discount,    'rgba(38,166,154,0.08)',  '#26a69a', plotW, plotH);
    }

    // Internal Order Blocks
    if (this.showInternalOrderBlocks) {
      for (const ob of this.smcData.internal_order_blocks) {
        this.drawZone(ob, ob.type === 'bullish' ? 'rgba(49,121,245,0.25)' : 'rgba(247,124,128,0.25)',
          ob.type === 'bullish' ? '#3179f5' : '#f77c80', ob.type === 'bullish' ? 'Int Bull OB' : 'Int Bear OB', ob.mitigated, plotW, plotH);
      }
    }

    // Swing Order Blocks
    if (this.showOrderBlocks) {
      for (const ob of this.smcData.order_blocks) {
        this.drawZone(ob, ob.type === 'bullish' ? 'rgba(38,166,154,0.28)' : 'rgba(239,83,80,0.28)',
          ob.type === 'bullish' ? '#26a69a' : '#ef5350', ob.type === 'bullish' ? 'Bull OB' : 'Bear OB', ob.mitigated, plotW, plotH);
      }
    }

    // FVG
    if (this.showFVG) {
      for (const fvg of this.smcData.fvgs) {
        this.drawZone(fvg, fvg.type === 'bullish' ? 'rgba(59,130,246,0.20)' : 'rgba(168,85,247,0.20)',
          fvg.type === 'bullish' ? '#3b82f6' : '#a855f7', fvg.type === 'bullish' ? 'FVG ↑' : 'FVG ↓', fvg.mitigated, plotW, plotH);
      }
    }

    // Equal Highs/Lows
    if (this.showEqualHL) {
      for (const eq of this.smcData.equal_highs) this.drawEqualLine(eq, '#ef5350', 'EQH', plotW, plotH);
      for (const eq of this.smcData.equal_lows)  this.drawEqualLine(eq, '#26a69a', 'EQL', plotW, plotH);
    }

    // Internal Structure Lines
    if (this.showInternalStructure) {
      this.drawStructureLines(this.smcData.internal_structure, true, plotW, plotH);
    }

    // Swing Structure Lines
    if (this.showStructure) {
      this.drawStructureLines(this.smcData.swing_structure, false, plotW, plotH);
    }

    this.smcCtx.restore();
  }

  private resolveTimeX(t: Time): number | null {
    const timeScale = this.chart.timeScale();
    const coord = timeScale.timeToCoordinate(t);
    if (coord !== null) return coord as unknown as number;
    if (this.lastChartTime > 0 && (t as number) >= this.lastChartTime) {
      const lastCoord = timeScale.timeToCoordinate(this.lastChartTime as Time);
      if (lastCoord !== null) return lastCoord as unknown as number;
    }
    return null;
  }

  private drawStructureLines(events: any[], isInternal: boolean, plotW: number, plotH: number): void {
    if (!this.smcData) return;
    const ctx = this.smcCtx;

    for (const event of events) {
      const isChoch = event.type === 'CHoCH';
      const color = isChoch ? '#f59e0b' : event.direction === 'bullish' ? '#3b82f6' : '#a855f7';

      const tSwing = this.toTime(event.swing_time);
      const tBreak = this.toTime(event.time);
      const rawX1 = this.resolveTimeX(tSwing);
      const rawX2 = this.resolveTimeX(tBreak);
      const rawY  = this.candlestickSeries.priceToCoordinate(event.price);
      if (rawX1 === null || rawX2 === null || rawY === null) continue;

      const x1: number = rawX1;
      const x2: number = rawX2;
      const y: number  = rawY as unknown as number;

      if (x1 < 0 && x2 < 0) continue;
      if (x1 > plotW && x2 > plotW) continue;
      if (y < 0 || y > plotH) continue;

      const PADDING = 45;
      const xStart = Math.max(0, x1);
      const actualPadding = (x2 - x1) > PADDING ? PADDING : (x2 - x1) / 2;
      const xEnd = Math.min(plotW, x2 - actualPadding);
      if (xEnd <= xStart) continue;

      ctx.save();
      ctx.strokeStyle = color;
      ctx.lineWidth = isInternal ? 1 : 1.5;
      ctx.setLineDash(isInternal ? [3, 3] : [4, 3]);
      ctx.globalAlpha = isInternal ? 0.7 : 1.0;
      ctx.beginPath();
      ctx.moveTo(xStart, y);
      ctx.lineTo(xEnd, y);
      ctx.stroke();

      ctx.setLineDash([]);
      ctx.fillStyle = color;
      ctx.font = isInternal ? '9px sans-serif' : 'bold 10px sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText(event.type, xEnd + 4, y + 3);
      ctx.restore();
    }
  }

  private drawZone(zone: PriceZone, fillColor: string, borderColor: string, label: string, mitigated: boolean | undefined, plotW: number, plotH: number): void {
    const t1 = this.toTime(zone.start_time);
    const t2 = this.toTime(zone.end_time);
    const rawX1 = this.resolveTimeX(t1);
    const rawX2 = this.resolveTimeX(t2);
    const rawY1 = this.candlestickSeries.priceToCoordinate(zone.top);
    const rawY2 = this.candlestickSeries.priceToCoordinate(zone.bottom);
    if (rawX1 === null || rawX2 === null || rawY1 === null || rawY2 === null) return;

    const x1: number = rawX1;
    const x2: number = rawX2;
    const y1: number = rawY1 as unknown as number;
    const y2: number = rawY2 as unknown as number;

    const rawRx = Math.min(x1, x2);
    const rawRight = Math.max(x1, x2);
    const ry = Math.min(y1, y2);
    const rh = Math.max(Math.abs(y2 - y1), 2);

    if (rawRight < 0 || rawRx > plotW || ry + rh < 0 || ry > plotH) return;

    const rx = Math.max(0, rawRx);
    const rw = Math.max(Math.min(plotW, rawRight) - rx, 2);
    const ctx = this.smcCtx;

    ctx.save();
    // ทำให้สีเข้มขึ้นหน่อยสำหรับ OB/FVG
    ctx.globalAlpha = mitigated ? 0.5 : 1.0;
    ctx.fillStyle = fillColor;
    ctx.fillRect(rx, ry, rw, rh);
    
    ctx.strokeStyle = borderColor;
    ctx.lineWidth = 1;
    ctx.setLineDash(mitigated ? [3, 3] : []);
    ctx.beginPath();
    // วาดเส้นขอบ บน-ล่าง
    ctx.moveTo(rx, ry); ctx.lineTo(rx + rw, ry);
    ctx.moveTo(rx, ry + rh); ctx.lineTo(rx + rw, ry + rh);
    // วาดเส้นขอบ ซ้าย-ขวา ด้วย
    ctx.moveTo(rx, ry); ctx.lineTo(rx, ry + rh);
    ctx.moveTo(rx + rw, ry); ctx.lineTo(rx + rw, ry + rh);
    ctx.stroke();

    // วาด Text เสมอ ไม่ว่ากล่องจะเล็กแค่ไหน
    ctx.fillStyle = borderColor;
    ctx.font = 'bold 10px sans-serif';
    ctx.setLineDash([]);
    // ถ้ายาวไม่พอให้เอาไว้ข้างบน
    const textY = rh > 12 ? ry + 11 : ry - 4;
    ctx.fillText(mitigated ? label + ' ✓' : label, rx + 4, textY);
    
    ctx.restore();
  }

  private drawHorizontalZone(zone: DiscountZone, fillColor: string, borderColor: string, plotW: number, plotH: number): void {
    const rawY1 = this.candlestickSeries.priceToCoordinate(zone.top);
    const rawY2 = this.candlestickSeries.priceToCoordinate(zone.bottom);
    if (rawY1 === null || rawY2 === null) return;
    const y1: number = rawY1 as unknown as number;
    const y2: number = rawY2 as unknown as number;
    const ry = Math.min(y1, y2), rh = Math.abs(y2 - y1);
    if (rh < 1 || ry + rh < 0 || ry > plotH) return;
    const ctx = this.smcCtx;
    ctx.save();
    ctx.fillStyle = fillColor;
    ctx.fillRect(0, ry, plotW, rh);
    ctx.strokeStyle = borderColor;
    ctx.lineWidth = 1;
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(0, ry); ctx.lineTo(plotW, ry);
    ctx.moveTo(0, ry + rh); ctx.lineTo(plotW, ry + rh);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = borderColor;
    ctx.font = 'bold 10px sans-serif';
    ctx.fillText(zone.label, 8, ry + 13);
    ctx.restore();
  }

  private drawEqualLine(eq: EqualLevel, color: string, label: string, plotW: number, plotH: number): void {
    const t1 = this.toTime(eq.start_time);
    const t2 = this.toTime(eq.end_time);
    const rawX1 = this.resolveTimeX(t1);
    const rawX2 = this.resolveTimeX(t2);
    const rawY  = this.candlestickSeries.priceToCoordinate(eq.price);
    if (rawX1 === null || rawX2 === null || rawY === null) return;
    const x1: number = rawX1;
    const x2: number = rawX2;
    const y: number  = rawY as unknown as number;
    if ((x1 < 0 && x2 < 0) || (x1 > plotW && x2 > plotW)) return;
    if (y < 0 || y > plotH) return;
    const ctx = this.smcCtx;
    ctx.save();
    ctx.strokeStyle = color;
    ctx.lineWidth = 1;
    ctx.setLineDash([2, 3]);
    ctx.beginPath();
    ctx.moveTo(Math.max(0, x1), y);
    ctx.lineTo(Math.min(plotW, x2), y);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = color;
    ctx.font = 'bold 9px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(label, (Math.max(0, x1) + Math.min(plotW, x2)) / 2, y - 3);
    ctx.textAlign = 'left';
    ctx.restore();
  }

  private clearCanvas(): void {
    if (!this.smcCtx || !this.smcCanvas) return;
    this.smcCtx.save();
    this.smcCtx.setTransform(1, 0, 0, 1, 0, 0);
    this.smcCtx.clearRect(0, 0, this.smcCanvas.width, this.smcCanvas.height);
    this.smcCtx.restore();
  }

  // ---- Toggle Methods ----
  toggleSwings():              void { this.showSwings = !this.showSwings; this.renderSmcLayers(); }
  toggleInternalSwings():      void { this.showInternalSwings = !this.showInternalSwings; this.renderSmcLayers(); }
  toggleStructure():           void { this.showStructure = !this.showStructure; this.drawSmcOverlay(); }
  toggleInternalStructure():   void { this.showInternalStructure = !this.showInternalStructure; this.drawSmcOverlay(); }
  toggleOrderBlocks():         void { this.showOrderBlocks = !this.showOrderBlocks; this.drawSmcOverlay(); }
  toggleInternalOrderBlocks(): void { this.showInternalOrderBlocks = !this.showInternalOrderBlocks; this.drawSmcOverlay(); }
  toggleFVG():                 void { this.showFVG = !this.showFVG; this.drawSmcOverlay(); }
  toggleEqualHL():             void { this.showEqualHL = !this.showEqualHL; this.drawSmcOverlay(); }
  toggleZones():               void { this.showZones = !this.showZones; this.drawSmcOverlay(); }
  toggleStrongWeakHL():        void { this.showStrongWeakHL = !this.showStrongWeakHL; this.renderSmcLayers(); }

  // ---- Real-time Live Update ----

  private startLiveUpdate(): void {
    this.stopLiveUpdate(); // ล้าง interval เก่าก่อน
    if (!this.isLive) return;
    this.liveInterval = setInterval(() => {
      this.pollLiveCandle();
    }, 5000); // ทุก 5 วินาที
  }

  private stopLiveUpdate(): void {
    if (this.liveInterval) {
      clearInterval(this.liveInterval);
      this.liveInterval = null;
    }
  }

  private pollLiveCandle(): void {
    if (!this.candlestickSeries) return;
    this.marketData.getLiveCandle(this.activeSymbol, this.activeTimeframe).subscribe({
      next: (res) => {
        this.currentPrice = res.current_price;
        if (!res.candles || res.candles.length === 0) return;
        // อัปเดตแท่งเทียนล่าสุดบน chart เฉพาะแท่งที่เวลา >= แท่งล่าสุด
        for (const c of res.candles) {
          const t = Math.floor(new Date(c.time_stamp).getTime() / 1000);
          if (t >= this.lastChartTime) {
            const bar = {
              time: t as Time,
              open:  c.open_price,
              high:  c.high_price,
              low:   c.low_price,
              close: c.close_price,
            };
            this.candlestickSeries.update(bar);
            this.lastChartTime = t; // อัปเดตเผื่อขึ้นแท่งใหม่
          }
        }
        this.drawSmcOverlay();
      },
      error: () => { /* ไม่แสดง error เพื่อไม่ให้รบกวน UI */ },
    });
  }

  toggleLive(): void {
    this.isLive = !this.isLive;
    if (this.isLive) {
      this.startLiveUpdate();
    } else {
      this.stopLiveUpdate();
    }
  }

  formatPrice(price: number): string {
    let decimals = 5;
    if (this.activeSymbol.includes('JPY')) decimals = 3;
    else if (this.activeSymbol.includes('XAU') || this.activeSymbol.includes('GOLD')) decimals = 2;
    return price.toFixed(decimals);
  }
}

