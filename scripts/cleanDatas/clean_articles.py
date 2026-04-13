import pandas as pd
import numpy as np

# 1. 載入資料
def load_and_explore(file_path):
    
    df = pd.read_csv(file_path, encoding="latin1")
    print(f"--- 資料形狀(列,欄): {df.shape}")

    print("--- 資料概況 ---")
    print(df.info())  # 查看每欄的資料型態與非空值數量
    return df

# 2. 執行清洗
def clean_data(df):
    # A. 處理重複值
    # 檢查是否有重複的 article_id
    duplicate_count = df.duplicated(subset=['article_id']).sum()
    print(f"重複的 ID 數量: {duplicate_count}")
    df = df.drop_duplicates(subset=['article_id'], keep='first')
    
    # 範例：如果 detail_desc 缺失，填入 "No description"
    df['detail_desc'] = df['detail_desc'].fillna('No description')
    
    # C. 文字標準化 (Normalization)
    # 將所有產品名稱轉為大寫，並去除前後空格
    df['prod_name'] = df['prod_name'].str.upper().str.strip()
    
    # D. 資料型態轉換
    # 確保 article_id 是字串（避免開頭的 0 被去掉）
    df['article_id'] = df['article_id'].astype(str)
    # 先轉字串，再補齊 10 位數(雙重保險，確保所有 ID 都是 10 位數字)
    df['article_id'] = df['article_id'].astype(str).str.zfill(10)
    return df

# 3. 儲存結果
def save_data(df, output_path):
    df.to_csv(output_path, index=False)
    print(f"\n清洗完成！已儲存至 {output_path}")

if __name__ == "__main__":
    file_path = './Assets/articles.csv'
    cleaned_file_path = './Assets/articles_cleaned.csv'
    
    
    # 執行流程
    raw_df = load_and_explore(file_path)
    cleaned_df = clean_data(raw_df)

    print("\n--- 缺失值處理成效 ---")
    null_compare = pd.DataFrame({
        '清洗前 (Nulls)': raw_df.isnull().sum(),
        '清洗後 (Nulls)': cleaned_df.isnull().sum()
    })
        # 只顯示有缺失過或是被處理過的欄位
    print(null_compare[null_compare['清洗前 (Nulls)'] > 0])

    save_data(cleaned_df, cleaned_file_path)