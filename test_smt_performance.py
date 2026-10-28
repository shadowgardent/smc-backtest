import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

from services.mt5_service import get_market_df
from services.smc_engine import (
    calc_atr,
    detect_swings,
    detect_structure,
    detect_order_blocks,
    detect_fvg,
)

def calc_rsi(closes: np.ndarray, period: int = 14) -> np.ndarray:
    n = len(closes)
    rsi = np.full(n, 50.0)
    if n <= period:
        return rsi
    deltas = np.diff(closes)
    gains = np.where(deltas > 0, deltas, 0.0)
    losses = np.where(deltas < 0, -deltas, 0.0)
    
    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])
    if avg_loss == 0:
        rsi[period] = 100.0
    else:
        rs = avg_gain / avg_loss
        rsi[period] = 100.0 - (100.0 / (1.0 + rs))
        
    for i in range(period + 1, n):
        gain = gains[i - 1]
        loss = losses[i - 1]
        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period
        if avg_loss == 0:
            rsi[i] = 100.0
        else:
            rs = avg_gain / avg_loss
            rsi[i] = 100.0 - (100.0 / (1.0 + rs))
    return rsi

def detect_smt_divergence(
    df_primary: pd.DataFrame,
    df_corr: pd.DataFrame | None = None,
    swing_period: int = 5
) -> dict:
    """
    ตรวจจับ SMT Divergence ทั้งแบบ Intermarket (ICT SMT) และ Momentum SMT (RSI Divergence)
    คืนค่า dict ของแท่งเทียนที่เกิด SMT:
    {
        candle_idx: {
            "type": "bullish" | "bearish",
            "smt_type": "intermarket" | "momentum" | "both",
            "desc": str
        }
    }
    """
    highs = df_primary["high_price"].values
    lows = df_primary["low_price"].values
    closes = df_primary["close_price"].values
    n = len(df_primary)
    
    # 1. Swings บน Primary Asset
    shs, sls = detect_swings(df_primary, n=swing_period)
    
    # คำนวณ RSI สำหรับ Momentum SMT
    rsi = calc_rsi(closes, period=14)
    
    # ตรวจจับ Intermarket SMT หากมีข้อมูล Correlated Asset
    corr_highs = None
    corr_lows = None
    if df_corr is not None and len(df_corr) == n:
        corr_highs = df_corr["high_price"].values
        corr_lows = df_corr["low_price"].values
        
    smt_signals = {}
    
    # Bullish SMT: เปรียบเทียบ Swing Lows ติดกัน
    # เมื่อราคาทำ Lower Low (LL) แต่ Correlated Asset ทำ Higher Low (HL) หรือ RSI ทำ Higher Low
    for i in range(1, len(sls)):
        curr_sl = sls[i]
        prev_sl = sls[i - 1]
        curr_idx = curr_sl["idx"]
        prev_idx = prev_sl["idx"]
        
        # เงื่อนไขราคาทำ Lower Low
        price_ll = curr_sl["price"] < prev_sl["price"]
        
        is_intermarket_bull_smt = False
        if corr_lows is not None:
            # Correlated Asset Low ในช่วง window
            c_curr_low = np.min(corr_lows[max(0, curr_idx - swing_period): min(n, curr_idx + swing_period + 1)])
            c_prev_low = np.min(corr_lows[max(0, prev_idx - swing_period): min(n, prev_idx + swing_period + 1)])
            # Divergence: Primary ทำ LL แต่ Correlated ทำ HL (หรือไม่ยอมลงทำ New Low)
            if price_ll and c_curr_low > c_prev_low:
                is_intermarket_bull_smt = True
            elif not price_ll and c_curr_low < c_prev_low: # Primary ทำ HL แต่ Correlated ทำ LL (Swept Liquidity)
                is_intermarket_bull_smt = True

        # Momentum SMT: Price LL แต่ RSI HL
        is_momentum_bull_smt = False
        if price_ll and rsi[curr_idx] > rsi[prev_idx]:
            is_momentum_bull_smt = True
            
        if is_intermarket_bull_smt or is_momentum_bull_smt:
            smt_type = "both" if (is_intermarket_bull_smt and is_momentum_bull_smt) else ("intermarket" if is_intermarket_bull_smt else "momentum")
            # บันทึกสัญญาณในช่วงตั้งแต่ swing low จนถึง swing low + 20 แท่ง
            for k in range(curr_idx, min(n, curr_idx + 25)):
                smt_signals[k] = {
                    "direction": "bullish",
                    "smt_type": smt_type,
                    "swing_idx": curr_idx
                }

    # Bearish SMT: เปรียบเทียบ Swing Highs ติดกัน
    # เมื่อราคาทำ Higher High (HH) แต่ Correlated Asset ทำ Lower High (LH) หรือ RSI ทำ Lower High
    for i in range(1, len(shs)):
        curr_sh = shs[i]
        prev_sh = shs[i - 1]
        curr_idx = curr_sh["idx"]
        prev_idx = prev_sh["idx"]
        
        price_hh = curr_sh["price"] > prev_sh["price"]
        
        is_intermarket_bear_smt = False
        if corr_highs is not None:
            c_curr_high = np.max(corr_highs[max(0, curr_idx - swing_period): min(n, curr_idx + swing_period + 1)])
            c_prev_high = np.max(corr_highs[max(0, prev_idx - swing_period): min(n, prev_idx + swing_period + 1)])
            if price_hh and c_curr_high < c_prev_high:
                is_intermarket_bear_smt = True
            elif not price_hh and c_curr_high > c_prev_high:
                is_intermarket_bear_smt = True
                
        is_momentum_bear_smt = False
        if price_hh and rsi[curr_idx] < rsi[prev_idx]:
            is_momentum_bear_smt = True
            
        if is_intermarket_bear_smt or is_momentum_bear_smt:
            smt_type = "both" if (is_intermarket_bear_smt and is_momentum_bear_smt) else ("intermarket" if is_intermarket_bear_smt else "momentum")
            for k in range(curr_idx, min(n, curr_idx + 25)):
                smt_signals[k] = {
                    "direction": "bearish",
                    "smt_type": smt_type,
                    "swing_idx": curr_idx
                }
                
    return smt_signals

def run_backtest_with_smt(
    df: pd.DataFrame,
    df_corr: pd.DataFrame | None = None,
    use_smt_filter: bool = False,
    smt_mode: str = "any", # "intermarket", "momentum", "any"
    max_trades: int = 300,
    risk_reward_ratio: float = 3.0,
    tp1_rr: float = 1.5,
    tp2_rr: float = 3.0,
    use_htf_filter: bool = True
):
    atr = calc_atr(df)
    swing_highs, swing_lows = detect_swings(df, n=5)
    structure_events = detect_structure(df, swing_highs, swing_lows)
    order_blocks = detect_order_blocks(df, structure_events, atr=atr, limit=None)
    fvgs = detect_fvg(df, limit=None)
    
    smt_signals = detect_smt_divergence(df, df_corr, swing_period=5) if use_smt_filter else {}
    
    highs = df["high_price"].values
    lows = df["low_price"].values
    closes = df["close_price"].values
    opens = df["open_price"].values
    times = [str(t) for t in df["time_stamp"]]
    ema200 = pd.Series(closes).ewm(span=200, adjust=False).mean().values if use_htf_filter else None
    
    capital = 10000.0
    initial_capital = capital
    peak_capital = capital
    max_dd = 0.0
    trades = []
    
    chochs = [e for e in structure_events if e["type"] == "CHoCH"]
    
    for choch in chochs:
        if len(trades) >= max_trades:
            break
            
        c_idx = choch["idx"]
        c_dir = choch["direction"]
        
        # HTF EMA 200 filter
        if use_htf_filter and ema200 is not None:
            if c_dir == "bullish" and closes[c_idx] < ema200[c_idx]:
                continue
            if c_dir == "bearish" and closes[c_idx] > ema200[c_idx]:
                continue
                
        # SMT Filter check at or around CHoCH
        if use_smt_filter:
            # ตรวจสอบว่ามี SMT signal ทิศทางเดียวกับ CHoCH ในช่วงใกล้เคียง [c_idx - 15, c_idx + 5]
            has_smt = False
            for look_back in range(max(0, c_idx - 15), min(len(df), c_idx + 6)):
                sig = smt_signals.get(look_back)
                if sig and sig["direction"] == c_dir:
                    if smt_mode == "any":
                        has_smt = True
                        break
                    elif smt_mode == "intermarket" and sig["smt_type"] in ["intermarket", "both"]:
                        has_smt = True
                        break
                    elif smt_mode == "momentum" and sig["smt_type"] in ["momentum", "both"]:
                        has_smt = True
                        break
            if not has_smt:
                continue

        rel_obs = [o for o in order_blocks if o["type"] == c_dir and o.get("idx", 0) <= c_idx and c_idx - o.get("idx", 0) <= 35]
        rel_fvgs = [f for f in fvgs if f["type"] == c_dir and f.get("idx", 0) <= c_idx and c_idx - f.get("idx", 0) <= 35]
        
        for i in range(c_idx + 1, min(c_idx + 60, len(df))):
            curr_low = lows[i]
            curr_high = highs[i]
            curr_atr = atr[i] if i < len(atr) else 0.0010
            if curr_atr <= 0:
                curr_atr = 0.0010
                
            triggered = None
            if c_dir == "bullish":
                for f in rel_fvgs:
                    if curr_low <= f["top"] and curr_high >= f["bottom"]:
                        triggered = ("FVG", f["top"], f["bottom"])
                        break
                if not triggered:
                    for o in rel_obs:
                        if curr_low <= o["top"] and curr_high >= o["bottom"]:
                            triggered = ("OB", o["top"], o["bottom"])
                            break
            else:
                for f in rel_fvgs:
                    if curr_high >= f["bottom"] and curr_low <= f["top"]:
                        triggered = ("FVG", f["top"], f["bottom"])
                        break
                if not triggered:
                    for o in rel_obs:
                        if curr_high >= o["bottom"] and curr_low <= o["top"]:
                            triggered = ("OB", o["top"], o["bottom"])
                            break
                            
            if triggered:
                z_type, z_top, z_bottom = triggered
                
                # Setup trade (Hybrid Partial TP)
                if c_dir == "bullish":
                    entry = z_top
                    sl = z_bottom - (0.2 * curr_atr)
                    risk_dist = entry - sl
                    if risk_dist <= 0:
                        continue
                    tp1 = entry + (risk_dist * tp1_rr)
                    tp2 = entry + (risk_dist * tp2_rr)
                    
                    # Simulation forward
                    t1_hit = False
                    full_win = False
                    partial_win = False
                    loss = False
                    
                    for k in range(i + 1, min(i + 120, len(df))):
                        bar_h = highs[k]
                        bar_l = lows[k]
                        if not t1_hit:
                            if bar_l <= sl:
                                loss = True
                                break
                            elif bar_h >= tp1:
                                t1_hit = True
                                if bar_h >= tp2:
                                    full_win = True
                                    break
                        else:
                            if bar_h >= tp2:
                                full_win = True
                                break
                            elif bar_l <= entry:
                                partial_win = True
                                break
                                
                    if not (full_win or partial_win or loss):
                        if t1_hit: partial_win = True
                        else: loss = True
                        
                else: # bearish
                    entry = z_bottom
                    sl = z_top + (0.2 * curr_atr)
                    risk_dist = sl - entry
                    if risk_dist <= 0:
                        continue
                    tp1 = entry - (risk_dist * tp1_rr)
                    tp2 = entry - (risk_dist * tp2_rr)
                    
                    t1_hit = False
                    full_win = False
                    partial_win = False
                    loss = False
                    
                    for k in range(i + 1, min(i + 120, len(df))):
                        bar_h = highs[k]
                        bar_l = lows[k]
                        if not t1_hit:
                            if bar_h >= sl:
                                loss = True
                                break
                            elif bar_l <= tp1:
                                t1_hit = True
                                if bar_l <= tp2:
                                    full_win = True
                                    break
                        else:
                            if bar_l <= tp2:
                                full_win = True
                                break
                            elif bar_h >= entry:
                                partial_win = True
                                break
                                
                    if not (full_win or partial_win or loss):
                        if t1_hit: partial_win = True
                        else: loss = True
                        
                risk_cash = capital * 0.01
                if full_win:
                    pnl = risk_cash * 2.25
                    res_type = "FULL_WIN"
                elif partial_win:
                    pnl = risk_cash * 0.75
                    res_type = "PARTIAL_WIN"
                else:
                    pnl = -risk_cash
                    res_type = "LOSS"
                    
                capital += pnl
                if capital > peak_capital:
                    peak_capital = capital
                dd = (peak_capital - capital) / peak_capital * 100
                if dd > max_dd:
                    max_dd = dd
                    
                trades.append({
                    "res": res_type,
                    "pnl": pnl,
                })
                break # 1 trade per CHoCH
                
    total = len(trades)
    if total == 0:
        return {"total": 0, "win_rate": 0, "pf": 0, "net_profit": 0, "max_dd": 0}
        
    full_wins = sum(1 for t in trades if t["res"] == "FULL_WIN")
    part_wins = sum(1 for t in trades if t["res"] == "PARTIAL_WIN")
    losses = sum(1 for t in trades if t["res"] == "LOSS")
    wins = full_wins + part_wins
    win_rate = (wins / total) * 100
    
    gross_win = sum(t["pnl"] for t in trades if t["pnl"] > 0)
    gross_loss = abs(sum(t["pnl"] for t in trades if t["pnl"] < 0))
    pf = (gross_win / gross_loss) if gross_loss > 0 else 99.0
    net_profit = capital - initial_capital
    roi = (net_profit / initial_capital) * 100
    
    return {
        "total": total,
        "full_wins": full_wins,
        "part_wins": part_wins,
        "losses": losses,
        "win_rate": win_rate,
        "pf": pf,
        "net_profit": net_profit,
        "roi": roi,
        "max_dd": max_dd
    }

if __name__ == "__main__":
    bars = 35000
    print(f"Loading {bars} M15 bars from MT5...")
    df_eur = get_market_df("EURUSD", "M15", bars)
    df_gbp = get_market_df("GBPUSD", "M15", bars)
    df_gold = get_market_df("XAUUSD", "M15", bars)
    
    # 1. Test EURUSD
    print("\n=================== EURUSD (Correlated Pair: GBPUSD) ===================")
    r_eur_base = run_backtest_with_smt(df_eur, use_smt_filter=False)
    r_eur_inter = run_backtest_with_smt(df_eur, df_corr=df_gbp, use_smt_filter=True, smt_mode="intermarket")
    r_eur_mom = run_backtest_with_smt(df_eur, use_smt_filter=True, smt_mode="momentum")
    r_eur_any = run_backtest_with_smt(df_eur, df_corr=df_gbp, use_smt_filter=True, smt_mode="any")
    
    print(f"BASELINE (No SMT)   : Trades={r_eur_base['total']:3d} | WR={r_eur_base['win_rate']:.1f}% (FW:{r_eur_base['full_wins']}, PW:{r_eur_base['part_wins']}, L:{r_eur_base['losses']}) | PF={r_eur_base['pf']:.2f} | Net=${r_eur_base['net_profit']:+,.2f} | MaxDD={r_eur_base['max_dd']:.1f}%")
    print(f"+ ICT SMT (vs GBP)  : Trades={r_eur_inter['total']:3d} | WR={r_eur_inter['win_rate']:.1f}% (FW:{r_eur_inter['full_wins']}, PW:{r_eur_inter['part_wins']}, L:{r_eur_inter['losses']}) | PF={r_eur_inter['pf']:.2f} | Net=${r_eur_inter['net_profit']:+,.2f} | MaxDD={r_eur_inter['max_dd']:.1f}%")
    print(f"+ Momentum SMT (RSI): Trades={r_eur_mom['total']:3d} | WR={r_eur_mom['win_rate']:.1f}% (FW:{r_eur_mom['full_wins']}, PW:{r_eur_mom['part_wins']}, L:{r_eur_mom['losses']}) | PF={r_eur_mom['pf']:.2f} | Net=${r_eur_mom['net_profit']:+,.2f} | MaxDD={r_eur_mom['max_dd']:.1f}%")
    print(f"+ Combined SMT      : Trades={r_eur_any['total']:3d} | WR={r_eur_any['win_rate']:.1f}% (FW:{r_eur_any['full_wins']}, PW:{r_eur_any['part_wins']}, L:{r_eur_any['losses']}) | PF={r_eur_any['pf']:.2f} | Net=${r_eur_any['net_profit']:+,.2f} | MaxDD={r_eur_any['max_dd']:.1f}%")

    # 2. Test GBPUSD
    print("\n=================== GBPUSD (Correlated Pair: EURUSD) ===================")
    r_gbp_base = run_backtest_with_smt(df_gbp, use_smt_filter=False)
    r_gbp_inter = run_backtest_with_smt(df_gbp, df_corr=df_eur, use_smt_filter=True, smt_mode="intermarket")
    r_gbp_mom = run_backtest_with_smt(df_gbp, use_smt_filter=True, smt_mode="momentum")
    
    print(f"BASELINE (No SMT)   : Trades={r_gbp_base['total']:3d} | WR={r_gbp_base['win_rate']:.1f}% (FW:{r_gbp_base['full_wins']}, PW:{r_gbp_base['part_wins']}, L:{r_gbp_base['losses']}) | PF={r_gbp_base['pf']:.2f} | Net=${r_gbp_base['net_profit']:+,.2f} | MaxDD={r_gbp_base['max_dd']:.1f}%")
    print(f"+ ICT SMT (vs EUR)  : Trades={r_gbp_inter['total']:3d} | WR={r_gbp_inter['win_rate']:.1f}% (FW:{r_gbp_inter['full_wins']}, PW:{r_gbp_inter['part_wins']}, L:{r_gbp_inter['losses']}) | PF={r_gbp_inter['pf']:.2f} | Net=${r_gbp_inter['net_profit']:+,.2f} | MaxDD={r_gbp_inter['max_dd']:.1f}%")
    print(f"+ Momentum SMT (RSI): Trades={r_gbp_mom['total']:3d} | WR={r_gbp_mom['win_rate']:.1f}% (FW:{r_gbp_mom['full_wins']}, PW:{r_gbp_mom['part_wins']}, L:{r_gbp_mom['losses']}) | PF={r_gbp_mom['pf']:.2f} | Net=${r_gbp_mom['net_profit']:+,.2f} | MaxDD={r_gbp_mom['max_dd']:.1f}%")

    # 3. Test GOLD (XAUUSD)
    print("\n=================== GOLD (XAUUSD) ===================")
    r_gold_base = run_backtest_with_smt(df_gold, use_smt_filter=False)
    r_gold_mom = run_backtest_with_smt(df_gold, use_smt_filter=True, smt_mode="momentum")
    r_gold_inter = run_backtest_with_smt(df_gold, df_corr=df_eur, use_smt_filter=True, smt_mode="intermarket")
    print(f"BASELINE (No SMT)   : Trades={r_gold_base['total']:3d} | WR={r_gold_base['win_rate']:.1f}% (FW:{r_gold_base['full_wins']}, PW:{r_gold_base['part_wins']}, L:{r_gold_base['losses']}) | PF={r_gold_base['pf']:.2f} | Net=${r_gold_base['net_profit']:+,.2f} | MaxDD={r_gold_base['max_dd']:.1f}%")
    print(f"+ Momentum SMT (RSI): Trades={r_gold_mom['total']:3d} | WR={r_gold_mom['win_rate']:.1f}% (FW:{r_gold_mom['full_wins']}, PW:{r_gold_mom['part_wins']}, L:{r_gold_mom['losses']}) | PF={r_gold_mom['pf']:.2f} | Net=${r_gold_mom['net_profit']:+,.2f} | MaxDD={r_gold_mom['max_dd']:.1f}%")
    print(f"+ ICT SMT (vs EUR)  : Trades={r_gold_inter['total']:3d} | WR={r_gold_inter['win_rate']:.1f}% (FW:{r_gold_inter['full_wins']}, PW:{r_gold_inter['part_wins']}, L:{r_gold_inter['losses']}) | PF={r_gold_inter['pf']:.2f} | Net=${r_gold_inter['net_profit']:+,.2f} | MaxDD={r_gold_inter['max_dd']:.1f}%")
