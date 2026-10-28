# 📈 SMC Backtest & Market Structure Analysis System

ระบบวิเคราะห์และทดสอบกลยุทธ์โครงสร้างตลาดการเงินด้วยอัลกอริทึม **Smart Money Concepts (SMC)** แบบ Full-Stack เพื่อแปลงการวิเคราะห์ทางเทคนิคให้เป็นกฎเกณฑ์ทางคณิตศาสตร์ที่เป็นปรนัย (Objective Analysis) พร้อมหน้าจอแสดงผลชาร์ตแบบ Interactive

---

## ✨ คุณสมบัติหลัก (Key Features)

* **SMC Core Engine:** ตรวจจับโครงสร้างตลาดอัตโนมัติด้วยคณิตศาสตร์
  * **Market Structure:** ตรวจจับ Swing High / Low, BOS (Break of Structure), และ CHoCH (Change of Character)
  * **Supply / Demand & Liquidity:** ตรวจจับ Order Blocks (เช็ค Mitigation), Fair Value Gap (FVG), และ Liquidity Pools (Equal Highs / Lows)
  * **Pricing Zones:** คำนวณโซน Premium & Discount
* **Multi-Timeframe Matrix:** สแกนและวิเคราะห์แนวโน้มตลาดพร้อมประเมินคะแนนทิศทางราคาในหลายกรอบเวลา (Multi-TF Dashboard)
* **Interactive Charting:** หน้าบ้าน Angular เชื่อมต่อ TradingView Lightweight Charts พร้อมเลเยอร์ **HTML5 Canvas Overlay** วาดโซนราคาและโครงสร้างแบบ Real-time
* **Backtesting Engine:** ระบบจำลองและประเมินผลการเทรดย้อนหลัง วัดผลกำไร-ขาดทุน, Win Rate, และ Risk-to-Reward Ratio

---

## 🛠️ Tech Stack

* **Backend:** Python 3.11, FastAPI, Pandas, NumPy, Uvicorn, Pytest
* **Frontend:** Angular 19, TypeScript, TradingView Lightweight Charts, HTML5 Canvas
* **Data Providers:** MetaTrader 5 (MT5) / Financial Market APIs

---

## 🚀 เริ่มต้นใช้งาน (Quick Start)

### 1. รันระบบ Backend (FastAPI)

```bash
# ติดตั้ง dependencies
pip install -r requirements.txt

# รัน API Server (พอร์ต 8000)
python main.py
```
> เข้าดู API Documentation (Swagger) ได้ที่ `http://127.0.0.1:8000/docs`

### 2. รันระบบ Frontend (Angular)

```bash
cd smc-backtest-frontend

# ติดตั้งแพ็กเกจ
npm install

# รัน Development Server
npm start
```
> เข้าใช้งานเว็บแอปพลิเคชันได้ที่ `http://localhost:4200`

---

## 🧪 การทดสอบ (Unit Testing)

ทดสอบลอจิก SMC Engine และ API Endpoints:

```bash
pytest tests/
```
