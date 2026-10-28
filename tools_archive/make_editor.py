import shutil
import os

# Copy mermaid.min.js to Downloads as well
shutil.copyfile("e:/Project/smc-backtest-backend/mermaid.min.js", "C:/Users/ONEST/Downloads/mermaid.min.js")

html_content = """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SMC System Flow Diagram Editor</title>
    <!-- Try local mermaid first, then CDN fallback -->
    <script src="mermaid.min.js"></script>
    <script>
        if (typeof mermaid === 'undefined') {
            document.write('<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"><\\/script>');
        }
    </script>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', Tahoma, sans-serif; display: flex; height: 100vh; background: #f8fafc; color: #1e293b; overflow: hidden; }
        .sidebar { width: 440px; background: white; border-right: 1px solid #e2e8f0; display: flex; flex-direction: column; padding: 20px; box-shadow: 2px 0 8px rgba(0,0,0,0.04); z-index: 10; }
        .sidebar h2 { font-size: 18px; margin-bottom: 8px; color: #0f172a; font-weight: 700; display: flex; align-items: center; gap: 8px; }
        .sidebar p { font-size: 13px; color: #64748b; margin-bottom: 16px; line-height: 1.5; }
        textarea { flex: 1; width: 100%; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px; font-family: 'Consolas', 'Courier New', monospace; font-size: 13px; resize: none; background: #fdfdfd; line-height: 1.4; outline: none; transition: border-color 0.2s; }
        textarea:focus { border-color: #7c3aed; background: white; }
        .actions { margin-top: 16px; display: flex; flex-direction: column; gap: 10px; }
        .btn-row { display: flex; gap: 10px; }
        button { cursor: pointer; border: none; border-radius: 8px; font-size: 14px; font-weight: 600; padding: 12px 16px; transition: all 0.2s; display: flex; align-items: center; justify-content: center; gap: 6px; }
        .btn-update { background: #7c3aed; color: white; width: 100%; }
        .btn-update:hover { background: #6d28d9; }
        .btn-png { background: #0284c7; color: white; flex: 1; }
        .btn-png:hover { background: #0369a1; }
        .btn-svg { background: #f1f5f9; color: #334155; border: 1px solid #cbd5e1; flex: 1; }
        .btn-svg:hover { background: #e2e8f0; }
        .canvas-area { flex: 1; display: flex; flex-direction: column; position: relative; background: #fafafa; overflow: auto; }
        .canvas-toolbar { position: absolute; top: 16px; right: 16px; display: flex; gap: 8px; background: white; padding: 6px 12px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid #e2e8f0; z-index: 5; }
        .zoom-btn { background: none; border: none; font-size: 16px; cursor: pointer; padding: 4px 8px; color: #475569; }
        .zoom-btn:hover { color: #0f172a; }
        #preview-wrapper { flex: 1; display: flex; align-items: center; justify-content: center; padding: 40px; overflow: auto; }
        #preview { transform-origin: center center; transition: transform 0.15s ease; background: white; padding: 24px; border-radius: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.05); }
        .badge { background: #ede9fe; color: #7c3aed; font-size: 11px; padding: 2px 8px; border-radius: 12px; font-weight: 600; }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>🛠️ แก้ไขโค้ดแผนภาพ <span class="badge">Mermaid</span></h2>
        <p>คุณสามารถแก้ไขข้อความภาษาไทยในเครื่องหมาย <code>["..."]</code> ได้โดยตรง แผนภาพจะอัปเดตให้อัตโนมัติ</p>
        <textarea id="code-input" spellcheck="false"></textarea>
        <div class="actions">
            <button class="btn-update" onclick="renderDiagram()">🔄 อัปเดตแผนภาพ (Refresh)</button>
            <div class="btn-row">
                <button class="btn-png" onclick="exportPNG()">📥 โหลดรูป PNG (HD)</button>
                <button class="btn-svg" onclick="exportSVG()">📥 โหลด SVG</button>
            </div>
        </div>
    </div>

    <div class="canvas-area">
        <div class="canvas-toolbar">
            <button class="zoom-btn" onclick="zoom(0.1)" title="ซูมเข้า">➕</button>
            <button class="zoom-btn" onclick="zoom(-0.1)" title="ซูมออก">➖</button>
            <button class="zoom-btn" onclick="resetZoom()" title="รีเซ็ต">🔄 100%</button>
        </div>
        <div id="preview-wrapper">
            <div id="preview"></div>
        </div>
    </div>

    <script>
        const initialCode = `%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#EDE9FE', 'primaryBorderColor': '#8B5CF6', 'primaryTextColor': '#262626', 'lineColor': '#7C7C7C', 'tertiaryColor': '#F5F5F5'}}}%%
graph TD
    subgraph Sub1 ["ระบบวิเคราะห์ SMC ด้วยอัลกอริทึม"]
        A["Input: ระบุสัญลักษณ์คู่เงิน & Timeframe"]
        B["Data Fetching API: ดึงข้อมูลราคา OHLCV"]
        C["Algorithm: ประมวลผลจุด Swing High / Low"]
        D["Algorithm: ตรวจจับ BOS / CHoCH / OB"]
        E["Multi-Timeframe Engine: สแกนข้อมูล 7 กรอบเวลา"]
        F["Scoring System: คำนวณทิศทางเทรนด์หลัก"]
    end

    G["Web Application: เรนเดอร์กราฟ Interactive"]
    H["Output: แสดงผลกราฟ SMC และ Dashboard สรุปผล"]
    User(("User / นักเทรด"))

    A --> B
    B --> C
    C --> D
    D --> E
    D --> G
    E --> F
    F --> G
    G --> H
    H --> User
    User --> A

    style Sub1 fill:#FAFAFA,stroke:#7C7C7C,stroke-width:1.5px
    style A fill:#EDE9FE,stroke:#8B5CF6,stroke-width:1.2px
    style B fill:#EDE9FE,stroke:#8B5CF6,stroke-width:1.2px
    style C fill:#EDE9FE,stroke:#8B5CF6,stroke-width:1.2px
    style D fill:#EDE9FE,stroke:#8B5CF6,stroke-width:1.2px
    style E fill:#EDE9FE,stroke:#8B5CF6,stroke-width:1.2px
    style F fill:#EDE9FE,stroke:#8B5CF6,stroke-width:1.2px
    style G fill:#EDE9FE,stroke:#8B5CF6,stroke-width:1.2px
    style H fill:#EDE9FE,stroke:#8B5CF6,stroke-width:1.2px
    style User fill:#EDE9FE,stroke:#8B5CF6,stroke-width:1.2px`;

        document.getElementById('code-input').value = initialCode;

        let currentZoom = 1.0;
        function zoom(delta) {
            currentZoom = Math.max(0.4, Math.min(2.5, currentZoom + delta));
            document.getElementById('preview').style.transform = `scale(${currentZoom})`;
        }
        function resetZoom() {
            currentZoom = 1.0;
            document.getElementById('preview').style.transform = 'scale(1.0)';
        }

        async function renderDiagram() {
            const code = document.getElementById('code-input').value;
            const container = document.getElementById('preview');
            try {
                mermaid.initialize({ startOnLoad: false });
                const { svg } = await mermaid.render('mermaid-svg-' + Date.now(), code);
                container.innerHTML = svg;
            } catch (err) {
                console.error(err);
            }
        }

        function exportSVG() {
            const svgEl = document.querySelector("#preview svg");
            if (!svgEl) return;
            const svgData = new XMLSerializer().serializeToString(svgEl);
            const blob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
            const a = document.createElement("a");
            a.href = URL.createObjectURL(blob);
            a.download = "SMC_System_Flow.svg";
            a.click();
        }

        function exportPNG(scale = 2.5) {
            const svgEl = document.querySelector("#preview svg");
            if (!svgEl) return;
            const svgData = new XMLSerializer().serializeToString(svgEl);
            const bbox = svgEl.getBoundingClientRect();
            const canvas = document.createElement("canvas");
            canvas.width = (bbox.width / currentZoom) * scale;
            canvas.height = (bbox.height / currentZoom) * scale;
            const ctx = canvas.getContext("2d");
            
            const img = new Image();
            const blob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
            const url = URL.createObjectURL(blob);
            
            img.onload = function() {
                ctx.fillStyle = "#ffffff";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                URL.revokeObjectURL(url);
                const a = document.createElement("a");
                a.download = "SMC_System_Flow_Custom.png";
                a.href = canvas.toDataURL("image/png");
                a.click();
            };
            img.src = url;
        }

        // Live preview on input with debounce
        let timer;
        document.getElementById('code-input').addEventListener('input', () => {
            clearTimeout(timer);
            timer = setTimeout(renderDiagram, 500);
        });

        window.onload = renderDiagram;
    </script>
</body>
</html>
"""

with open("e:/Project/smc-backtest-backend/smc_flow_editor.html", "w", encoding="utf-8") as f:
    f.write(html_content)

with open("C:/Users/ONEST/Downloads/smc_flow_editor.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Saved smc_flow_editor.html successfully in both Downloads and project!")
