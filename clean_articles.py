import pandas as pd
import numpy as np
import os

def clean_articles_data(input_file, output_file):
    print(f"開始處理資料: {input_file}")
    
    # 讀取 CSV，設定 article_id 為字串以保留開頭的 0
    df = pd.read_csv(input_file, dtype={'article_id': str})
    
    print("\n--- 原始資料資訊 ---")
    print(f"資料筆數 (列數, 欄數): {df.shape}")
    print("\n各欄位缺失值統計:")
    print(df.isnull().sum()[df.isnull().sum() > 0])
    print(f"\n重複資料筆數: {df.duplicated().sum()}")

    # 1. 處理缺失值 (Missing Values)
    # detail_desc 欄位常有缺失，將其填補為 'No description'
    if 'detail_desc' in df.columns:
        df['detail_desc'] = df['detail_desc'].fillna('No description')
    
    # 處理其他可能的數值缺失值 (如有需要可自行修改)
    # df.fillna(0, inplace=True)
    
    # 2. 移除重複資料 (Duplicates)
    df.drop_duplicates(inplace=True)

    # 3. 資料格式轉換 (Data Formatting)
    # 確保 article_id 是字串長度一致 (補滿 10 位)
    if 'article_id' in df.columns:
        df['article_id'] = df['article_id'].apply(lambda x: str(x).zfill(10))

    # 4. 去除可能的前後留白 (字串欄位)
    string_cols = df.select_dtypes(include=['object']).columns
    for col in string_cols:
        df[col] = df[col].astype(str).str.strip()

    print("\n--- 清洗後資料資訊 ---")
    print(f"資料筆數 (列數, 欄數): {df.shape}")
    print("\n各欄位缺失值統計:")
    missing_after = df.isnull().sum()
    print(missing_after[missing_after > 0] if missing_after.sum() > 0 else "無缺失值")
    
    # 輸出成乾淨的 CSV 檔案
    print(f"\n儲存清洗後的資料至: {output_file}")
    df.to_csv(output_file, index=False, encoding='utf-8')
    print("處理完成！")

if __name__ == "__main__":
    # 設定檔案路徑
    BASE_DIR = r"C:\Project_Hsiang\assets"
    input_csv = os.path.join(BASE_DIR, "articles.csv")
    output_csv = os.path.join(BASE_DIR, "articles_cleaned.csv")
    
    if os.path.exists(input_csv):
        clean_articles_data(input_csv, output_csv)
    else:
        print(f"找不到檔案: {input_csv}")
