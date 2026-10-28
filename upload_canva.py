import requests

url = "https://www.canva.com/_blob/upload/ingress/upload/file/agent-tool?_sat=eyJhbGciOiJFUzI1NiJ9.eyJqdGkiOiJTYS1IaFh3ZzE4TXhyWFlvM3NpQjd3Iiwic3ViIjoiVUFGa1pEN0tpWmM6QkFGRUlxaWw5RWMiLCJpYXQiOjE3OTMwOTE5ODcsImV4cCI6MTc5MzA5Mzc4NywidXNnIjoxLCJhY3QiOiIvX2Jsb2IvdXBsb2FkL2luZ3Jlc3MvdXBsb2FkL2ZpbGUvYWdlbnQtdG9vbCIsIm1vZGUiOiJTSU5HTEVfUkVRVUVTVCJ9.LNMmx04yZpXfIfWRuGE-L-oCK9Y5QeoleJaORAF-koP9_bKGlztPK0TQxz9nMD3Fayx5x8J5LIb7xHVO3p5Unw"
file_path = r"C:\Users\ONEST\Downloads\SMC_System_Flow_Clean.png"

with open(file_path, "rb") as f:
    data = f.read()

headers = {
    "Content-Type": "application/octet-stream"
}

resp = requests.post(url, data=data, headers=headers)
print("Status code:", resp.status_code)
print("Response text:", resp.text)
