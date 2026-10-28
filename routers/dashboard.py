from fastapi import APIRouter
from services.mt5_service import get_market_df
from services.smc_engine import (
    calc_atr,
    detect_swings,
    detect_structure,
    detect_order_blocks,
    detect_fvg,
    detect_equal_highs_lows,
    detect_premium_discount_zones,
)

router = APIRouter(prefix="/api", tags=["Dashboard"])


@router.get("/dashboard/{symbol}")
def get_dashboard(symbol: str):
    """
    การทำงานของโค้ด:
    1. วนลูปดึงข้อมูลแท่งเทียนและหาแนวโน้มโครงสร้างราคา (detect_structure) ใน 7 Timeframe (W1 ถึง M5)
    2. คำนวณคะแนนรวมถ่วงน้ำหนัก: W1=3, D1=3, H4=2, H1=2, M30=1, M15=1, M5=1 (bullish = +weight, bearish = -weight)
    3. กำหนดสัญญาณการเทรด: score >= 5 (Strong BUY), score > 0 (Weak BUY), score <= -5 (Strong SELL), score < 0 (Weak SELL), score == 0 (WAIT)
    4. ดึงข้อมูล H4 มาประมวลผลเพิ่มเติม:
       - เช็คระยะห่างราคาปัจจุบันกับ Order Block และ FVG ที่ยังไม่ถูกทดสอบ (mitigated = False)
       - คำนวณสถานะ Premium, Equilibrium, Discount
       - หาเป้าหมายราคา EQH (ด้านบน) และ EQL (ด้านล่าง) ที่ยังไม่ถูกกวาด
    5. คืนค่าผลการวิเคราะห์ทั้งหมดในรูปแบบ JSON
    """
    tfs = ["W1", "D1", "H4", "H1", "M30", "M15", "M5"]
    bars_map = {"W1": 50, "D1": 100, "H4": 300, "H1": 300, "M30": 300, "M15": 300, "M5": 300}
    results = {}
    score = 0
    # ให้น้ำหนัก Timeframe ใหญ่เยอะกว่าในการประเมินเทรนด์รวม
    weights = {"W1": 3, "D1": 3, "H4": 2, "H1": 2, "M30": 1, "M15": 1, "M5": 1}

    h4_data = None

    # 1. วนลูปวิเคราะห์โครงสร้างตลาดทั้ง 7 Timeframe
    for tf in tfs:
        b = bars_map.get(tf, 300)
        df = get_market_df(symbol, tf, bars=b)
        trend = "neutral"
        sh, sl, struct = [], [], []
        if df is not None and len(df) > 10:
            sh, sl = detect_swings(df, n=3 if tf in ["W1", "D1"] else 5)
            struct = detect_structure(df, sh, sl)
            if struct:
                trend = struct[-1]["direction"]
            else:
                if sh and sl:
                    trend = "bullish" if sh[-1]["price"] > sh[0]["price"] else "bearish"
        
        if tf == "H4" and df is not None and len(df) > 30:
            h4_data = (df, sh, sl, struct)

        results[tf] = trend
        # รวมคะแนนถ่วงน้ำหนัก
        if trend == "bullish":
            score += weights[tf]
        elif trend == "bearish":
            score -= weights[tf]

    # 2. แปลงคะแนนสุทธิเป็นคำแนะนำการเทรด
    if score >= 5:
        recommendation = "Strong BUY (เทรนด์ขาขึ้นชัดเจน แนะนำหาจังหวะ Buy ที่แนวรับ/OB)"
        signal = "BUY"
    elif score > 0:
        recommendation = "Weak BUY (เทรนด์หลักเริ่มขึ้น แต่มีย่อใน TF เล็ก)"
        signal = "BUY"
    elif score <= -5:
        recommendation = "Strong SELL (เทรนด์ขาลงชัดเจน แนะนำหาจังหวะ Sell ที่แนวต้าน/OB)"
        signal = "SELL"
    elif score < 0:
        recommendation = "Weak SELL (เทรนด์หลักเริ่มลง แต่มีย่อใน TF เล็ก)"
        signal = "SELL"
    else:
        recommendation = "Sideways (เทรนด์ไม่ชัดเจน แนะนำให้รอก่อน)"
        signal = "WAIT"

    # ================= 3. ADVANCED SMC FEATURES (ระดับ H4) =================
    radar_signals = []
    pd_status = "Unknown"
    liquidity_targets = {"upside": None, "downside": None}

    if h4_data is not None:
        h4_df, h4_sh, h4_sl, h4_struct = h4_data
        current_price = float(h4_df["close_price"].iloc[-1])
        atr = calc_atr(h4_df)
        
        # 3.1 SMC Setup Radar: ตรวจจับระยะห่างกับ Order Block และ FVG ระดับ H4
        obs = detect_order_blocks(h4_df, h4_struct, atr=atr)
        for ob in obs:
            if not ob["mitigated"]:
                if ob["bottom"] <= current_price <= ob["top"]:
                    radar_signals.append(f"🚨 กำลังทดสอบ H4 {ob['type'].title()} OB ({ob['bottom']} - {ob['top']})")
                elif ob["type"] == "bullish" and current_price > ob["top"] and (current_price - ob["top"]) / current_price < 0.003:
                    radar_signals.append(f"⏳ เข้าใกล้โซน H4 Bullish OB (รอ Buy)")
                elif ob["type"] == "bearish" and current_price < ob["bottom"] and (ob["bottom"] - current_price) / current_price < 0.003:
                    radar_signals.append(f"⏳ เข้าใกล้โซน H4 Bearish OB (รอ Sell)")
                    
        fvgs = detect_fvg(h4_df)
        for fvg in fvgs:
            if not fvg["mitigated"]:
                if fvg["bottom"] <= current_price <= fvg["top"]:
                    radar_signals.append(f"🧲 ราคาอยู่ในช่องว่าง H4 {fvg['type'].title()} FVG")
                    
        if not radar_signals:
            radar_signals.append("✅ ทางสะดวก (ไม่ติด OB/FVG ระดับ H4)")

        # 3.2 Premium / Discount Status
        zones = detect_premium_discount_zones(h4_df)
        if zones and zones["premium"] and zones["discount"]:
            if current_price >= zones["premium"]["bottom"]:
                pd_status = "🔴 Premium Zone (ราคาแพง แนะนำหนุนฝั่ง Sell)"
            elif current_price <= zones["discount"]["top"]:
                pd_status = "🟢 Discount Zone (ราคาถูก แนะนำหนุนฝั่ง Buy)"
            else:
                pd_status = "⚖️ Equilibrium (ราคากลางๆ ไม่ได้เปรียบ)"
        
        # 3.3 Liquidity Targets: ค้นหาเป้าหมายสภาพคล่อง EQH / EQL ที่ยังไม่ถูกกวาด
        eqh, eql = detect_equal_highs_lows(h4_df, h4_sh, h4_sl, atr)
        valid_eqh = [h for h in eqh if not h.get("mitigated", False) and h["price"] > current_price]
        if valid_eqh:
            liquidity_targets["upside"] = min(valid_eqh, key=lambda x: x["price"])["price"]
        valid_eql = [l for l in eql if not l.get("mitigated", False) and l["price"] < current_price]
        if valid_eql:
            liquidity_targets["downside"] = max(valid_eql, key=lambda x: x["price"])["price"]

    return {
        "symbol": symbol,
        "trends": results,
        "score": score,
        "signal": signal,
        "recommendation": recommendation,
        "radar_signals": radar_signals,
        "pd_status": pd_status,
        "liquidity_targets": liquidity_targets,
    }
