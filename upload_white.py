import requests

url = "https://www.canva.com/_blob/upload/ingress/upload/file/agent-tool?_sat=eyJhbGciOiJFUzI1NiJ9.eyJqdGkiOiJvTGlsSWtJWnI1elc0b0t6U0o0RzlRIiwic3ViIjoiVUFGa1pEN0tpWmM6QkFGRUlxaWw5RWMiLCJpYXQiOjE3OTMxNzUzMzQsImV4cCI6MTc5MzE3NzEzNCwidXNnIjoxLCJhY3QiOiIvX2Jsb2IvdXBsb2FkL2luZ3Jlc3MvdXBsb2FkL2ZpbGUvYWdlbnQtdG9vbCIsIm1vZGUiOiJTSU5HTEVfUkVRVUVTVCJ9.pqlXQ55dM_6T3yQoAX1leRy66I_n9MCGucHJLCAEOJekTHeioYw1tLneh9fHMtwkH-7NMLjI44NYDsMu56igag"
file_path = r"C:\Users\ONEST\Downloads\SMC_Architecture_Flow_White.png"

with open(file_path, "rb") as f:
    data = f.read()

headers = {"Content-Type": "application/octet-stream"}
resp = requests.post(url, data=data, headers=headers)
print("Status code:", resp.status_code)
print("Response text:", resp.text)
