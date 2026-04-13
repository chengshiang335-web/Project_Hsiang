import pandas as pd
import numpy as np
import time
import os
from tqdm import tqdm  # 如果沒安裝請執行: pip install tqdm

def clean_transactions_by_chunks(file_path, chunk_size=1000000):
    """
    使用分塊機制清洗大型交易資料
    :param file_path: CSV 路徑
    :param chunk_size: 每一批次處理的筆數 (預設一百萬筆)
    """
    print(f"--- 開始分塊清洗流程: {os.path.basename(file_path)} ---")
    start_all = time.time()
    
    # 獲取總筆數以計算進度 (這會花一點點時間，但對預估時間很重要)
    print("正在統計總筆數以預估剩餘時間...")
    total_rows = sum(1 for _ in open(file_path)) - 1 # 扣除標頭
    print(f"總筆數: {total_rows:,} 筆")

    # 定義優化的資料型態
    t_dtypes = {'article_id': 'int32', 'price': 'float32', 'sales_channel_id': 'int8'}
    
    chunks = []
    current_count = 0
    
    # 使用 tqdm 顯示動態進度條
    with tqdm(total=total_rows, unit='rows', desc="清洗進度") as pbar:
        # 分塊讀取
        reader = pd.read_csv(file_path, chunksize=chunk_size, dtype=t_dtypes)
        
        for i, chunk in enumerate(reader):
            batch_start = time.time()
            batch_size = len(chunk)
            
            # --- 執行清洗邏輯 ---
            chunk['t_dat'] = pd.to_datetime(chunk['t_dat'])
            chunk = chunk[chunk['price'] > 0].copy() # 排除異常價格
            
            # 收集清洗後的區塊
            chunks.append(chunk)
            
            # --- 更新計數器 ---
            current_count += batch_size
            batch_end = time.time()
            batch_duration = batch_end - batch_start
            
            # --- 更新進度條報告 ---
            # tqdm 會自動處理：【當前清洗筆數】、【預估完成剩餘時間】
            # 我們手動輸出詳細資訊
            pbar.update(batch_size)
            
            if (i + 1) % 5 == 0 or current_count >= total_rows:
                print(f"\n批次 {i+1} 報告:")
                print(f"  - 該批次清洗筆數: {batch_size:,}")
                print(f"  - 當前累計筆數: {current_count:,} / {total_rows:,}")
                print(f"  - 該批次耗時: {batch_duration:.2f} 秒")
                print(f"  - 累計已花費時間: {time.time() - start_all:.2f} 秒")

    # 合併所有區塊
    print("\n--- 正在合併分塊資料 ---")
    full_df = pd.concat(chunks, axis=0)
    
    # --- 最終清洗報告 ---
    end_all = time.time()
    mem_final = full_df.memory_usage(deep=True).sum() / 1024**2
    
    print("\n" + "="*40)
    print("【最終清洗報告】")
    print(f"1. 總筆數 (清洗後): {len(full_df):,}")
    print(f"2. 實際總花費時間: {end_all - start_all:.2f} 秒")
    print(f"3. 最終記憶體占用: {mem_final:.2f} MB")
    print(f"4. 時間跨度: {full_df['t_dat'].min().date()} 至 {full_df['t_dat'].max().date()}")
    print(f"5. 平均清洗速率: {total_rows / (end_all - start_all):,.0f} 筆/秒")
    print("="*40)
    
    return full_df

if __name__ == "__main__":
    file_path = './Assets/transactions_train.csv'
    
    if os.path.exists(file_path):
        try:
            # 執行分塊清洗
            df_final = clean_transactions_by_chunks(file_path, chunk_size=2000000)
            
            # 儲存結果
            df_final.to_csv('./Assets/clean_transactions.csv', index=False)
            print("\n[OK] 清洗後的檔案已儲存至 clean_transactions.csv")

            # 建議保存為高效格式，避免下次又要清洗一次
            # df_final.to_parquet('transactions_cleaned.parquet')
            
        except Exception as e:
            print(f"執行過程中發生錯誤: {e}")
    else:
        print(f"錯誤: 找不到檔案 {file_path}")