import pandas as pd

# 定義欄位型態以節省記憶體
 
dtypes = {
    #'age': 'int8',  # 年齡可能有小數，但為了節省空間，我們先轉為 int8（如果有小數會被截斷）
    #'FN': 'int8',  # 0 或 1 的二元變數
    #'Active': 'int8',  # 0 或 1 的二元變數
    #'club_member_status': 'category',  # 會員狀態類別
    #'fashion_news_frequency': 'category',  # 時尚新聞頻率類別
    'postal_code': 'str'  # 郵遞區號可能有前導零，保持為字串
    
}

def detailed_cleaning(file_path):
    # 1. 載入資料
    df = pd.read_csv(file_path, dtype=dtypes)
    
    print("===== 1. 原始資料診斷 =====")
    print(f"資料總筆數: {len(df)}")
    
    # --- 檢查重複值 ---
    duplicate_count = df.duplicated(subset=['customer_id']).sum()
    print(f"\n# 重複值檢查:")
    print(f"找到重複的 customer_id 數量: {duplicate_count}")
    
    # 執行刪除重複
    df = df.drop_duplicates(subset=['customer_id'])
    
    # --- 檢查缺失值 ---
    print(f"\n# 處理缺失值 (清洗前):")
    print(df[['age', 'FN', 'Active', 'club_member_status','fashion_news_frequency','postal_code']].isnull().sum())
    
    # 執行處理缺失值
    # age 用中位數填補
    age_median = df['age'].median()
    df['age'] = df['age'].fillna(age_median)
    df['age'] = df['age'].astype('int8')# 再轉整數
    
    # FN / Active 缺失代表 0
    df['FN'] = df['FN'].fillna(0)
    df['FN'] = df['FN'].astype('int8')  # 確保轉為 int8
    df['Active'] = df['Active'].fillna(0)
    df['Active'] = df['Active'].astype('int8')  # 確保轉為 int8
    
    # 會員狀態缺失補 'NONE'
    df['club_member_status'] = df['club_member_status'].fillna('NONE')
    # 郵遞區號缺失補 '0'
    df['postal_code'] = df['postal_code'].fillna('0')
    
    # fashion_news_frequency 缺失補 'NONE'
    df['fashion_news_frequency'] = df['fashion_news_frequency'].fillna('NONE')
    
    # --- 清洗檢查資訊 ---
    print(f"\n# 處理缺失值 (清洗後):")
    print(df[['age', 'FN', 'Active', 'club_member_status','fashion_news_frequency','postal_code']].isnull().sum())
    
    # 2. 格式轉換與異常過濾
    df['age'] = df['age'].astype(int)
    # 過濾掉年齡異常者 (例如 100 歲以上)
    df = df[df['age'] <= 100]
    
    print("\n===== 2. 清洗完成報告 =====")
    print(f"最終剩餘筆數: {len(df)}")
    print(f"平均年齡: {df['age'].mean():.2f}")
    
    return df

if __name__ == "__main__":
    # 假設檔案名為 customers.csv
    cleaned_customers = detailed_cleaning('./Assets/customers.csv')
    
    # 儲存結果
    cleaned_customers.to_csv('./Assets/customers_cleaned.csv', index=False)
    print("\n[OK] 清洗後的檔案已儲存至 customers_cleaned.csv")