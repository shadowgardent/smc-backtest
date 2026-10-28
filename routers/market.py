from fastapi import APIRouter
from services.mt5_service import (
    get_terminal_status,
    get_symbols_list,
    get_live_candles,
    get_market_df,
)

router = APIRouter(prefix="/api", tags=["Market"])


@router.get("/mt5/status")
def mt5_status():
    """เช็คสถานะการเชื่อมต่อ MT5"""
    return get_terminal_status()


@router.get("/symbols")
def get_symbols():
    """ดึง symbols ที่มีใน MT5"""
    return get_symbols_list()


@router.get("/live/{symbol}")
def get_live_candle(symbol: str, timeframe: str = "M5"):
    """ดึงแท่งเทียนล่าสุด 2 แท่ง สำหรับ real-time polling update"""
    return get_live_candles(symbol, timeframe)


@router.get("/data/{symbol}")
def get_market_data(symbol: str, timeframe: str = "M5", bars: int = 1000):
    """ดึงข้อมูลแท่งเทียนจาก MT5 (real-time)"""
    print(f"Request: {symbol} TF:{timeframe} bars:{bars}")
    df = get_market_df(symbol, timeframe, bars)
    if df is None:
        return {"error": "No data found — MT5 not connected or symbol invalid"}
    df["time_stamp"] = df["time_stamp"].astype(str)
    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "total_candles": len(df),
        "source": "mt5",
        "data": df.to_dict(orient="records")
    }
