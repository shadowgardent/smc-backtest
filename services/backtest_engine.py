import pandas as pd
import numpy as np
from services.smc_engine import (
    calc_atr,
    detect_swings,
    detect_structure,
    detect_order_blocks,
    detect_fvg,
    detect_smt_divergence,
)

def run_smc_backtest(
    df: pd.DataFrame,
    risk_reward_ratio: float = 2.0,
    risk_per_trade_pct: float = 1.0,
    initial_capital: float = 10000.0,
    swing_period: int = 5,
    strategy_mode: str = "choch_ob_fvg",
    max_trades: int = 100,
    use_break_even: bool = True,
    break_even_rr: float = 1.0,
    use_partial_tp: bool = False,
    tp1_rr: float = 1.5,
    tp2_rr: float = 3.0,
    use_htf_filter: bool = False,
    use_smt_filter: bool = False,
    smt_mode: str = "any",
    df_corr: pd.DataFrame | None = None,
) -> dict:
    """
    อัลกอริทึมจำลองการทำ Backtesting ตามกลยุทธ์ Smart Money Concepts
    
    Strategy Modes:
    1. 'hybrid_partial_tp' (Option 2 - High Win Rate ~60%):
       - กรองเทรนด์ Timeframe ใหญ่ (HTF EMA200 Alignment)
       - ระบบ Hybrid Partial TP: แบ่งไม้ TP1 ที่ 1.5R (50%) เพื่อการันตี Win Rate สูง
       - ไม้ Runner ที่เหลือ (50%) เลื่อนกันหน้าทุน (BE) ปล่อยรันไปชน TP2 ที่ 3.0R
       
    2. 'choch_ob_fvg' (Default Single Target):
       - ต้องเกิด Change of Character (CHoCH) ยืนยันการเปลี่ยนโครงสร้างเทรนด์
       - รอราคาย่อกลับมาทดสอบโซน Order Block (OB) หรือ Fair Value Gap (FVG)
       - ตั้ง Stop Loss ขอบโซน + ATR buffer (0.2 * ATR)
       - ระบบ Break-Even (กันหน้าทุน): เมื่อราคาวิ่งถึง break_even_rr (1:1) จะเลื่อน SL มาที่ทุน
       - วาง Take Profit ตาม Risk-to-Reward Ratio (เช่น 1:2.0, 1:3.0, 1:4.0)
       
    3. 'all_ob':
       - สแกน Order Block ทุกจุดหลังเกิด Breakout โครงสร้าง (BOS / CHoCH)
    """
    if df is None or len(df) < 50:
        return {
            "total_trades": 0,
            "win_trades": 0,
            "full_win_trades": 0,
            "partial_win_trades": 0,
            "loss_trades": 0,
            "be_trades": 0,
            "win_rate": 0.0,
            "be_rate": 0.0,
            "loss_rate": 0.0,
            "profit_factor": 1.0,
            "net_profit": 0.0,
            "net_profit_pct": 0.0,
            "max_drawdown": 0.0,
            "trades": [],
            "equity_curve": [],
            "zone_breakdown": {}
        }

    # Auto-configure flags if hybrid_partial_tp is selected
    if strategy_mode == "hybrid_partial_tp":
        use_partial_tp = True
        use_htf_filter = True
        tp2_rr = max(risk_reward_ratio, tp2_rr)

    atr = calc_atr(df)
    swing_highs, swing_lows = detect_swings(df, n=swing_period)
    structure_events = detect_structure(df, swing_highs, swing_lows)
    order_blocks = detect_order_blocks(df, structure_events, atr=atr, limit=None)
    fvgs = detect_fvg(df, limit=None)
    smt_signals = detect_smt_divergence(df, df_corr, swing_period=swing_period) if use_smt_filter else {}

    highs = df["high_price"].values
    lows = df["low_price"].values
    opens = df["open_price"].values
    closes = df["close_price"].values
    times = [str(t) for t in df["time_stamp"]]

    # HTF Trend Indicator (EMA 200)
    ema200 = pd.Series(closes).ewm(span=200, adjust=False).mean().values if use_htf_filter else None

    trades = []
    capital = initial_capital
    peak_capital = initial_capital
    max_drawdown = 0.0
    equity_curve = [{"time": times[0], "equity": round(capital, 2), "drawdown": 0.0}]

    # =========================================================================
    # Strategy 1: CHoCH + OB / FVG Retest (Single TP or Hybrid Partial TP)
    # =========================================================================
    if strategy_mode in ["choch_ob_fvg", "hybrid_partial_tp"]:
        chochs = [e for e in structure_events if e["type"] == "CHoCH"]

        for choch in chochs:
            if len(trades) >= max_trades:
                break

            c_idx = choch["idx"]
            c_dir = choch["direction"]

            # Filter 1: HTF Trend Alignment
            if use_htf_filter and ema200 is not None:
                if c_dir == "bullish" and closes[c_idx] < ema200[c_idx]:
                    continue
                if c_dir == "bearish" and closes[c_idx] > ema200[c_idx]:
                    continue

            # Filter 2: SMT Divergence Filter
            if use_smt_filter:
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

            # Candidate OBs and FVGs
            rel_obs = [
                o for o in order_blocks
                if o["type"] == c_dir and o.get("idx", 0) <= c_idx and c_idx - o.get("idx", 0) <= 35
            ]
            rel_fvgs = [
                f for f in fvgs
                if f["type"] == c_dir and f.get("idx", 0) <= c_idx and c_idx - f.get("idx", 0) <= 35
            ]

            # Look for pullback into zones within next 60 candles
            for i in range(c_idx + 1, min(c_idx + 60, len(df))):
                curr_low = lows[i]
                curr_high = highs[i]
                curr_atr = atr[i] if i < len(atr) else 0.0010
                if curr_atr <= 0:
                    curr_atr = 0.0010

                triggered = None
                if c_dir == "bullish":
                    # Check FVG first, then OB
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

                    # =========================================================
                    # Mode A: Hybrid Partial TP Logic (TP1 50% + TP2 50%)
                    # =========================================================
                    if use_partial_tp:
                        if c_dir == "bullish":
                            entry_price = z_top
                            sl_price = round(z_bottom - (0.2 * curr_atr), 5)
                            risk = entry_price - sl_price
                            if risk <= 0:
                                continue
                            tp1_price = round(entry_price + (risk * tp1_rr), 5)
                            tp2_price = round(entry_price + (risk * tp2_rr), 5)

                            tp1_hit = False
                            current_sl = sl_price
                            pnl_r = 0.0
                            result = "OPEN"
                            exit_price = entry_price
                            exit_time = times[-1]

                            for j in range(i + 1, len(df)):
                                bar_low = lows[j]
                                bar_high = highs[j]
                                bar_time = times[j]

                                if bar_low <= current_sl:
                                    if tp1_hit:
                                        pnl_r = 0.5 * tp1_rr + 0.5 * 0.0  # +0.75R
                                        result = "PARTIAL_WIN"
                                        exit_price = entry_price
                                    else:
                                        pnl_r = -1.0
                                        result = "LOSS"
                                        exit_price = current_sl
                                    exit_time = bar_time
                                    break

                                if not tp1_hit and bar_high >= tp1_price:
                                    tp1_hit = True
                                    current_sl = entry_price  # Move SL to BE for runner

                                if tp1_hit and bar_high >= tp2_price:
                                    pnl_r = 0.5 * tp1_rr + 0.5 * tp2_rr  # +2.25R
                                    result = "FULL_WIN"
                                    exit_price = tp2_price
                                    exit_time = bar_time
                                    break

                        else:  # Bearish
                            entry_price = z_bottom
                            sl_price = round(z_top + (0.2 * curr_atr), 5)
                            risk = sl_price - entry_price
                            if risk <= 0:
                                continue
                            tp1_price = round(entry_price - (risk * tp1_rr), 5)
                            tp2_price = round(entry_price - (risk * tp2_rr), 5)

                            tp1_hit = False
                            current_sl = sl_price
                            pnl_r = 0.0
                            result = "OPEN"
                            exit_price = entry_price
                            exit_time = times[-1]

                            for j in range(i + 1, len(df)):
                                bar_high = highs[j]
                                bar_low = lows[j]
                                bar_time = times[j]

                                if bar_high >= current_sl:
                                    if tp1_hit:
                                        pnl_r = 0.5 * tp1_rr + 0.5 * 0.0
                                        result = "PARTIAL_WIN"
                                        exit_price = entry_price
                                    else:
                                        pnl_r = -1.0
                                        result = "LOSS"
                                        exit_price = current_sl
                                    exit_time = bar_time
                                    break

                                if not tp1_hit and bar_low <= tp1_price:
                                    tp1_hit = True
                                    current_sl = entry_price

                                if tp1_hit and bar_low <= tp2_price:
                                    pnl_r = 0.5 * tp1_rr + 0.5 * tp2_rr
                                    result = "FULL_WIN"
                                    exit_price = tp2_price
                                    exit_time = bar_time
                                    break

                        tp_price = tp2_price

                    # =========================================================
                    # Mode B: Standard Single TP Logic (with Break-Even)
                    # =========================================================
                    else:
                        if c_dir == "bullish":
                            entry_price = z_top
                            sl_price = round(z_bottom - (0.2 * curr_atr), 5)
                            risk = entry_price - sl_price
                            if risk <= 0:
                                continue
                            tp_price = round(entry_price + (risk * risk_reward_ratio), 5)
                            be_trigger_price = round(entry_price + (risk * break_even_rr), 5) if use_break_even else None

                            result = "OPEN"
                            pnl_r = 0.0
                            exit_price = entry_price
                            exit_time = times[-1]
                            current_sl = sl_price
                            is_be_activated = False

                            for j in range(i + 1, len(df)):
                                bar_low = lows[j]
                                bar_high = highs[j]
                                bar_time = times[j]

                                if bar_low <= current_sl:
                                    if is_be_activated:
                                        result = "BE"
                                        exit_price = entry_price
                                        exit_time = bar_time
                                        pnl_r = 0.0
                                    else:
                                        result = "LOSS"
                                        exit_price = current_sl
                                        exit_time = bar_time
                                        pnl_r = -1.0
                                    break

                                if use_break_even and not is_be_activated and bar_high >= be_trigger_price:
                                    is_be_activated = True
                                    current_sl = entry_price

                                if bar_high >= tp_price:
                                    result = "WIN"
                                    exit_price = tp_price
                                    exit_time = bar_time
                                    pnl_r = risk_reward_ratio
                                    break

                        else:  # Bearish
                            entry_price = z_bottom
                            sl_price = round(z_top + (0.2 * curr_atr), 5)
                            risk = sl_price - entry_price
                            if risk <= 0:
                                continue
                            tp_price = round(entry_price - (risk * risk_reward_ratio), 5)
                            be_trigger_price = round(entry_price - (risk * break_even_rr), 5) if use_break_even else None

                            result = "OPEN"
                            pnl_r = 0.0
                            exit_price = entry_price
                            exit_time = times[-1]
                            current_sl = sl_price
                            is_be_activated = False

                            for j in range(i + 1, len(df)):
                                bar_high = highs[j]
                                bar_low = lows[j]
                                bar_time = times[j]

                                if bar_high >= current_sl:
                                    if is_be_activated:
                                        result = "BE"
                                        exit_price = entry_price
                                        exit_time = bar_time
                                        pnl_r = 0.0
                                    else:
                                        result = "LOSS"
                                        exit_price = current_sl
                                        exit_time = bar_time
                                        pnl_r = -1.0
                                    break

                                if use_break_even and not is_be_activated and bar_low <= be_trigger_price:
                                    is_be_activated = True
                                    current_sl = entry_price

                                if bar_low <= tp_price:
                                    result = "WIN"
                                    exit_price = tp_price
                                    exit_time = bar_time
                                    pnl_r = risk_reward_ratio
                                    break

                    risk_cash = capital * (risk_per_trade_pct / 100.0)
                    pnl_cash = risk_cash * pnl_r
                    capital += pnl_cash
                    peak_capital = max(peak_capital, capital)
                    dd = (peak_capital - capital) / peak_capital * 100.0 if peak_capital > 0 else 0.0
                    max_drawdown = max(max_drawdown, dd)

                    trades.append({
                        "id": len(trades) + 1,
                        "setup": "CHoCH",
                        "entry_zone": z_type,
                        "type": "BUY" if c_dir == "bullish" else "SELL",
                        "entry_time": times[i],
                        "exit_time": exit_time,
                        "entry_price": entry_price,
                        "sl_price": sl_price,
                        "tp_price": tp_price,
                        "exit_price": exit_price,
                        "r_multiple": round(pnl_r, 2),
                        "pnl_cash": round(pnl_cash, 2),
                        "result": result,
                    })

                    equity_curve.append({
                        "time": exit_time,
                        "equity": round(capital, 2),
                        "drawdown": round(dd, 2)
                    })
                    break

    # =========================================================================
    # Strategy 2: All Order Blocks Retest Mode
    # =========================================================================
    else:
        executed_ob_keys = set()
        order_blocks_sorted = sorted(order_blocks, key=lambda x: x.get("idx", 0))

        for ob in order_blocks_sorted:
            if len(trades) >= max_trades:
                break
            start_idx = ob.get("idx", 0)
            event_idx = ob.get("event_idx", start_idx + 1)

            ob_key = (ob["type"], ob["top"], ob["bottom"], start_idx)
            if ob_key in executed_ob_keys:
                continue

            ob_top = ob["top"]
            ob_bot = ob["bottom"]
            ob_type = ob["type"]

            for i in range(event_idx + 1, len(df)):
                curr_low = lows[i]
                curr_high = highs[i]
                curr_time = times[i]
                curr_atr = atr[i] if i < len(atr) else (ob_top - ob_bot)
                if curr_atr <= 0:
                    curr_atr = (ob_top - ob_bot) or 0.0010

                if ob_type == "bullish":
                    if curr_low <= ob_top and curr_high >= ob_bot:
                        entry_price = ob_top
                        sl_price = round(ob_bot - (0.2 * curr_atr), 5)
                        risk = entry_price - sl_price
                        if risk <= 0:
                            break
                        tp_price = round(entry_price + (risk * risk_reward_ratio), 5)
                        be_trigger_price = round(entry_price + (risk * break_even_rr), 5) if use_break_even else None

                        result = "OPEN"
                        pnl_r = 0.0
                        exit_price = entry_price
                        exit_time = times[-1]
                        current_sl = sl_price
                        is_be_activated = False

                        for j in range(i + 1, len(df)):
                            bar_low = lows[j]
                            bar_high = highs[j]
                            bar_time = times[j]

                            if bar_low <= current_sl:
                                if is_be_activated:
                                    result = "BE"
                                    exit_price = entry_price
                                    exit_time = bar_time
                                    pnl_r = 0.0
                                else:
                                    result = "LOSS"
                                    exit_price = current_sl
                                    exit_time = bar_time
                                    pnl_r = -1.0
                                break

                            if use_break_even and not is_be_activated and bar_high >= be_trigger_price:
                                is_be_activated = True
                                current_sl = entry_price

                            if bar_high >= tp_price:
                                result = "WIN"
                                exit_price = tp_price
                                exit_time = bar_time
                                pnl_r = risk_reward_ratio
                                break

                        if result == "OPEN":
                            exit_price = round(closes[-1], 5)
                            exit_time = times[-1]
                            pnl_r = round((exit_price - entry_price) / risk, 2)
                            result = "WIN" if pnl_r > 0 else "LOSS"

                        risk_cash = capital * (risk_per_trade_pct / 100.0)
                        pnl_cash = risk_cash * pnl_r
                        capital += pnl_cash
                        peak_capital = max(peak_capital, capital)
                        dd = (peak_capital - capital) / peak_capital * 100.0 if peak_capital > 0 else 0.0
                        max_drawdown = max(max_drawdown, dd)

                        trades.append({
                            "id": len(trades) + 1,
                            "setup": ob.get("event_type", "BOS"),
                            "entry_zone": "OB",
                            "type": "BUY",
                            "entry_time": curr_time,
                            "exit_time": exit_time,
                            "entry_price": entry_price,
                            "sl_price": sl_price,
                            "tp_price": tp_price,
                            "exit_price": exit_price,
                            "r_multiple": round(pnl_r, 2),
                            "pnl_cash": round(pnl_cash, 2),
                            "result": result,
                        })

                        equity_curve.append({
                            "time": exit_time,
                            "equity": round(capital, 2),
                            "drawdown": round(dd, 2)
                        })
                        executed_ob_keys.add(ob_key)
                        break

                elif ob_type == "bearish":
                    if curr_high >= ob_bot and curr_low <= ob_top:
                        entry_price = ob_bot
                        sl_price = round(ob_top + (0.2 * curr_atr), 5)
                        risk = sl_price - entry_price
                        if risk <= 0:
                            break
                        tp_price = round(entry_price - (risk * risk_reward_ratio), 5)
                        be_trigger_price = round(entry_price - (risk * break_even_rr), 5) if use_break_even else None

                        result = "OPEN"
                        pnl_r = 0.0
                        exit_price = entry_price
                        exit_time = times[-1]
                        current_sl = sl_price
                        is_be_activated = False

                        for j in range(i + 1, len(df)):
                            bar_high = highs[j]
                            bar_low = lows[j]
                            bar_time = times[j]

                            if bar_high >= current_sl:
                                if is_be_activated:
                                    result = "BE"
                                    exit_price = entry_price
                                    exit_time = bar_time
                                    pnl_r = 0.0
                                else:
                                    result = "LOSS"
                                    exit_price = current_sl
                                    exit_time = bar_time
                                    pnl_r = -1.0
                                break

                            if use_break_even and not is_be_activated and bar_low <= be_trigger_price:
                                is_be_activated = True
                                current_sl = entry_price

                            if bar_low <= tp_price:
                                result = "WIN"
                                exit_price = tp_price
                                exit_time = bar_time
                                pnl_r = risk_reward_ratio
                                break

                        if result == "OPEN":
                            exit_price = round(closes[-1], 5)
                            exit_time = times[-1]
                            pnl_r = round((entry_price - exit_price) / risk, 2)
                            result = "WIN" if pnl_r > 0 else "LOSS"

                        risk_cash = capital * (risk_per_trade_pct / 100.0)
                        pnl_cash = risk_cash * pnl_r
                        capital += pnl_cash
                        peak_capital = max(peak_capital, capital)
                        dd = (peak_capital - capital) / peak_capital * 100.0 if peak_capital > 0 else 0.0
                        max_drawdown = max(max_drawdown, dd)

                        trades.append({
                            "id": len(trades) + 1,
                            "setup": ob.get("event_type", "BOS"),
                            "entry_zone": "OB",
                            "type": "SELL",
                            "entry_time": curr_time,
                            "exit_time": exit_time,
                            "entry_price": entry_price,
                            "sl_price": sl_price,
                            "tp_price": tp_price,
                            "exit_price": exit_price,
                            "r_multiple": round(pnl_r, 2),
                            "pnl_cash": round(pnl_cash, 2),
                            "result": result,
                        })

                        equity_curve.append({
                            "time": exit_time,
                            "equity": round(capital, 2),
                            "drawdown": round(dd, 2)
                        })
                        executed_ob_keys.add(ob_key)
                        break

    # Metrics computation
    total_trades = len(trades)
    winning_trades = [t for t in trades if t["result"] in ["WIN", "FULL_WIN", "PARTIAL_WIN"]]
    full_wins = [t for t in trades if t["result"] in ["WIN", "FULL_WIN"]]
    part_wins = [t for t in trades if t["result"] == "PARTIAL_WIN"]
    losses = [t for t in trades if t["result"] == "LOSS"]
    bes = [t for t in trades if t["result"] == "BE"]

    win_count = len(winning_trades)
    full_win_count = len(full_wins)
    part_win_count = len(part_wins)
    loss_count = len(losses)
    be_count = len(bes)

    win_rate = round((win_count / total_trades * 100.0), 2) if total_trades > 0 else 0.0
    be_rate = round((be_count / total_trades * 100.0), 2) if total_trades > 0 else 0.0
    loss_rate = round((loss_count / total_trades * 100.0), 2) if total_trades > 0 else 0.0

    gross_profit = sum(t["pnl_cash"] for t in winning_trades)
    gross_loss = abs(sum(t["pnl_cash"] for t in losses))
    profit_factor = round((gross_profit / max(gross_loss, 1.0)), 2) if gross_loss > 0 else (round(gross_profit, 2) if gross_profit > 0 else 1.0)
    net_profit = round(capital - initial_capital, 2)
    net_profit_pct = round(((capital - initial_capital) / initial_capital) * 100.0, 2)

    # Zone Breakdown (OB vs FVG)
    ob_trades = [t for t in trades if t.get("entry_zone") == "OB"]
    fvg_trades = [t for t in trades if t.get("entry_zone") == "FVG"]
    ob_wins = len([t for t in ob_trades if t["result"] in ["WIN", "FULL_WIN", "PARTIAL_WIN"]])
    ob_bes = len([t for t in ob_trades if t["result"] == "BE"])
    fvg_wins = len([t for t in fvg_trades if t["result"] in ["WIN", "FULL_WIN", "PARTIAL_WIN"]])
    fvg_bes = len([t for t in fvg_trades if t["result"] == "BE"])

    zone_breakdown = {
        "ob_total": len(ob_trades),
        "ob_wins": ob_wins,
        "ob_bes": ob_bes,
        "ob_win_rate": round(ob_wins / len(ob_trades) * 100.0, 1) if ob_trades else 0.0,
        "fvg_total": len(fvg_trades),
        "fvg_wins": fvg_wins,
        "fvg_bes": fvg_bes,
        "fvg_win_rate": round(fvg_wins / len(fvg_trades) * 100.0, 1) if fvg_trades else 0.0,
    }

    return {
        "strategy": strategy_mode,
        "initial_capital": initial_capital,
        "final_capital": round(capital, 2),
        "net_profit": net_profit,
        "net_profit_pct": net_profit_pct,
        "total_trades": total_trades,
        "win_trades": win_count,
        "full_win_trades": full_win_count,
        "partial_win_trades": part_win_count,
        "loss_trades": loss_count,
        "be_trades": be_count,
        "win_rate": win_rate,
        "be_rate": be_rate,
        "loss_rate": loss_rate,
        "profit_factor": profit_factor,
        "max_drawdown": round(max_drawdown, 2),
        "risk_reward_ratio": risk_reward_ratio,
        "use_break_even": use_break_even,
        "break_even_rr": break_even_rr,
        "use_partial_tp": use_partial_tp,
        "tp1_rr": tp1_rr,
        "tp2_rr": tp2_rr,
        "use_htf_filter": use_htf_filter,
        "use_smt_filter": use_smt_filter,
        "smt_mode": smt_mode,
        "trades": trades,
        "equity_curve": equity_curve,
        "zone_breakdown": zone_breakdown,
    }
