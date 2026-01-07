import argparse
import csv
import os
import re
from typing import List, Dict, Tuple

import numpy as np
import pandas as pd
from scipy import stats


DATE_RE = re.compile(r"^\d{1,2}\.\d{1,2}$")
NUM_RE = re.compile(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?")


def _safe_decode(filepath: str) -> List[List[str]]:
    """Read a possibly messy CSV with unknown encoding into a list of rows (list of tokens).

    Tries utf-8-sig first, then gbk. Preserves empty cells.
    """
    for enc in ("utf-8-sig", "utf-8", "gbk"):
        try:
            with open(filepath, "r", encoding=enc, newline="") as f:
                reader = csv.reader(f)
                return [list(row) for row in reader]
        except Exception:
            continue
    # Fallback: binary read + best-effort split on commas
    with open(filepath, "rb") as f:
        data = f.read().decode(errors="ignore")
    return [line.split(",") for line in data.splitlines()]


def _extract_first_float(token: str) -> float:
    """Extract first numeric value from a token like '2.48:1' or '  586 '. Returns np.nan if none."""
    m = NUM_RE.search(token)
    if not m:
        return np.nan
    try:
        return float(m.group(0))
    except Exception:
        return np.nan


def parse_sections(rows: List[List[str]]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Parse the provided CSV rows into two DataFrames.

    Returns:
    - replicates_df: columns = ['date','group','replicate','value'] for up to first 12 numeric entries per group line
    - summaries_df: columns = ['date','group','key','value'] parsed from any trailing summary cells with Chinese headers
    """
    replicates_records: List[Dict] = []
    summaries_records: List[Dict] = []

    current_date = None

    # Heuristic for summary header mapping from the first row if it contains Chinese labels
    header_map: List[str] = []
    if rows:
        first = rows[0]
        # attempt to find meaningful header labels in the tail of the first row
        tail_labels = [c.strip() for c in first if c.strip()]
        # Keep labels containing Chinese or known keywords
        header_map = [
            c for c in tail_labels
            if any(k in c for k in ["总重", "平均重", "总增重", "总日增重", "单个日增重", "耗料量", "料肉比", "经济成本"])
        ]

    for row in rows:
        if not row:
            continue
        first_cell = (row[0] or "").strip()
        if DATE_RE.match(first_cell):
            current_date = first_cell
            continue

        if first_cell in ("甜菜碱组", "对照组"):
            group = first_cell
            # Extract up to first 12 numeric tokens as replicates
            replicates: List[float] = []
            for token in row[1:]:
                if len(replicates) >= 12:
                    break
                val = _extract_first_float(token)
                if not np.isnan(val):
                    replicates.append(val)

            for i, v in enumerate(replicates, start=1):
                replicates_records.append({
                    "date": current_date,
                    "group": group,
                    "replicate": i,
                    "value": v,
                })

            # Parse trailing summary values if header_map present
            if header_map:
                # Find tail numeric tokens beyond the 12 replicates
                tail_tokens = row[1+len(replicates):]
                tail_values: List[float] = []
                for token in tail_tokens:
                    val = _extract_first_float(token)
                    if not np.isnan(val):
                        tail_values.append(val)
                # Align first len(header_map) values
                for k, v in zip(header_map, tail_values):
                    summaries_records.append({
                        "date": current_date,
                        "group": group,
                        "key": k,
                        "value": v,
                    })

    replicates_df = pd.DataFrame(replicates_records)
    summaries_df = pd.DataFrame(summaries_records)
    return replicates_df, summaries_df


def welch_t_test_by_date(df: pd.DataFrame) -> pd.DataFrame:
    """Compute Welch's t-test for '甜菜碱组' vs '对照组' per date on replicate 'value'.

    Returns a summary DataFrame with statistics.
    """
    results: List[Dict] = []
    for date, sub in df.groupby("date"):
        g1 = sub[sub["group"] == "甜菜碱组"]["value"].dropna().to_numpy()
        g2 = sub[sub["group"] == "对照组"]["value"].dropna().to_numpy()
        if len(g1) == 0 or len(g2) == 0:
            continue
        # Welch's t-test
        t_stat, p_val = stats.ttest_ind(g1, g2, equal_var=False)
        # Effect size (Hedges' g)
        n1, n2 = len(g1), len(g2)
        mean1, mean2 = float(np.mean(g1)), float(np.mean(g2))
        var1 = float(np.var(g1, ddof=1)) if n1 > 1 else np.nan
        var2 = float(np.var(g2, ddof=1)) if n2 > 1 else np.nan
        # Cohen's d (pooled SD)
        s_pooled = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)) if (n1 + n2 - 2) > 0 else np.nan
        cohen_d = (mean1 - mean2) / s_pooled if s_pooled and not np.isnan(s_pooled) and s_pooled != 0 else np.nan
        # Small sample correction (Hedges' g)
        hedges_g = cohen_d * (1 - (3 / (4 * (n1 + n2) - 9))) if cohen_d and not np.isnan(cohen_d) else np.nan
        results.append({
            "date": date,
            "n_甜菜碱组": n1,
            "n_对照组": n2,
            "mean_甜菜碱组": round(mean1, 3),
            "mean_对照组": round(mean2, 3),
            "mean_diff": round(mean1 - mean2, 3),
            "t_stat": round(float(t_stat), 4) if t_stat is not None else np.nan,
            "p_value": round(float(p_val), 6) if p_val is not None else np.nan,
            "hedges_g": round(float(hedges_g), 4) if not np.isnan(hedges_g) else np.nan,
        })
    return pd.DataFrame(results).sort_values("date")


def main():
    parser = argparse.ArgumentParser(description="Analyze significance between groups per date from messy CSV.")
    parser.add_argument("input", help="输入CSV路径，例如 analysis/甜菜碱组数据结果.csv")
    parser.add_argument("--out", default=None, help="输出结果CSV路径，默认写到 analysis/significance_results.csv")
    args = parser.parse_args()

    rows = _safe_decode(args.input)
    replicates_df, summaries_df = parse_sections(rows)

    if replicates_df.empty:
        print("未解析到任何重复数据（前12列）。请检查文件格式。")
        return

    results_df = welch_t_test_by_date(replicates_df)

    out_path = args.out
    if not out_path:
        # default under analysis/
        base_dir = os.path.dirname(os.path.abspath(args.input))
        out_path = os.path.join(base_dir, "significance_results.csv")

    results_df.to_csv(out_path, index=False, encoding="utf-8-sig")

    print("按日期的Welch t检验：")
    print(results_df.to_string(index=False))
    print(f"\n结果已保存：{out_path}")

    # Optional: show summaries keys found
    if not summaries_df.empty:
        keys = sorted(set(summaries_df["key"]))
        print(f"\n识别到的汇总指标: {', '.join(keys)}")


if __name__ == "__main__":
    main()
