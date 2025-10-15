from pathlib import Path
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from config import get_connection

SQL_DIR = Path("sql")
OUT_DIR = Path("outputs")
OUT_DIR.mkdir(exist_ok=True)

def read_sql(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def run_sql(path: Path, params=None) -> pd.DataFrame:
    query = read_sql(path)
    conn = get_connection()
    try:
        df = pd.read_sql(query, conn, params=params)
    finally:
        conn.close()
    return df

# 你已經有的：各主類別成功率
def plot_success_rate_by_category():
    sql_path = SQL_DIR / "01_success_rate_by_category.sql"
    df = run_sql(sql_path)
    if df.empty:
        print("⚠️ No data for 01_success_rate_by_category.sql"); return

    df = df.sort_values("success_rate", ascending=False)

    plt.figure(figsize=(12, 7))
    bars = plt.bar(df["main_category"], df["success_rate"])
    top_cat, top_rate = df.iloc[0]["main_category"], df.iloc[0]["success_rate"]
    plt.text(top_cat, top_rate + 1, f"⭐ {top_cat} ({top_rate:.1f}%)",
             ha="center", va="bottom", fontsize=12, fontweight="bold")

    plt.title("Kickstarter Success Rate by Category", fontsize=18, fontweight="bold", pad=20)
    plt.xlabel("Main Category"); plt.ylabel("Success Rate (%)")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.gca().spines["right"].set_visible(False); plt.gca().spines["top"].set_visible(False)
    plt.tight_layout()
    out = OUT_DIR / "01_success_rate_by_category.png"
    plt.savefig(out, dpi=300, bbox_inches="tight"); plt.close()
    print(f"✅ saved: {out}")

# ➊ 年度成功率趨勢
def plot_yearly_success_trend():
    sql_path = SQL_DIR / "02_yearly_success_trend.sql"
    df = run_sql(sql_path)
    if df.empty:
        print("⚠️ No data for 02_yearly_success_trend.sql"); return
    df = df[df["yr"].notna()]

    plt.figure(figsize=(10, 5))
    plt.plot(df["yr"], df["success_rate"], marker="o")
    plt.title("Yearly Success Rate Trend", fontsize=18, fontweight="bold", pad=16)
    plt.xlabel("Year"); plt.ylabel("Success Rate (%)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    out = OUT_DIR / "02_yearly_success_trend.png"
    plt.savefig(out, dpi=300, bbox_inches="tight"); plt.close()
    print(f"✅ saved: {out}")

# ➋ 各國 × 指定主類別 的成功率（參數：category, min_samples）
def plot_country_success_for_category(category: str = "Games", min_samples: int = 50):
    sql_path = SQL_DIR / "03_country_success_for_category.sql"
    df = run_sql(sql_path, params=[category, min_samples])
    if df.empty:
        print(f"⚠️ No data for category='{category}' with min_samples>={min_samples}"); return

    plt.figure(figsize=(12, 6))
    plt.bar(df["country"], df["success_rate"])
    plt.title(f"Success Rate by Country — {category} (n ≥ {min_samples})",
              fontsize=18, fontweight="bold", pad=16)
    plt.xlabel("Country"); plt.ylabel("Success Rate (%)")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    out = OUT_DIR / f"03_country_success_{category}.png"
    plt.savefig(out, dpi=300, bbox_inches="tight"); plt.close()
    print(f"✅ saved: {out}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", default="Games", help="Main category for country chart")
    parser.add_argument("--min-samples", type=int, default=50, help="Min samples per country")
    args = parser.parse_args()

    plot_success_rate_by_category()
    plot_yearly_success_trend()
    plot_country_success_for_category(args.category, args.min_samples)

    print("🎉 charts generated under ./outputs")
