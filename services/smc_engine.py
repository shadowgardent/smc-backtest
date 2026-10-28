import pandas as pd
import numpy as np

# ==============================================================================
# 1. ฟังก์ชันคำนวณ Average True Range (ATR)
# หลักการทางคณิตศาสตร์: Volatility Estimation (Wilder's Smoothing / Exponential Moving Average)
# ==============================================================================
def calc_atr(df: pd.DataFrame, period: int = 14) -> np.ndarray:
    """
    [Mathematical Concept]: Wilder's Volatility Smoothing & True Range (TR)
    1. หาค่า True Range (TR) ของแต่ละแท่งเทียน:
       tr[i] = max(high[i] - low[i], abs(high[i] - close[i-1]), abs(low[i] - close[i-1]))
    2. แท่งแรกของช่วงคำนวณค่าเฉลี่ยแบบ Simple Moving Average ของค่า TR (p แท่งแรก)
    3. แท่งถัดไปคำนวณด้วยสูตร Wilder's Smoothing: (atr[i-1] * (p - 1) + tr[i]) / p
    4. เติมค่าว่างในแท่งแรกๆ ด้วยค่า ATR ตัวแรกที่คำนวณได้
    """
    high = df["high_price"].values
    low = df["low_price"].values
    close = df["close_price"].values
    n = len(df)
    tr = np.zeros(n)
    
    for i in range(1, n):
        tr[i] = max(high[i] - low[i], abs(high[i] - close[i-1]), abs(low[i] - close[i-1]))
        
    atr = np.zeros(n)
    p = min(period, n - 1)
    if p > 0:
        atr[p] = np.mean(tr[1:p+1])
        for i in range(p + 1, n):
            atr[i] = (atr[i-1] * (p - 1) + tr[i]) / p
            
    first_valid = atr[p] if p > 0 and atr[p] > 0 else (np.mean(tr[1:]) if n > 1 else 0.001)
    if first_valid <= 0:
        first_valid = 0.001
    for i in range(p):
        atr[i] = first_valid
    return atr



# ==============================================================================
# 2. ฟังก์ชันตรวจจับ Swing High และ Swing Low
# หลักการทางคณิตศาสตร์: Local Extrema Detection (Local Maxima/Minima) / Williams Fractals
# อัลกอริทึม: Sliding Window Extremum Search ขนาด (2n + 1)
# ==============================================================================
def detect_swings(df: pd.DataFrame, n: int = 5) -> tuple[list, list]:
    """
    [Mathematical Concept]: Local Maxima & Minima Detection / Rolling Peak-Valley Search
    - Swing High: High[i] == max(High[i-n : i+n+1])
    - Swing Low:  Low[i] == min(Low[i-n : i+n+1])
    1. วนลูปตรวจสอบแท่งเทียนตั้งแต่ index n ถึง length - n
    2. หา Swing High: เช็คว่าราคา high[i] == max(high[i-n:i+n+1])
    3. หา Swing Low: เช็คว่าราคา low[i] == min(low[i-n:i+n+1])
    """
    highs = df["high_price"].values
    lows = df["low_price"].values
    times = df["time_stamp"]
    length = len(df)
    swing_highs, swing_lows = [], []
    
    for i in range(n, length - n):
        if highs[i] == max(highs[i-n:i+n+1]):
            if not swing_highs or swing_highs[-1]["idx"] != i:
                swing_highs.append({"time": str(times.iloc[i]), "price": round(float(highs[i]), 5), "idx": i})
                
        if lows[i] == min(lows[i-n:i+n+1]):
            if not swing_lows or swing_lows[-1]["idx"] != i:
                swing_lows.append({"time": str(times.iloc[i]), "price": round(float(lows[i]), 5), "idx": i})
                
    return swing_highs, swing_lows


# ==============================================================================
# 3. ฟังก์ชันตรวจจับโครงสร้างตลาด (BOS vs CHoCH)
# หลักการทางคณิตศาสตร์: Threshold Crossing Detection & Finite State Machine (FSM)
# การเปลี่ยนผ่านสถานะ: State Transition {Bullish, Bearish, Neutral}
# ==============================================================================
def detect_structure(df: pd.DataFrame, swing_highs: list, swing_lows: list) -> list:
    """
    [Mathematical Concept]: Threshold Crossing & State Transition Model (FSM)
    ติดตามสถานะแนวโน้มของตลาด ('neutral', 'bullish', 'bearish')
    - ทะลุ Swing High: bearish -> CHoCH (State Flip), bullish -> BOS (State Continuation)
    - ทะลุ Swing Low: bullish -> CHoCH (State Flip), bearish -> BOS (State Continuation)
    """
    events = []
    closes = df["close_price"].values
    times = df["time_stamp"]
    sh_sorted = sorted(swing_highs, key=lambda x: x["idx"])
    sl_sorted = sorted(swing_lows, key=lambda x: x["idx"])
    trend = "neutral"
    last_broken_sh_idx = -1
    last_broken_sl_idx = -1

    for i in range(len(df)):
        close = closes[i]
        available_sh = [s for s in sh_sorted if s["idx"] < i and s["idx"] > last_broken_sh_idx]
        available_sl = [s for s in sl_sorted if s["idx"] < i and s["idx"] > last_broken_sl_idx]
        
        if available_sh:
            last_sh = available_sh[-1]
            if close > last_sh["price"]:
                event_type = "CHoCH" if trend == "bearish" else "BOS"
                events.append({
                    "time": str(times.iloc[i]),
                    "swing_time": last_sh["time"],
                    "price": last_sh["price"],
                    "type": event_type,
                    "direction": "bullish",
                    "label": event_type,
                    "idx": i
                })
                last_broken_sh_idx = last_sh["idx"]
                trend = "bullish"

        if available_sl:
            last_sl = available_sl[-1]
            if close < last_sl["price"]:
                event_type = "CHoCH" if trend == "bullish" else "BOS"
                events.append({
                    "time": str(times.iloc[i]),
                    "swing_time": last_sl["time"],
                    "price": last_sl["price"],
                    "type": event_type,
                    "direction": "bearish",
                    "label": event_type,
                    "idx": i
                })
                last_broken_sl_idx = last_sl["idx"]
                trend = "bearish"
                
    return events


# ==============================================================================
# 4. ฟังก์ชันตรวจจับ Order Blocks (OB) และ Mitigation
# หลักการทางคณิตศาสตร์ / สถิติ:
# - Change Point Detection (CPD) & Supply/Demand Clustering
# - Displacement Footprint Extraction (ย้อนหา Origin of Imbalance ก่อนเกิด Breakout)
# - Volatility Filtering ด้วย ATR (Wilder's Smoothing)
# ==============================================================================
def detect_order_blocks(
    df: pd.DataFrame,
    structure_events: list,
    use_atr_filter: bool = True,
    atr: np.ndarray | None = None,
    limit: int | None = 15,
) -> list:
    """
    [Mathematical Concept]: Change Point Detection & Origin of Displacement
    - ค้นหา Origin Candle (แท่งสีตรงข้ามสุดท้ายก่อนเกิด Breakout Impulse)
    - กรองสัญญาณหลอกด้วย ATR Threshold (ตัดแท่งที่มีความผันผวนเกินปกติ 2 * ATR)
    - ตรวจสอบ Point-in-Polygon / Interval Intersection สำหรับ Mitigation
    """
    order_blocks = []
    last_timestamp = str(df["time_stamp"].iloc[-1])
    if use_atr_filter and atr is None:
        atr = calc_atr(df)
    close_arr = df["close_price"].values
    open_arr = df["open_price"].values
    high_arr = df["high_price"].values
    low_arr = df["low_price"].values
    
    for event in structure_events:
        event_pos = event.get("idx")
        if event_pos is None:
            continue
            
        if event["direction"] == "bullish":
            for j in range(event_pos - 1, max(event_pos - 50, -1), -1):
                if j < 0: break
                if use_atr_filter and atr is not None and (high_arr[j] - low_arr[j]) >= 2 * atr[j]:
                    continue
                if close_arr[j] < open_arr[j]:
                    top = round(float(max(open_arr[j], close_arr[j])), 5)
                    bot = round(float(min(open_arr[j], close_arr[j])), 5)
                    
                    mitigated = False
                    end_time = last_timestamp
                    for k in range(event_pos, len(df)):
                        if low_arr[k] <= top:
                            mitigated = True
                            end_time = str(df["time_stamp"].iloc[k])
                            break
                            
                    order_blocks.append({
                        "type": "bullish",
                        "start_time": str(df["time_stamp"].iloc[j]),
                        "end_time": end_time,
                        "top": top,
                        "bottom": bot,
                        "mitigated": mitigated,
                        "idx": j,
                        "event_idx": event_pos,
                        "event_type": event.get("type", "BOS"),
                    })
                    break

        else:
            for j in range(event_pos - 1, max(event_pos - 50, -1), -1):
                if j < 0: break
                if use_atr_filter and atr is not None and (high_arr[j] - low_arr[j]) >= 2 * atr[j]:
                    continue
                if close_arr[j] > open_arr[j]:
                    top = round(float(max(open_arr[j], close_arr[j])), 5)
                    bot = round(float(min(open_arr[j], close_arr[j])), 5)
                    
                    mitigated = False
                    end_time = last_timestamp
                    for k in range(event_pos, len(df)):
                        if high_arr[k] >= bot:
                            mitigated = True
                            end_time = str(df["time_stamp"].iloc[k])
                            break
                            
                    order_blocks.append({
                        "type": "bearish",
                        "start_time": str(df["time_stamp"].iloc[j]),
                        "end_time": end_time,
                        "top": top,
                        "bottom": bot,
                        "mitigated": mitigated,
                        "idx": j,
                        "event_idx": event_pos,
                        "event_type": event.get("type", "BOS"),
                    })
                    break

    seen = set()
    unique = []
    for ob in reversed(order_blocks):
        key = (ob["type"], ob["top"], ob["bottom"])
        if key not in seen:
            seen.add(key)
            unique.append(ob)
            
    res = list(reversed(unique))
    if limit is not None and limit > 0:
        return res[-limit:]
    return res


# ==============================================================================
# 5. ฟังก์ชันตรวจจับ Fair Value Gap (FVG)
# หลักการทางคณิตศาสตร์: Time-Series Discontinuity Detection & Price Range Inefficiency
# เชิง Microstructure: Order Flow Imbalance (OFI) / Liquidity Void
# สถิติ: Cumulative Moving Average Momentum Filter (กรองแท่งส่งด้วย > 2 * Mean Delta)
# ==============================================================================
def detect_fvg(df: pd.DataFrame, use_auto_threshold: bool = True, limit: int | None = 30) -> list:
    """
    [Mathematical Concept]: 3-Point Time-Series Discontinuity (Range Inefficiency)
    - Bullish FVG: Low[t] > High[t-2]  (Gap = Low[t] - High[t-2] > 0)
    - Bearish FVG: High[t] < Low[t-2]  (Gap = Low[t-2] - High[t] > 0)
    - Statistical Displacement Filter: BarDelta[t-1] > 2 * Cumulative_Mean(BarDeltas)
    ตรวจจับช่องว่างสภาพคล่อง (Imbalance) จาก 3 แท่งเทียนต่อเนื่อง (c0, c1, c2)
    """
    fvgs = []
    last_timestamp = str(df["time_stamp"].iloc[-1])
    n = len(df)
    high_arr = df["high_price"].values
    low_arr = df["low_price"].values
    close_arr = df["close_price"].values
    open_arr = df["open_price"].values
    
    bar_deltas = np.abs(close_arr - open_arr) / (np.abs(open_arr) + 1e-10) * 100
    cum_mean = np.cumsum(bar_deltas) / np.arange(1, n + 1)
    
    for i in range(2, n):
        c0_high = float(high_arr[i - 2])
        c0_low = float(low_arr[i - 2])
        c2_high = float(high_arr[i])
        c2_low = float(low_arr[i])
        bar_delta = bar_deltas[i - 1]
        threshold = cum_mean[i] * 2 if use_auto_threshold else 0
        
        gap_up = c2_low - c0_high
        if gap_up > 0 and bar_delta > threshold:
            top = round(c2_low, 5)
            bottom = round(c0_high, 5)
            
            mitigated = False
            end_time = last_timestamp
            for k in range(i + 1, n):
                if low_arr[k] <= bottom:
                    mitigated = True
                    end_time = str(df["time_stamp"].iloc[k])
                    break
                    
            fvgs.append({
                "type": "bullish",
                "start_time": str(df["time_stamp"].iloc[i - 1]),
                "end_time": end_time,
                "top": top,
                "bottom": bottom,
                "mitigated": mitigated,
                "idx": i - 1,
            })
            
        gap_down = c0_low - c2_high
        if gap_down > 0 and bar_delta > threshold:
            top = round(c0_low, 5)
            bottom = round(c2_high, 5)
            
            mitigated = False
            end_time = last_timestamp
            for k in range(i + 1, n):
                if high_arr[k] >= top:
                    mitigated = True
                    end_time = str(df["time_stamp"].iloc[k])
                    break
                    
            fvgs.append({
                "type": "bearish",
                "start_time": str(df["time_stamp"].iloc[i - 1]),
                "end_time": end_time,
                "top": top,
                "bottom": bottom,
                "mitigated": mitigated,
                "idx": i - 1,
            })
            
    if limit is not None and limit > 0:
        return fvgs[-limit:]
    return fvgs


# ==============================================================================
# 6. ฟังก์ชันตรวจจับ Equal Highs และ Equal Lows (EQH / EQL)
# หลักการทางคณิตศาสตร์: Proximity / Nearest-Neighbor Density Clustering
# เกณฑ์การวัดระยะ: Adaptive Volatility Metric (|Delta Price| < 0.1 * ATR)
# ==============================================================================
def detect_equal_highs_lows(df: pd.DataFrame, swing_highs: list, swing_lows: list, atr_arr: np.ndarray) -> tuple[list, list]:
    """
    [Mathematical Concept]: Proximity Density Clustering / Liquidity Pool Extraction
    - คำนวณระยะห่างระหว่างจุด Peak/Valley ติดกันด้วยเกณฑ์ความผันผวนยืดหยุ่น:
      |Price[i] - Price[i-1]| < Threshold * ATR
    - ทำหน้าที่เป็น Cluster Centroid สำหรับ Liquidity Pool
    ตรวจจับยอดคู่ หรือฐานคู่ที่มีระยะห่างของราคา < 0.1 * ATR
    """
    THRESHOLD = 0.1
    equal_highs, equal_lows = [], []
    
    for i in range(1, len(swing_highs)):
        curr, prev = swing_highs[i], swing_highs[i - 1]
        atr_val = float(atr_arr[curr["idx"]]) if curr["idx"] < len(atr_arr) else 1.0
        if abs(curr["price"] - prev["price"]) < THRESHOLD * atr_val:
            equal_highs.append({
                "start_time": prev["time"],
                "end_time": curr["time"],
                "price": round((curr["price"] + prev["price"]) / 2, 5)
            })
            
    for i in range(1, len(swing_lows)):
        curr, prev = swing_lows[i], swing_lows[i - 1]
        atr_val = float(atr_arr[curr["idx"]]) if curr["idx"] < len(atr_arr) else 1.0
        if abs(curr["price"] - prev["price"]) < THRESHOLD * atr_val:
            equal_lows.append({
                "start_time": prev["time"],
                "end_time": curr["time"],
                "price": round((curr["price"] + prev["price"]) / 2, 5)
            })
            
    return equal_highs[-10:], equal_lows[-10:]


# ==============================================================================
# 7. ฟังก์ชันตรวจจับโซนราคา Premium / Equilibrium / Discount
# หลักการทางคณิตศาสตร์: Min-Max Normalization & Quantile Range Partitioning
# สัดส่วนทางสถิติ: 50% Median Split (Equilibrium) & Outer Quantile Boundaries
# ==============================================================================
def detect_premium_discount_zones(df: pd.DataFrame) -> dict:
    """
    [Mathematical Concept]: Normalized Price Range Partitioning
    - Range = Max(High) - Min(Low)
    - Premium Zone: [Range * 0.95, Range * 1.00] (Overvalued / Expensive Zone)
    - Equilibrium:  [Range * 0.475, Range * 0.525] (Fair Value / Median Balance)
    - Discount Zone: [0, Range * 0.05] (Undervalued / Cheap Zone)
    """
    trail_high = float(df["high_price"].max())
    trail_low = float(df["low_price"].min())
    rng = trail_high - trail_low
    if rng == 0:
        return {}
    return {
        "premium":     {"top": round(trail_high, 5),                             "bottom": round(trail_high - 0.05 * rng, 5), "label": "Premium"},
        "equilibrium": {"top": round(trail_high * 0.525 + trail_low * 0.475, 5), "bottom": round(trail_high * 0.475 + trail_low * 0.525, 5), "label": "Equilibrium"},
        "discount":    {"top": round(trail_low + 0.05 * rng, 5),                 "bottom": round(trail_low, 5), "label": "Discount"},
    }


# ==============================================================================
# 8. ฟังก์ชันระบุ Strong / Weak High-Low
# หลักการทางคณิตศาสตร์: Global Extrema & Trend-Conditioned Boundary Classification
# ทฤษฎีความน่าจะเป็น: Conditional State Evaluation P(Break | Trend_Direction)
# ==============================================================================
def detect_strong_weak_hl(df: pd.DataFrame, swing_highs: list, swing_lows: list, swing_structure: list) -> dict:
    """
    [Mathematical Concept]: Conditional Extreme Classification based on Markov Trend State
    - ในเทรนด์ Bearish: High คือ Strong High (แนวต้านที่ผ่านยาก), Low คือ Weak Low (เป้าหมายรอการเบรก)
    - ในเทรนด์ Bullish: Low คือ Strong Low (แนวรับที่ผ่านยาก), High คือ Weak High (เป้าหมายรอการเบรก)
    """
    if not swing_highs or not swing_lows:
        return {}
    trail_high = max(swing_highs, key=lambda x: x["price"])
    trail_low  = min(swing_lows,  key=lambda x: x["price"])
    trend = swing_structure[-1]["direction"] if swing_structure else "neutral"
    return {
        "strong_high": {"time": trail_high["time"], "price": trail_high["price"], "label": "Strong High" if trend == "bearish" else "Weak High"},
        "strong_low":  {"time": trail_low["time"],  "price": trail_low["price"],  "label": "Strong Low"  if trend == "bullish" else "Weak Low"},
    }


# ==============================================================================
# 9. ฟังก์ชันคำนวณ RSI และตรวจจับ SMT Divergence (Smart Money Technique)
# หลักการทางคณิตศาสตร์ / สถิติ:
# - Correlation Breakdown & Non-Confirmation Principle (Intermarket Divergence)
# - Oscillator-Price Phase Asymmetry (Momentum Divergence / Wilder's Smoothing)
# ==============================================================================
def calc_rsi(closes: np.ndarray, period: int = 14) -> np.ndarray:
    """คำนวณ Wilder's Relative Strength Index (RSI)"""
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
    swing_period: int = 5,
) -> dict:
    """
    [Mathematical Concept]: Liquidity Manipulation & Correlation Divergence Search
    ตรวจจับ SMT Divergence ทั้งแบบ Intermarket Correlation (ICT SMT)
    และ Relative Strength Momentum Divergence (Wilder's RSI)
    """
    highs = df_primary["high_price"].values
    lows = df_primary["low_price"].values
    closes = df_primary["close_price"].values
    n = len(df_primary)

    shs, sls = detect_swings(df_primary, n=swing_period)
    rsi = calc_rsi(closes, period=14)

    corr_highs = None
    corr_lows = None
    if df_corr is not None and len(df_corr) == n:
        corr_highs = df_corr["high_price"].values
        corr_lows = df_corr["low_price"].values

    smt_signals = {}

    # Bullish SMT: Compare consecutive Swing Lows
    for i in range(1, len(sls)):
        curr_sl = sls[i]
        prev_sl = sls[i - 1]
        curr_idx = curr_sl["idx"]
        prev_idx = prev_sl["idx"]

        price_ll = curr_sl["price"] < prev_sl["price"]
        is_intermarket_bull = False
        if corr_lows is not None:
            c_curr_low = np.min(corr_lows[max(0, curr_idx - swing_period): min(n, curr_idx + swing_period + 1)])
            c_prev_low = np.min(corr_lows[max(0, prev_idx - swing_period): min(n, prev_idx + swing_period + 1)])
            if price_ll and c_curr_low > c_prev_low:
                is_intermarket_bull = True
            elif not price_ll and c_curr_low < c_prev_low:
                is_intermarket_bull = True

        is_momentum_bull = False
        if price_ll and rsi[curr_idx] > rsi[prev_idx]:
            is_momentum_bull = True

        if is_intermarket_bull or is_momentum_bull:
            stype = "both" if (is_intermarket_bull and is_momentum_bull) else ("intermarket" if is_intermarket_bull else "momentum")
            for k in range(curr_idx, min(n, curr_idx + 25)):
                smt_signals[k] = {"direction": "bullish", "smt_type": stype, "swing_idx": curr_idx}

    # Bearish SMT: Compare consecutive Swing Highs
    for i in range(1, len(shs)):
        curr_sh = shs[i]
        prev_sh = shs[i - 1]
        curr_idx = curr_sh["idx"]
        prev_idx = prev_sh["idx"]

        price_hh = curr_sh["price"] > prev_sh["price"]
        is_intermarket_bear = False
        if corr_highs is not None:
            c_curr_high = np.max(corr_highs[max(0, curr_idx - swing_period): min(n, curr_idx + swing_period + 1)])
            c_prev_high = np.max(corr_highs[max(0, prev_idx - swing_period): min(n, prev_idx + swing_period + 1)])
            if price_hh and c_curr_high < c_prev_high:
                is_intermarket_bear = True
            elif not price_hh and c_curr_high > c_prev_high:
                is_intermarket_bear = True

        is_momentum_bear = False
        if price_hh and rsi[curr_idx] < rsi[prev_idx]:
            is_momentum_bear = True

        if is_intermarket_bear or is_momentum_bear:
            stype = "both" if (is_intermarket_bear and is_momentum_bear) else ("intermarket" if is_intermarket_bear else "momentum")
            for k in range(curr_idx, min(n, curr_idx + 25)):
                smt_signals[k] = {"direction": "bearish", "smt_type": stype, "swing_idx": curr_idx}

    return smt_signals

