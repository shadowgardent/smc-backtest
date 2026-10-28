import zlib
import base64
import json

mermaid_code = """%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#EDE9FE', 'primaryBorderColor': '#8B5CF6', 'primaryTextColor': '#262626', 'lineColor': '#7C7C7C', 'tertiaryColor': '#F5F5F5'}}}%%
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
    style User fill:#EDE9FE,stroke:#8B5CF6,stroke-width:1.2px
"""

state = {
    "code": mermaid_code,
    "mermaid": '{"theme": "default"}',
    "autoSync": True,
    "updateDiagram": True
}

# pako format is zlib deflate raw
json_str = json.dumps(state)
compressed = zlib.compress(json_str.encode('utf-8'))[2:-4] # raw deflate without zlib header/checksum
encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
link = f"https://mermaid.live/edit#pako:{encoded}"
print("Mermaid Live URL:")
print(link)
