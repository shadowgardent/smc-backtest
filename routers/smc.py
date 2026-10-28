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
    detect_strong_weak_hl,
)

router = APIRouter(prefix="/api", tags=["SMC"])


@router.get("/smc/{symbol}")
def get_smc_data(symbol: str, timeframe: str = "M5", swing_period: int = 5, bars: int = 1000):
    """วิเคราะห์ SMC ครบ feature จากข้อมูล MT5 real-time"""
    print(f"SMC: {symbol} TF:{timeframe} n={swing_period} bars:{bars}")
    df = get_market_df(symbol, timeframe, bars)
    if df is None:
        return {"error": "No data found"}

    atr = calc_atr(df)

    internal_highs, internal_lows = detect_swings(df, n=swing_period)
    internal_structure = detect_structure(df, internal_highs, internal_lows)

    swing_n = max(swing_period * 2, 10)
    swing_highs, swing_lows = detect_swings(df, n=swing_n)
    swing_structure = detect_structure(df, swing_highs, swing_lows)

    order_blocks = detect_order_blocks(df, swing_structure, atr=atr)
    internal_order_blocks = detect_order_blocks(df, internal_structure, atr=atr)
    fvgs = detect_fvg(df)
    equal_highs, equal_lows = detect_equal_highs_lows(df, swing_highs, swing_lows, atr)
    zones = detect_premium_discount_zones(df)
    hl = detect_strong_weak_hl(df, swing_highs, swing_lows, swing_structure)

    def clean(events):
        return [{k: v for k, v in e.items() if k != "idx"} for e in events]

    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "source": "mt5",
        "swing_highs": clean(swing_highs),
        "swing_lows": clean(swing_lows),
        "internal_highs": clean(internal_highs),
        "internal_lows": clean(internal_lows),
        "swing_structure": clean(swing_structure),
        "internal_structure": clean(internal_structure),
        "order_blocks": order_blocks,
        "internal_order_blocks": internal_order_blocks[-10:],
        "fvgs": fvgs,
        "equal_highs": equal_highs,
        "equal_lows": equal_lows,
        "zones": zones,
        "strong_weak_hl": hl,
    }
