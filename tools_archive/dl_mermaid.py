import requests

try:
    r = requests.get("https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js", timeout=10)
    with open("e:/Project/smc-backtest-backend/mermaid.min.js", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Successfully downloaded mermaid.min.js offline! Size:", len(r.text))
except Exception as e:
    print("Error downloading:", e)
