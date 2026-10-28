import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

from services.mt5_service import get_market_df
from services.backtest_engine import run_smc_backtest

symbols = ["EURUSD", "XAUUSD", "GBPUSD", "USDJPY", "BTCUSD"]

print("=============================================================================================================================")
print("        SMC M15 LARGE-SCALE BACKTEST: HYBRID PARTIAL TAKE-PROFIT (TARGET 300 TRADES - 40,000 BARS HISTORICAL DATA)           ")
print("=============================================================================================================================")

summary_rows = []
detailed_trades_sample = {}

for sym in symbols:
    # 40,000 bars on M15 gives over 1 year of continuous data
    df = get_market_df(sym, "M15", bars=40000)
    if df is None:
        continue
        
    res = run_smc_backtest(
        df=df,
        risk_reward_ratio=3.0,
        risk_per_trade_pct=1.0,
        initial_capital=10000.0,
        swing_period=5,
        strategy_mode="hybrid_partial_tp",
        max_trades=300,
        use_partial_tp=True,
        tp1_rr=1.5,
        tp2_rr=3.0,
        use_htf_filter=True
    )
    
    summary_rows.append({
        "Symbol": sym,
        "TF": "M15",
        "Bars": len(df),
        "Trades": res["total_trades"],
        "FullWin": res["full_win_trades"],
        "PartWin": res["partial_win_trades"],
        "Loss": res["loss_trades"],
        "TotalWins": res["win_trades"],
        "WinRate": f"{res['win_rate']:.1f}%",
        "ProfitFactor": f"{res['profit_factor']:.2f}",
        "NetProfit": f"${res['net_profit']:+,.2f}",
        "ROI": f"{res['net_profit_pct']:+.1f}%",
        "MaxDD": f"{res['max_drawdown']:.1f}%",
    })
    
    if sym in ["XAUUSD", "GBPUSD"] and res["trades"]:
        detailed_trades_sample[sym] = res["trades"][:5]

df_summary = pd.DataFrame(summary_rows)
print(df_summary.to_string(index=False))

print("\n=============================================================================================================================")
print("                                SAMPLE EXECUTED TRADES (FIRST 5 TRADES OUT OF 300)                                           ")
print("=============================================================================================================================")

for sym, trades in detailed_trades_sample.items():
    print(f"\n--- Symbol: {sym} ---")
    for t in trades:
        res = t["result"]
        tag = "[FULL WIN +2.25R]" if res == "FULL_WIN" else ("[PART WIN +0.75R]" if res == "PARTIAL_WIN" else "[LOSS -1.0R]")
        print(f"Trade #{t['id']:03d} | {t['type']:4s} | Entry: {t['entry_price']} | SL: {t['sl_price']} | TP2: {t['tp_price']} | PnL: ${t['pnl_cash']:+,.2f} ({t['r_multiple']:+.2f}R) | {tag}")

print("=============================================================================================================================")
