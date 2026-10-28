for pkg in ['fitz', 'pypdfium2', 'pdf2image', 'pypdf']:
    try:
        __import__(pkg)
        print("Installed:", pkg)
    except Exception:
        print("Not installed:", pkg)
