import argparse
import csv
import os
import re
from typing import List, Dict, Tuple, Optional, Set


def read_text(path: str) -> str:
    for enc in ("utf-8", "utf-8-sig", "gbk", "latin-1"):
        try:
            with open(path, "r", encoding=enc, errors="ignore") as f:
                return f.read()
        except Exception:
            continue
    with open(path, "rb") as f:
        return f.read().decode(errors="ignore")


# Patterns for NPA (Natural Population Analysis) charges
NPA_HEADER_RE = re.compile(r"Natural\s+Population\s+Analysis", re.IGNORECASE)
NPA_CHARGE_LINE_RE = re.compile(
    r"^\s*(\w{1,2})\s*(\d+)\s+([+-]?[0-9]*\.?[0-9]+)\s*$"
)

# Patterns for E(2) donor-acceptor interactions
E2_HEADER_RE = re.compile(
    r"Second\s+Order\s+Perturbation\s+Theory\s+Analysis\s+of\s+Fock\s+Matrix",
    re.IGNORECASE,
)
E2_LINE_RE = re.compile(
    r"(?P<donor>(LP|BD|BD\*|RY)\s*\(.*?\)\s*[A-Za-z0-9\-*]+)\s*->\s*(?P<acceptor>(LP|BD|BD\*|RY)\s*\(.*?\)\s*[A-Za-z0-9\-*]+).*?E\(2\)\s*=\s*(?P<e2>[0-9]*\.?[0-9]+)",
    re.IGNORECASE,
)


def extract_atom_symbols(text: str) -> List[str]:
    """Extract atom symbols in input order from 'Symbolic Z-matrix' section.

    Returns a list like ['Fe','C','C',...], index starting from 1.
    """
    lines = text.splitlines()
    symbols: List[str] = []
    in_sym = False
    for line in lines:
        if not in_sym and line.strip().startswith("Symbolic Z-matrix"):
            in_sym = True
            continue
        if in_sym:
            if line.strip() == "":
                # stop at first blank after entries
                if symbols:
                    break
                else:
                    continue
            # line starts with element symbol followed by coordinates
            parts = line.strip().split()
            if len(parts) >= 4:
                sym = parts[0]
                if re.match(r"^[A-Za-z]{1,2}$", sym):
                    symbols.append(sym)
    return symbols


def nbo_label_indices(label: str) -> Set[int]:
    """Extract atom indices appearing in NBO label like 'BD (C-N) 20' or 'LP (N) 12'."""
    idxs: Set[int] = set()
    # capture trailing index
    m = re.search(r"\b(\d{1,4})\b", label)
    if m:
        try:
            idxs.add(int(m.group(1)))
        except Exception:
            pass
    # also inside parentheses may have numbers if format differs
    for mm in re.finditer(r"\(([^)]*)\)", label):
        for x in re.findall(r"\b(\d{1,4})\b", mm.group(1)):
            try:
                idxs.add(int(x))
            except Exception:
                pass
    return idxs


def filter_interactions_by_atoms(interactions: List[Dict], target_atoms: Set[int]) -> List[Dict]:
    out: List[Dict] = []
    for it in interactions:
        d_idxs = nbo_label_indices(it["donor"]) if it.get("donor") else set()
        a_idxs = nbo_label_indices(it["acceptor"]) if it.get("acceptor") else set()
        if (d_idxs & target_atoms) or (a_idxs & target_atoms):
            out.append(it)
    return out


def extract_npa_charges(text: str) -> List[Dict]:
    lines = text.splitlines()
    charges: List[Dict] = []
    in_npa = False
    for i, line in enumerate(lines):
        if not in_npa and NPA_HEADER_RE.search(line):
            in_npa = True
            # continue scanning following lines
            continue
        if in_npa:
            # stop when a blank block ends or a new section starts
            if line.strip() == "" and len(charges) > 0:
                break
            m = NPA_CHARGE_LINE_RE.match(line)
            if m:
                elem, idx, q = m.groups()
                try:
                    charges.append({"elem": elem, "index": int(idx), "charge": float(q)})
                except Exception:
                    pass
    return charges


def extract_e2_interactions(text: str, max_count: int = 200) -> List[Dict]:
    interactions: List[Dict] = []
    lines = text.splitlines()
    in_e2 = False
    for i, line in enumerate(lines):
        if not in_e2 and E2_HEADER_RE.search(line):
            in_e2 = True
            continue
        if in_e2:
            if line.strip() == "":
                # tolerate blank lines
                pass
            # Stop when another big header appears
            if "Natural" in line and "Bond" in line and "Orbital" in line:
                break
            m = E2_LINE_RE.search(line)
            if m:
                donor = m.group("donor").strip()
                acceptor = m.group("acceptor").strip()
                e2 = float(m.group("e2"))
                interactions.append({"donor": donor, "acceptor": acceptor, "E2_kcal": e2})
                if len(interactions) >= max_count:
                    break
    # sort by E2 descending
    interactions.sort(key=lambda x: x["E2_kcal"], reverse=True)
    return interactions


def summarize_charges(charges: List[Dict]) -> Dict:
    summary: Dict[str, Dict[str, float]] = {}
    # per element average
    by_elem: Dict[str, List[float]] = {}
    for c in charges:
        by_elem.setdefault(c["elem"], []).append(c["charge"])
    summary["per_element_avg"] = {k: sum(v) / len(v) for k, v in by_elem.items() if v}
    # totals
    total = sum(c["charge"] for c in charges)
    summary["total_charge"] = total
    summary["count"] = len(charges)
    return summary


def compare_charges(a: List[Dict], b: List[Dict]) -> Dict:
    sa = summarize_charges(a)
    sb = summarize_charges(b)
    elems = set(sa["per_element_avg"].keys()) | set(sb["per_element_avg"].keys())
    elem_diff = {}
    for e in sorted(elems):
        va = sa["per_element_avg"].get(e)
        vb = sb["per_element_avg"].get(e)
        if va is None or vb is None:
            diff = None
        else:
            diff = va - vb
        elem_diff[e] = {"avg_a": va, "avg_b": vb, "delta": diff}
    return {
        "total_charge_a": sa["total_charge"],
        "total_charge_b": sb["total_charge"],
        "count_a": sa["count"],
        "count_b": sb["count"],
        "per_element_avg_diff": elem_diff,
    }


def compare_e2(a: List[Dict], b: List[Dict], top_n: int = 20) -> Dict:
    sum_a = sum(x["E2_kcal"] for x in a)
    sum_b = sum(x["E2_kcal"] for x in b)
    top_a = a[:top_n]
    top_b = b[:top_n]
    # create sets for overlap by donor-acceptor label
    key = lambda x: (x["donor"], x["acceptor"])
    set_a = {key(x) for x in a}
    set_b = {key(x) for x in b}
    overlap = sorted(list(set_a & set_b))
    return {
        "sum_e2_a": sum_a,
        "sum_e2_b": sum_b,
        "delta_sum": sum_a - sum_b,
        "top_a": top_a,
        "top_b": top_b,
        "overlap_pairs": overlap,
    }


def write_csv(path: str, rows: List[Dict], fieldnames: List[str]):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k) for k in fieldnames})


def write_markdown_report(path: str, charge_cmp: Dict, e2_cmp: Dict, file_a: str, file_b: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    lines: List[str] = []
    lines.append(f"# NBO差异报告\n")
    lines.append(f"- 文件A: {file_a}\n- 文件B: {file_b}\n")
    lines.append("\n## NPA电荷对比\n")
    lines.append(
        f"- 总电荷: A={charge_cmp['total_charge_a']:.4f}, B={charge_cmp['total_charge_b']:.4f}, Δ={charge_cmp['total_charge_a']-charge_cmp['total_charge_b']:.4f}\n"
    )
    lines.append("- 原子计数: A=%d, B=%d\n" % (charge_cmp["count_a"], charge_cmp["count_b"]))
    lines.append("\n- 元素平均电荷差（A-B）：\n")
    lines.append("\n| 元素 | A均值 | B均值 | Δ |\n|---|---:|---:|---:|\n")
    for e, rec in charge_cmp["per_element_avg_diff"].items():
        va = rec["avg_a"]
        vb = rec["avg_b"]
        d = rec["delta"]
        def fmt(x):
            return ("%.4f" % x) if x is not None else "-"
        lines.append(f"| {e} | {fmt(va)} | {fmt(vb)} | {fmt(d)} |\n")

    lines.append("\n## E(2)二阶相互作用对比\n")
    lines.append(
        f"- 总E(2)稳定能: A={e2_cmp['sum_e2_a']:.2f} kcal/mol, B={e2_cmp['sum_e2_b']:.2f} kcal/mol, Δ={e2_cmp['delta_sum']:.2f}\n"
    )
    lines.append("- 重叠的供体→受体对数量: %d\n" % len(e2_cmp["overlap_pairs"]))
    lines.append("\n- A前20强相互作用（E(2)）：\n")
    lines.append("\n| Donor | Acceptor | E(2) (kcal/mol) |\n|---|---|---:|\n")
    for x in e2_cmp["top_a"]:
        lines.append(f"| {x['donor']} | {x['acceptor']} | {x['E2_kcal']:.2f} |\n")
    lines.append("\n- B前20强相互作用（E(2)）：\n")
    lines.append("\n| Donor | Acceptor | E(2) (kcal/mol) |\n|---|---|---:|\n")
    for x in e2_cmp["top_b"]:
        lines.append(f"| {x['donor']} | {x['acceptor']} | {x['E2_kcal']:.2f} |\n")

    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(lines))


def main():
    ap = argparse.ArgumentParser(description="Compare two Gaussian NBO log files (NPA charges and E(2) interactions)")
    ap.add_argument("file_a", help="路径到第一个NBO日志文件")
    ap.add_argument("file_b", help="路径到第二个NBO日志文件")
    ap.add_argument("--outdir", default="analysis/nbo_compare", help="输出目录")
    args = ap.parse_args()

    # Prepare output dir first
    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)

    text_a = read_text(args.file_a)
    text_b = read_text(args.file_b)

    # Atom symbols and mapping
    atoms_a = extract_atom_symbols(text_a)
    atoms_b = extract_atom_symbols(text_b)

    npa_a = extract_npa_charges(text_a)
    npa_b = extract_npa_charges(text_b)
    e2_a = extract_e2_interactions(text_a)
    e2_b = extract_e2_interactions(text_b)

    if not npa_a and not npa_b and not e2_a and not e2_b:
        report_path = os.path.join(outdir, "nbo_compare_report.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(
                "# NBO差异报告\n\n"
                f"- 文件A: {args.file_a}\n- 文件B: {args.file_b}\n\n"
                "未识别到 NPA 或 E(2) 数据。\n"
                "请确认Gaussian输入包含 NBO 输出（例如 `pop=(nbo)` 或 `pop=(nboread)`），并提供完整日志。\n"
            )
        print("未识别到NPA/E(2)。已写出占位报告：", report_path)
        return

    cmp_charge = compare_charges(npa_a, npa_b)
    cmp_e2 = compare_e2(e2_a, e2_b)

    # Targeted analysis per user request:
    # Focus on atoms: 1 with 12,13 and with other CN groups; 14 and 15 onwards (histidine ligand part)
    targets_core: Set[int] = {1, 12, 13}
    # CN group heuristic: all atoms labeled C or N
    cn_atoms_a = {i+1 for i, s in enumerate(atoms_a) if s.upper() in {"C", "N"}}
    cn_atoms_b = {i+1 for i, s in enumerate(atoms_b) if s.upper() in {"C", "N"}}
    histidine_range_a = {i+1 for i in range(len(atoms_a)) if (i+1) >= 14}
    histidine_range_b = {i+1 for i in range(len(atoms_b)) if (i+1) >= 14}

    e2_core_a = filter_interactions_by_atoms(e2_a, targets_core)
    e2_core_b = filter_interactions_by_atoms(e2_b, targets_core)
    e2_cn_a = filter_interactions_by_atoms(e2_a, cn_atoms_a | {1})
    e2_cn_b = filter_interactions_by_atoms(e2_b, cn_atoms_b | {1})
    e2_his_a = filter_interactions_by_atoms(e2_a, histidine_range_a)
    e2_his_b = filter_interactions_by_atoms(e2_b, histidine_range_b)

    # Write targeted CSVs
    write_csv(os.path.join(outdir, "e2_focus_core_A.csv"), e2_core_a, ["donor", "acceptor", "E2_kcal"])
    write_csv(os.path.join(outdir, "e2_focus_core_B.csv"), e2_core_b, ["donor", "acceptor", "E2_kcal"])
    write_csv(os.path.join(outdir, "e2_focus_CN_A.csv"), e2_cn_a, ["donor", "acceptor", "E2_kcal"])
    write_csv(os.path.join(outdir, "e2_focus_CN_B.csv"), e2_cn_b, ["donor", "acceptor", "E2_kcal"])
    write_csv(os.path.join(outdir, "e2_focus_histidine_A.csv"), e2_his_a, ["donor", "acceptor", "E2_kcal"])
    write_csv(os.path.join(outdir, "e2_focus_histidine_B.csv"), e2_his_b, ["donor", "acceptor", "E2_kcal"])

    # outdir already created

    # Write CSVs
    write_csv(os.path.join(outdir, "npa_charges_A.csv"), npa_a, ["elem", "index", "charge"])
    write_csv(os.path.join(outdir, "npa_charges_B.csv"), npa_b, ["elem", "index", "charge"])
    write_csv(os.path.join(outdir, "e2_A.csv"), e2_a, ["donor", "acceptor", "E2_kcal"])
    write_csv(os.path.join(outdir, "e2_B.csv"), e2_b, ["donor", "acceptor", "E2_kcal"])

    # Markdown report
    report_path = os.path.join(outdir, "nbo_compare_report.md")
    write_markdown_report(report_path, cmp_charge, cmp_e2, args.file_a, args.file_b)

    print("完成NBO对比与指定区域筛选。")
    print(f"- NPA与E(2)CSV已输出到: {outdir}")
    print(f"- 差异报告: {report_path}")


if __name__ == "__main__":
    main()
