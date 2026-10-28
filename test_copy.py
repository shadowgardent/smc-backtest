import shutil
from PIL import Image

# 1. Clean crop of the original uploaded image
orig = Image.open(r"C:\Users\ONEST\.gemini\antigravity\brain\a19985bc-fcd1-432f-9cb1-a7239ee1919d\.user_uploaded\media_1793090342193_64faed1d.png")
# crop with tight clean border around diagram
cropped = orig.crop((47, 10, 415, 730))
cropped.save("e:/Project/smc-backtest-backend/SMC_Dataflow_Original_Crop.png")
cropped.save("C:/Users/ONEST/Downloads/SMC_Dataflow_Original_Crop.png")

# 2. Also ensure HD versions are present in both places
shutil.copyfile("C:/Users/ONEST/Downloads/SMC_Dataflow_System_Process.png", "C:/Users/ONEST/Downloads/SMC_Dataflow_Process_HD.png")
shutil.copyfile("C:/Users/ONEST/Downloads/SMC_Dataflow_System_Process.png", "e:/Project/smc-backtest-backend/SMC_Dataflow_Process_HD.png")
print("All files saved successfully!")
