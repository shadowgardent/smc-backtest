import pytest
import pandas as pd
from services.mt5_service import generate_synthetic_market_data
from services.backtest_engine import run_smc_backtest

class TestBacktestEngine:
    def test_backtest_with_synthetic_feed(self):
        df = generate_synthetic_market_data("EURUSD", "M5", bars=500)
        result = run_smc_backtest(df, risk_reward_ratio=2.0, risk_per_trade_pct=1.0)
        
        assert "total_trades" in result
        assert "win_rate" in result
        assert "profit_factor" in result
        assert "net_profit" in result
        assert "max_drawdown" in result
        assert "trades" in result
        assert "equity_curve" in result
        
        assert isinstance(result["trades"], list)
        assert isinstance(result["equity_curve"], list)
        assert 0.0 <= result["win_rate"] <= 100.0
        assert result["max_drawdown"] >= 0.0

    def test_backtest_insufficient_bars(self):
        df = generate_synthetic_market_data("EURUSD", "M5", bars=20)
        result = run_smc_backtest(df)
        assert result["total_trades"] == 0
        assert result["win_rate"] == 0.0
        assert result["trades"] == []

    def test_backtest_trade_record_schema(self):
        df = generate_synthetic_market_data("XAUUSD", "H1", bars=800)
        result = run_smc_backtest(df, risk_reward_ratio=2.5)
        
        assert result["total_trades"] > 0
        first_trade = result["trades"][0]
        assert "id" in first_trade
        assert first_trade["type"] in ["BUY", "SELL"]
        assert first_trade["result"] in ["WIN", "LOSS", "BE", "FULL_WIN", "PARTIAL_WIN"]

        assert "entry_price" in first_trade
        assert "sl_price" in first_trade
        assert "tp_price" in first_trade
        assert "pnl_cash" in first_trade

    def test_backtest_choch_ob_fvg_mode(self):
        df = generate_synthetic_market_data("EURUSD", "M15", bars=1200)
        result = run_smc_backtest(df, strategy_mode="choch_ob_fvg", max_trades=20)
        assert "zone_breakdown" in result
        assert "strategy" in result
        assert result["strategy"] == "choch_ob_fvg"
        if result["total_trades"] > 0:
            trade = result["trades"][0]
            assert trade["setup"] == "CHoCH"
            assert trade["entry_zone"] in ["OB", "FVG"]

    def test_backtest_break_even(self):
        df = generate_synthetic_market_data("EURUSD", "M15", bars=1500)
        result = run_smc_backtest(df, risk_reward_ratio=3.0, use_break_even=True, break_even_rr=1.0, max_trades=30)
        assert "be_trades" in result
        assert "be_rate" in result
        assert result["be_trades"] >= 0
        assert result["be_rate"] >= 0.0



