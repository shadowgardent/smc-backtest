import os
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone

# ---- MT5 Setup ----
try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    mt5 = None
    MT5_AVAILABLE = False
    print("[MT5] MetaTrader5 library not installed")

# MT5 Timeframe mapping
MT5_TF_MAP = {
    "M1":  getattr(mt5, "TIMEFRAME_M1", 1) if MT5_AVAILABLE else 1,
    "M5":  getattr(mt5, "TIMEFRAME_M5", 5) if MT5_AVAILABLE else 5,
    "M15": getattr(mt5, "TIMEFRAME_M15", 15) if MT5_AVAILABLE else 15,
    "M30": getattr(mt5, "TIMEFRAME_M30", 30) if MT5_AVAILABLE else 30,
    "H1":  getattr(mt5, "TIMEFRAME_H1", 16385) if MT5_AVAILABLE else 16385,
    "H4":  getattr(mt5, "TIMEFRAME_H4", 16388) if MT5_AVAILABLE else 16388,
    "D1":  getattr(mt5, "TIMEFRAME_D1", 16408) if MT5_AVAILABLE else 16408,
    "W1":  getattr(mt5, "TIMEFRAME_W1", 32769) if MT5_AVAILABLE else 32769,
}

TF_MINUTES_MAP = {
    "M1": 1,
    "M5": 5,
    "M15": 15,
    "M30": 30,
    "H1": 60,
    "H4": 240,
    "D1": 1440,
    "W1": 10080,
}

SYMBOL_BASE_PRICES = {
    "EURUSD": (1.0850, 0.00015, 5),
    "GBPUSD": (1.2950, 0.00020, 5),
    "USDJPY": (152.50, 0.040, 3),
    "AUDUSD": (0.6650, 0.00015, 5),
    "USDCAD": (1.3850, 0.00015, 5),
    "XAUUSD": (2650.0, 1.20, 2),
    "GOLD":   (2650.0, 1.20, 2),
    "BTCUSD": (68500.0, 45.0, 2),
}

# ---- Symbol Mapping (UI name → MT5 broker name) ----
SYMBOL_MAP: dict[str, str] = {
    "XAUUSD": "GOLD#",
    "GOLD":   "GOLD#",
}

def resolve_symbol(symbol: str) -> str:
    """แปลง UI symbol → MT5 broker symbol"""
    return SYMBOL_MAP.get(symbol.upper(), symbol)

import time

# ---- MT5 Connection ----
_mt5_connected = False
_last_mt5_attempt = 0.0
_MT5_RETRY_COOLDOWN = 30.0  # seconds

def is_real_mt5_running() -> bool:
    """ตรวจสอบว่ามีโปรแกรม MetaTrader 5 ของจริงกำลังเปิดใช้งานอยู่หรือไม่ (ไม่นับ background liveupdate)"""
    try:
        import psutil
        for p in psutil.process_iter(['name', 'exe']):
            name = (p.info.get('name') or '').lower()
            if 'terminal64' in name or 'terminal.exe' in name:
                exe = (p.info.get('exe') or '').lower()
                if 'liveupdate' not in exe:
                    return True
    except Exception:
        pass
    return False

def ensure_mt5_connected() -> bool:
    global _mt5_connected, _last_mt5_attempt
    if not MT5_AVAILABLE or mt5 is None:
        return False
    if _mt5_connected:
        info = mt5.terminal_info()
        if info is not None:
            return True
        _mt5_connected = False
    
    # Fast check: Do not try to connect/initialize if user has not opened MT5 terminal
    if not is_real_mt5_running():
        return False

    # Cooldown to avoid hanging when MT5 terminal is closed
    now = time.time()
    if now - _last_mt5_attempt < _MT5_RETRY_COOLDOWN:
        return False
        
    _last_mt5_attempt = now
    try:
        # Connect to default terminal or primary install path
        path = r"C:\Program Files\MetaTrader 5\terminal64.exe"
        if os.path.exists(path):
            success = mt5.initialize(path=path, timeout=2000)
        else:
            success = mt5.initialize(timeout=2000)
            
        if success:
            _mt5_connected = True
            print(f"[MT5] connected: {mt5.terminal_info().name}")
            return True
    except Exception as e:
        print(f"[MT5] initialize exception: {e}")
    return False


def get_terminal_status() -> dict:
    """ตรวจสอบสถานะและรายละเอียดบัญชี MT5"""
    if not MT5_AVAILABLE or mt5 is None:
        return {"connected": False, "reason": "MetaTrader5 library not installed (Fallback Engine Active)"}
    if ensure_mt5_connected():
        info = mt5.terminal_info()
        account = mt5.account_info()
        return {
            "connected": True,
            "terminal": info.name if info else "Unknown",
            "build": info.build if info else 0,
            "account": account.login if account else 0,
            "broker": account.company if account else "Unknown",
            "server": account.server if account else "Unknown",
        }
    return {"connected": False, "reason": "MT5 Terminal not running (Fallback Engine Active)"}


def get_symbols_list() -> dict:
    """ดึงรายชื่อคู่เงินที่เปิดแสดงใน MT5 Market Watch หรือรายการหลัก"""
    if not ensure_mt5_connected() or mt5 is None:
        return {"source": "fallback", "symbols": ["EURUSD", "XAUUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "BTCUSD"]}
    all_symbols = mt5.symbols_get()
    if all_symbols is None:
        return {"source": "mt5", "symbols": ["EURUSD", "XAUUSD", "GBPUSD", "USDJPY", "BTCUSD"]}
    names = [s.name for s in all_symbols if s.visible]
    return {"source": "mt5", "symbols": names if names else ["EURUSD", "XAUUSD", "GBPUSD", "USDJPY", "BTCUSD"]}


def generate_synthetic_market_data(symbol: str, timeframe: str = "M5", bars: int = 1000) -> pd.DataFrame:
    """สร้างข้อมูลแท่งเทียนจำลองที่มีโครงสร้างราคาตามหลัก SMC สำหรับการทดสอบเมื่อ MT5 ออฟไลน์"""
    sym_upper = symbol.upper()
    base_price, volatility, precision = SYMBOL_BASE_PRICES.get(sym_upper, (1.0000, 0.0002, 5))
    step_minutes = TF_MINUTES_MAP.get(timeframe, 5)
    
    np.random.seed(abs(hash(symbol + timeframe)) % (2**31 - 1))
    
    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=step_minutes * bars)
    
    timestamps = [start_time + timedelta(minutes=step_minutes * i) for i in range(bars)]
    
    # Random walk with wave momentum
    trend_cycle = np.sin(np.linspace(0, 8 * np.pi, bars)) * volatility * 8
    noise = np.random.normal(0, volatility, bars)
    returns = noise + (trend_cycle / bars)
    
    close_prices = base_price + np.cumsum(returns)
    
    records = []
    prev_close = base_price
    for i, t in enumerate(timestamps):
        c = close_prices[i]
        o = prev_close
        high_diff = abs(np.random.exponential(volatility * 0.8))
        low_diff = abs(np.random.exponential(volatility * 0.8))
        h = max(o, c) + high_diff
        l = min(o, c) - low_diff
        vol = int(np.random.randint(100, 2500))
        
        records.append({
            "time_stamp": t,
            "symbol": symbol,
            "open_price": round(float(o), precision),
            "high_price": round(float(h), precision),
            "low_price": round(float(l), precision),
            "close_price": round(float(c), precision),
            "volume": vol
        })
        prev_close = c
        
    df = pd.DataFrame(records)
    return df


def get_live_candles(symbol: str, timeframe: str = "M5") -> dict:
    """ดึงแท่งเทียน 2 แท่งล่าสุด พร้อม Tick Bid Price ปัจจุบัน (รองรับ MT5 + Fallback)"""
    if ensure_mt5_connected() and mt5 is not None:
        tf_const = MT5_TF_MAP.get(timeframe)
        if tf_const is not None:
            mt5_symbol = resolve_symbol(symbol)
            mt5.symbol_select(mt5_symbol, True)
            rates = mt5.copy_rates_from_pos(mt5_symbol, tf_const, 0, 2)
            if rates is not None and len(rates) > 0:
                tick = mt5.symbol_info_tick(mt5_symbol)
                current_price = tick.bid if tick else None
                candles = []
                for r in rates:
                    candles.append({
                        "time_stamp": str(pd.Timestamp(r["time"], unit="s", tz="UTC")),
                        "open_price":  round(float(r["open"]),  5),
                        "high_price":  round(float(r["high"]),  5),
                        "low_price":   round(float(r["low"]),   5),
                        "close_price": round(float(r["close"]), 5),
                        "volume": int(r["tick_volume"]),
                    })
                return {
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "source": "mt5",
                    "current_price": round(float(current_price), 5) if current_price else None,
                    "candles": candles,
                }
    
    # Fallback simulation
    df = generate_synthetic_market_data(symbol, timeframe, bars=5)
    last_two = df.iloc[-2:].to_dict(orient="records")
    curr_price = float(df["close_price"].iloc[-1])
    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "source": "fallback",
        "current_price": curr_price,
        "candles": [
            {
                "time_stamp": str(c["time_stamp"]),
                "open_price": c["open_price"],
                "high_price": c["high_price"],
                "low_price": c["low_price"],
                "close_price": c["close_price"],
                "volume": c["volume"],
            } for c in last_two
        ]
    }


def get_market_df(symbol: str, timeframe: str, bars: int = 1000, allow_fallback: bool = True) -> pd.DataFrame | None:
    """ดึงข้อมูลแท่งเทียนตรงจาก MT5 terminal หรือสลับเป็น Synthetic Fallback หากไม่ได้เปิด MT5"""
    if ensure_mt5_connected() and mt5 is not None:
        tf_const = MT5_TF_MAP.get(timeframe)
        if tf_const is not None:
            mt5_symbol = resolve_symbol(symbol)
            if mt5.symbol_select(mt5_symbol, True):
                rates = mt5.copy_rates_from_pos(mt5_symbol, tf_const, 0, bars)
                if rates is not None and len(rates) > 0:
                    df = pd.DataFrame(rates)
                    df["time_stamp"] = pd.to_datetime(df["time"], unit="s", utc=True)
                    df = df.rename(columns={
                        "open":  "open_price",
                        "high":  "high_price",
                        "low":   "low_price",
                        "close": "close_price",
                        "tick_volume": "volume",
                    })
                    df["symbol"] = symbol
                    print(f"[MT5] {symbol} ({mt5_symbol}) {timeframe}: {len(df)} bars")
                    return df[["time_stamp", "symbol", "open_price", "high_price", "low_price", "close_price", "volume"]].reset_index(drop=True)

    if allow_fallback:
        print(f"[FALLBACK] Using synthetic market feed for {symbol} {timeframe}: {bars} bars")
        return generate_synthetic_market_data(symbol, timeframe, bars=bars)
        
    return None
