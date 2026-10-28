import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// ---- Candlestick Data ----

export interface MarketDataResponse {
  symbol: string;
  timeframe: string;
  total_candles: number;
  data: MarketCandle[];
}

export interface MarketCandle {
  time_stamp: string;
  open_price: number;
  high_price: number;
  low_price: number;
  close_price: number;
}

// ---- SMC Data ----

export interface SwingPoint {
  time: string;
  price: number;
}

export interface StructureEvent {
  time: string;
  swing_time: string;
  price: number;
  type: 'BOS' | 'CHoCH';
  direction: 'bullish' | 'bearish';
  label: string;
}

export interface PriceZone {
  type: 'bullish' | 'bearish';
  start_time: string;
  end_time: string;
  top: number;
  bottom: number;
  mitigated?: boolean;
}

export interface EqualLevel {
  start_time: string;
  end_time: string;
  price: number;
}

export interface DiscountZone {
  top: number;
  bottom: number;
  label: string;
}

export interface Zones {
  premium?: DiscountZone;
  equilibrium?: DiscountZone;
  discount?: DiscountZone;
}

export interface StrongWeakHL {
  time: string;
  price: number;
  label: string;
}

export interface SmcDataResponse {
  symbol: string;
  timeframe: string;
  swing_highs: SwingPoint[];
  swing_lows: SwingPoint[];
  internal_highs: SwingPoint[];
  internal_lows: SwingPoint[];
  swing_structure: StructureEvent[];
  internal_structure: StructureEvent[];
  order_blocks: PriceZone[];
  internal_order_blocks: PriceZone[];
  fvgs: PriceZone[];
  equal_highs: EqualLevel[];
  equal_lows: EqualLevel[];
  zones: Zones;
  strong_weak_hl: {
    strong_high?: StrongWeakHL;
    strong_low?: StrongWeakHL;
  };
}

// ---- Service ----

export interface LiveCandle {
  time_stamp: string;
  open_price: number;
  high_price: number;
  low_price: number;
  close_price: number;
  volume: number;
}

export interface LiveCandleResponse {
  symbol: string;
  timeframe: string;
  current_price: number | null;
  candles: LiveCandle[];
}

export interface DashboardResponse {
  symbol: string;
  trends: {
    W1: string;
    D1: string;
    H4: string;
    H1: string;
    M30: string;
    M15: string;
    M5: string;
  };
  score: number;
  signal: string;
  recommendation: string;
  radar_signals: string[];
  pd_status: string;
  liquidity_targets: {
    upside: number | null;
    downside: number | null;
  };
}

@Injectable({
  providedIn: 'root',
})
export class MarketData {
  private apiUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) {}

  getMarketData(symbol: string, timeframe: string, bars: number = 1000): Observable<MarketDataResponse> {
    return this.http.get<MarketDataResponse>(
      `${this.apiUrl}/data/${symbol}?timeframe=${timeframe}&bars=${bars}`
    );
  }

  getSmcData(symbol: string, timeframe: string): Observable<SmcDataResponse> {
    return this.http.get<SmcDataResponse>(
      `${this.apiUrl}/smc/${symbol}?timeframe=${timeframe}`
    );
  }

  getLiveCandle(symbol: string, timeframe: string): Observable<LiveCandleResponse> {
    return this.http.get<LiveCandleResponse>(
      `${this.apiUrl}/live/${symbol}?timeframe=${timeframe}`
    );
  }

  getDashboardData(symbol: string): Observable<DashboardResponse> {
    return this.http.get<DashboardResponse>(
      `${this.apiUrl}/dashboard/${symbol}`
    );
  }

  runBacktest(
    symbol: string,
    timeframe: string = 'M15',
    bars: number = 10000,
    riskReward: number = 2.0,
    riskPercent: number = 1.0,
    strategyMode: string = 'choch_ob_fvg',
    maxTrades: number = 100,
    useBreakEven: boolean = true,
    breakEvenRr: number = 1.0
  ): Observable<BacktestResponse> {
    return this.http.get<BacktestResponse>(
      `${this.apiUrl}/backtest/${symbol}?timeframe=${timeframe}&bars=${bars}&risk_reward=${riskReward}&risk_percent=${riskPercent}&strategy_mode=${strategyMode}&max_trades=${maxTrades}&use_break_even=${useBreakEven}&break_even_rr=${breakEvenRr}`
    );
  }
}

export interface BacktestTrade {
  id: number;
  setup?: string;
  entry_zone?: string;
  type: 'BUY' | 'SELL';
  entry_time: string;
  exit_time: string;
  entry_price: number;
  sl_price: number;
  tp_price: number;
  exit_price: number;
  r_multiple: number;
  pnl_cash: number;
  result: 'WIN' | 'LOSS' | 'BE' | 'FULL_WIN' | 'PARTIAL_WIN';
}

export interface EquityPoint {
  time: string;
  equity: number;
  drawdown: number;
}

export interface ZoneBreakdown {
  ob_total: number;
  ob_wins: number;
  ob_win_rate: number;
  fvg_total: number;
  fvg_wins: number;
  fvg_win_rate: number;
}

export interface BacktestResponse {
  symbol: string;
  timeframe: string;
  strategy?: string;
  bars_analyzed: number;
  initial_capital: number;
  final_capital: number;
  net_profit: number;
  net_profit_pct: number;
  total_trades: number;
  win_trades: number;
  full_win_trades?: number;
  partial_win_trades?: number;
  loss_trades: number;
  be_trades?: number;
  win_rate: number;
  be_rate?: number;
  loss_rate?: number;
  profit_factor: number;
  max_drawdown: number;
  risk_reward_ratio: number;
  use_break_even?: boolean;
  break_even_rr?: number;
  use_partial_tp?: boolean;
  tp1_rr?: number;
  tp2_rr?: number;
  use_htf_filter?: boolean;
  trades: BacktestTrade[];
  equity_curve: EquityPoint[];
  zone_breakdown?: ZoneBreakdown;
}
