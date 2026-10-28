import pytest
from starlette.testclient import TestClient
from main import app

client = TestClient(app)

class TestApiEndpoints:
    def test_root_health(self):
        res = client.get("/")
        assert res.status_code == 200
        data = res.json()
        assert data["message"] == "SMC Backtest API is running"
        assert "backtest" in data["features"]

    def test_symbols_endpoint(self):
        res = client.get("/api/symbols")
        assert res.status_code == 200
        data = res.json()
        assert "symbols" in data
        assert len(data["symbols"]) > 0

    def test_market_data_endpoint(self):
        res = client.get("/api/data/EURUSD?timeframe=M5&bars=100")
        assert res.status_code == 200
        data = res.json()
        assert data["symbol"] == "EURUSD"
        assert len(data["data"]) == 100

    def test_smc_endpoint(self):
        res = client.get("/api/smc/EURUSD?timeframe=M5&bars=100")
        assert res.status_code == 200
        data = res.json()
        assert "swing_highs" in data
        assert "swing_lows" in data
        assert "order_blocks" in data
        assert "fvgs" in data

    def test_dashboard_endpoint(self):
        res = client.get("/api/dashboard/EURUSD")
        assert res.status_code == 200
        data = res.json()
        assert "trends" in data
        assert "score" in data
        assert "signal" in data

    def test_backtest_endpoint(self):
        res = client.get("/api/backtest/EURUSD?timeframe=H1&bars=300&risk_reward=2.0")
        assert res.status_code == 200
        data = res.json()
        assert "total_trades" in data
        assert "win_rate" in data
        assert "profit_factor" in data
        assert "net_profit" in data
        assert "trades" in data
