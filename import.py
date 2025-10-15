# import_data.py
import pandas as pd
from config import get_connection

CSV_PATH = "data/ks-projects-201801.csv"   # 改成你的實際路徑也可

def main():
    # 1) 讀 CSV
    df = pd.read_csv(CSV_PATH)

    # 2) 欄位改名（處理有空白的 'usd pledged'）
    df = df.rename(columns={
        "usd pledged": "usd_pledged_legacy"
    })

    # 3) 只保留需要的欄位（照表的順序）
    df = df[[
        "ID", "name", "category", "main_category", "currency",
        "deadline", "launched", "goal", "pledged",
        "state", "backers", "country",
        "usd_pledged_legacy", "usd_pledged_real", "usd_goal_real"
    ]]

    # 4) 轉型：日期、數值
    df["deadline"] = pd.to_datetime(df["deadline"], errors="coerce")
    df["launched"] = pd.to_datetime(df["launched"], errors="coerce")

    num_cols = ["goal", "pledged", "backers", "usd_pledged_legacy", "usd_pledged_real", "usd_goal_real"]
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # 可先小批量測試
    # df = df.head(5000)

    # 5) 寫入 MySQL
    conn = get_connection()
    cur = conn.cursor()

    insert_sql = """
    INSERT INTO projects
    (id, name, category, main_category, currency, deadline, launched,
     goal, pledged, state, backers, country,
     usd_pledged_legacy, usd_pledged_real, usd_goal_real)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    # 轉成 tuple 列表（None 會進 DB 的 NULL）
    rows = [
        (
            int(row["ID"]) if pd.notna(row["ID"]) else None,
            row["name"] if pd.notna(row["name"]) else None,
            row["category"] if pd.notna(row["category"]) else None,
            row["main_category"] if pd.notna(row["main_category"]) else None,
            row["currency"] if pd.notna(row["currency"]) else None,
            row["deadline"].to_pydatetime() if pd.notna(row["deadline"]) else None,
            row["launched"].to_pydatetime() if pd.notna(row["launched"]) else None,
            float(row["goal"]) if pd.notna(row["goal"]) else None,
            float(row["pledged"]) if pd.notna(row["pledged"]) else None,
            row["state"] if pd.notna(row["state"]) else None,
            int(row["backers"]) if pd.notna(row["backers"]) else None,
            row["country"] if pd.notna(row["country"]) else None,
            float(row["usd_pledged_legacy"]) if pd.notna(row["usd_pledged_legacy"]) else None,
            float(row["usd_pledged_real"]) if pd.notna(row["usd_pledged_real"]) else None,
            float(row["usd_goal_real"]) if pd.notna(row["usd_goal_real"]) else None,
        )
        for _, row in df.iterrows()
    ]

    # 分批寫入，避免單次太大
    BATCH = 5000
    total = 0
    for i in range(0, len(rows), BATCH):
        chunk = rows[i:i+BATCH]
        cur.executemany(insert_sql, chunk)
        conn.commit()
        total += len(chunk)

    cur.close()
    conn.close()
    print(f"✅ 成功匯入 {total} 筆資料！")

if __name__ == "__main__":
    main()
