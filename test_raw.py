import json
with open(r"C:/Users/ONEST/.gemini/antigravity/brain/a19985bc-fcd1-432f-9cb1-a7239ee1919d/.system_generated/steps/2322/output.txt", "r", encoding="utf-8") as f:
    text = f.read()

print("File length:", len(text))
# Let's inspect first 500 chars and lines
lines = text.splitlines()
print(f"Total lines: {len(lines)}")
for i in range(min(5, len(lines))):
    print(f"Line {i} ({len(lines[i])} chars): {lines[i][:150]}")
