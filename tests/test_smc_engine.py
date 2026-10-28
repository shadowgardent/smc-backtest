import pytest
import pandas as pd
import numpy as np
from services.smc_engine import (
    calc_atr,
    detect_swings,
    detect_structure,
    detect_order_blocks,
    detect_fvg,
    detect_equal_highs_lows,
    detect_premium_discount_zones,
    detect_strong_weak_hl,
    calc_rsi,
    detect_smt_divergence,
)

def make_sample_df(n_bars=100, base=100.0, trend_slope=0.1):
    times = pd.date_range("2026-01-01", periods=n_bars, freq="5min")
    records = []
    price = base
    for i, t in enumerate(times):
        price += trend_slope + np.sin(i / 5.0) * 0.5
        o = price - 0.2
        c = price + 0.2
        h = max(o, c) + 0.4
        l = min(o, c) - 0.4
        records.append({
            "time_stamp": t,
            "open_price": round(o, 4),
            "high_price": round(h, 4),
            "low_price": round(l, 4),
            "close_price": round(c, 4),
            "volume": 1000,
        })
    return pd.DataFrame(records)

class TestSmcEngine:
    def test_calc_atr_normal(self):
        df = make_sample_df(100)
        atr = calc_atr(df, period=14)
        assert len(atr) == len(df)
        assert np.all(atr > 0)
        assert not np.any(np.isnan(atr))

    def test_calc_atr_empty_or_minimal(self):
        df = make_sample_df(2)
        atr = calc_atr(df, period=14)
        assert len(atr) == 2

    def test_detect_swings_finds_peaks_and_valleys(self):
        df = make_sample_df(100, trend_slope=0.0)
        highs, lows = detect_swings(df, n=5)
        assert isinstance(highs, list)
        assert isinstance(lows, list)
        assert len(highs) > 0
        assert len(lows) > 0
        for h in highs:
            assert "price" in h
            assert "time" in h
            assert "idx" in h

    def test_detect_structure_fsm(self):
        df = make_sample_df(150, trend_slope=0.2)
        highs, lows = detect_swings(df, n=5)
        events = detect_structure(df, highs, lows)
        assert isinstance(events, list)
        for ev in events:
            assert ev["type"] in ["BOS", "CHoCH"]
            assert ev["direction"] in ["bullish", "bearish"]

    def test_detect_order_blocks(self):
        df = make_sample_df(120, trend_slope=0.1)
        atr = calc_atr(df)
        highs, lows = detect_swings(df, n=5)
        events = detect_structure(df, highs, lows)
        obs = detect_order_blocks(df, events, atr=atr)
        assert isinstance(obs, list)
        for ob in obs:
            assert ob["type"] in ["bullish", "bearish"]
            assert ob["top"] >= ob["bottom"]
            assert "mitigated" in ob

    def test_detect_fvg(self):
        # Craft explicit 3-bar gap
        records = [
            {"time_stamp": "2026-01-01 00:00", "open_price": 10.0, "high_price": 10.5, "low_price": 9.8, "close_price": 10.2, "volume": 100},
            {"time_stamp": "2026-01-01 00:05", "open_price": 10.3, "high_price": 14.0, "low_price": 10.3, "close_price": 13.8, "volume": 500},
            {"time_stamp": "2026-01-01 00:10", "open_price": 13.9, "high_price": 15.0, "low_price": 11.5, "close_price": 14.5, "volume": 200},
        ]
        df = pd.DataFrame(records)
        fvgs = detect_fvg(df, use_auto_threshold=False)
        assert len(fvgs) >= 1
        assert fvgs[0]["type"] == "bullish"
        assert fvgs[0]["bottom"] == 10.5
        assert fvgs[0]["top"] == 11.5

    def test_detect_equal_highs_lows(self):
        df = make_sample_df(60)
        atr = calc_atr(df)
        highs = [
            {"price": 105.00, "time": "2026-01-01 00:00", "idx": 10},
            {"price": 105.01, "time": "2026-01-01 00:20", "idx": 30},
        ]
        lows = [
            {"price": 95.00, "time": "2026-01-01 00:10", "idx": 15},
            {"price": 95.02, "time": "2026-01-01 00:30", "idx": 35},
        ]
        eqh, eql = detect_equal_highs_lows(df, highs, lows, atr)
        assert len(eqh) >= 1
        assert len(eql) >= 1

    def test_detect_premium_discount_zones(self):
        df = make_sample_df(80)
        zones = detect_premium_discount_zones(df)
        assert "premium" in zones
        assert "equilibrium" in zones
        assert "discount" in zones
        assert zones["premium"]["top"] >= zones["premium"]["bottom"]
        assert zones["discount"]["top"] >= zones["discount"]["bottom"]

    def test_edge_case_flat_market(self):
        times = pd.date_range("2026-01-01", periods=30, freq="5min")
        df = pd.DataFrame({
            "time_stamp": times,
            "open_price": 100.0,
            "high_price": 100.0,
            "low_price": 100.0,
            "close_price": 100.0,
            "volume": 0
        })
        atr = calc_atr(df)
        assert len(atr) == 30
        highs, lows = detect_swings(df, n=5)
        assert isinstance(highs, list)
        zones = detect_premium_discount_zones(df)
        assert zones == {}

    def test_detect_smt_divergence(self):
        df_a = make_sample_df(120, base=100.0, trend_slope=0.0)
        df_b = make_sample_df(120, base=100.0, trend_slope=0.0)
        rsi = calc_rsi(df_a["close_price"].values, period=14)
        assert len(rsi) == len(df_a)
        assert np.all((rsi >= 0) & (rsi <= 100))

        signals = detect_smt_divergence(df_a, df_b, swing_period=5)
        assert isinstance(signals, dict)
