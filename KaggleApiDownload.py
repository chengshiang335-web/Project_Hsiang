from kaggle.api.kaggle_api_extended import KaggleApi
import os
import zipfile

download_path = "./assets/kaggle/"
competition = "h-and-m-personalized-fashion-recommendations"

os.makedirs(download_path, exist_ok=True)

api = KaggleApi()

try:
    api.authenticate()

    print("⬇️ 開始下載...")

    # ❗ 拿掉 unzip=True
    api.competition_download_files(
        competition,
        path=download_path
    )

    # ✅ 自己解壓
    for file in os.listdir(download_path):
        if file.endswith(".zip"):
            zip_path = os.path.join(download_path, file)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(download_path)

            print(f"📦 已解壓：{file}")

    # ✅ 檢查檔案
    files = os.listdir(download_path)

    if len(files) == 0:
        print("❌ 下載失敗")
    else:
        print(f"✅ 完成，共 {len(files)} 個檔案")

except Exception as e:
    print("❌ 發生錯誤：")
    print(e)