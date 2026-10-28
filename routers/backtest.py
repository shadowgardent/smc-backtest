from fastapi import APIRouter, Query
from services.mt5_service import get_market_df
from services.backtest_engine import run_smc_backtest

router = APIRouter(prefix="/api", tags=["Backtest"])

@router.get("/backtest/{symbol}")
def execute_backtest(
    symbol: str,
    timeframe: str = "M15",
    bars: int = Query(default=30000, ge=100, le=50000),
    risk_reward: float = Query(default=3.0, ge=1.0, le=10.0),
    risk_percent: float = Query(default=1.0, ge=0.1, le=10.0),
    initial_capital: float = Query(default=10000.0, ge=100.0),
    swing_period: int = Query(default=5, ge=3, le=20),
    strategy_mode: str = Query(default="hybrid_partial_tp"),
    max_trades: int = Query(default=300, ge=10, le=1000),
    use_break_even: bool = Query(default=True),
    break_even_rr: float = Query(default=1.0, ge=0.5, le=3.0),
    use_partial_tp: bool = Query(default=False),
    tp1_rr: float = Query(default=1.5, ge=0.5, le=5.0),
    tp2_rr: float = Query(default=3.0, ge=1.0, le=10.0),
    use_htf_filter: bool = Query(default=False),
    use_smt_filter: bool = Query(default=False),
    smt_mode: str = Query(default="any"),
):
    """
    API สำหรับการทำ Backtesting ตามกลยุทธ์ Smart Money Concepts
    - Strategy Mode: 
        * 'hybrid_partial_tp' (Option 2: TP1 1.5R 50% + TP2 3.0R 50% + HTF Trend Filter ดัน Win Rate ~60%)
        * 'choch_ob_fvg' (ต้องเกิด CHoCH แล้วราคาย่อกลับหา OB/FVG)
        * 'all_ob' (All Order Blocks)
    - Break-Even: เมื่อราคาวิ่งถึง break_even_rr (ค่าเริ่มต้น 1:1) จะเลื่อน SL มาที่ทุน
    - SMT Divergence Filter: กรองสัญญาณหลอกด้วย ICT Intermarket SMT และ Momentum SMT (RSI)
    - คำนวณผลตอบแทน (Net PnL, %), อัตราการชนะ (Win Rate, %), อัตรากันทุน (BE Rate, %)
    """
    df = get_market_df(symbol, timeframe, bars=bars)
    if df is None:
        return {"error": "Could not retrieve data for backtesting"}

    df_corr = None
    if use_smt_filter and smt_mode in ["intermarket", "any"]:
        corr_map = {
            "EURUSD": "GBPUSD",
            "GBPUSD": "EURUSD",
            "XAUUSD": "EURUSD",
            "GOLD": "EURUSD",
            "USDJPY": "EURUSD",
        }
        corr_sym = corr_map.get(symbol.upper())
        if corr_sym:
            df_corr = get_market_df(corr_sym, timeframe, bars=bars)

    result = run_smc_backtest(
        df=df,
        risk_reward_ratio=risk_reward,
        risk_per_trade_pct=risk_percent,
        initial_capital=initial_capital,
        swing_period=swing_period,
        strategy_mode=strategy_mode,
        max_trades=max_trades,
        use_break_even=use_break_even,
        break_even_rr=break_even_rr,
        use_partial_tp=use_partial_tp,
        tp1_rr=tp1_rr,
        tp2_rr=tp2_rr,
        use_htf_filter=use_htf_filter,
        use_smt_filter=use_smt_filter,
        smt_mode=smt_mode,
        df_corr=df_corr,
    )
    result["symbol"] = symbol
    result["timeframe"] = timeframe
    result["bars_analyzed"] = len(df)
    return result
