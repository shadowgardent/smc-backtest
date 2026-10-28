import requests

sheet_id = "15_QNMleInWe0B3X4Xx-YMA-rEVA69Gu4iWgFCUtNDLY"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    resp = requests.get(url, timeout=10)
    print("Status code:", resp.status_code)
    print("Content-Type:", resp.headers.get("Content-Type"))
    print("Length:", len(resp.text))
    with open("google_sheet_eval.csv", "w", encoding="utf-8") as f:
        f.write(resp.text)
    print("Saved to google_sheet_eval.csv")
    print("\nFirst 500 characters:")
    print(resp.text[:500])
except Exception as e:
    print("Error:", e)
