import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple

NAO_KEYWORDS = [
    'Natural Atomic Orbitals',
    'NAO',
    'NAOMO',
    'MOs in the NAO basis',
]

# Regex patterns for hybrid composition lines. Handles orders like s(%), p(%), d(%) appearing in any order.
COMP_PATTERN = re.compile(r"(s\(\s*([0-9]+(?:\.[0-9]+)?)%\))|(p\(\s*([0-9]+(?:\.[0-9]+)?)%\))|(d\(\s*([0-9]+(?:\.[0-9]+)?)%\))", re.IGNORECASE)
# Regex patterns for explicit AO contribution lines (e.g., s 0.123, px 0.456, ...). We will sum to s/p/d buckets.
# Pattern for floats
FLOAT_PATTERN = re.compile(r"[+-]?(?:\d*\.\d+|\d+)(?:[eE][+-]?\d+)?")
# Occupancy pattern if present near NAO header
OCC_PATTERN = re.compile(r"Occupancy\s*=\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE)
# Atom annotation often appears like: Fe   1 or Cu  14 near NAO blocks
# Match atom symbol with optional spaceless index (e.g., "Cu14" or "Fe 1")
ATOM_PATTERN = re.compile(r"\b([A-Z][a-z]?)\s*(\d+)\b")


def extract_nao_related_lines(lines: List[str]) -> List[str]:
    out: List[str] = []
    # Capture lines that contain NAO keywords and a small window around them
    window = 8
    for i, line in enumerate(lines):
        if any(k in line for k in NAO_KEYWORDS):
            start = max(0, i - 2)
            end = min(len(lines), i + window)
            out.extend(lines[start:end])
    # Deduplicate while retaining order
    seen = set()
    out_unique = []
    for l in out:
        if l not in seen:
            out_unique.append(l)
            seen.add(l)
    return out_unique


def parse_nao_mo_matrix(lines: List[str]) -> Dict[Tuple[str, str], Dict[str, float]]:
    """
    Parse the "MOs in the NAO basis" matrix and accumulate squared coefficients per atom into s/p/d buckets.
    Returns mapping: (atom, index) -> {'s': total, 'p': total, 'd': total, 'count': n}
    """
    acc: Dict[Tuple[str, str], Dict[str, float]] = {}
    in_block = False
    for line in lines:
        if 'MOs in the NAO basis' in line:
            in_block = True
            continue
        if in_block:
            # Data lines start with number and dot
            if re.match(r"^\s*\d+\.", line):
                m_atom = ATOM_PATTERN.search(line)
                m_label = re.search(r"\(([^)]+)\)", line)
                if not (m_atom and m_label):
                    continue
                atom, idx = m_atom.group(1), m_atom.group(2)
                label = m_label.group(1).strip().lower()
                pos = line.find(')')
                tail = line[pos+1:] if pos != -1 else line
                coeffs = [float(x) for x in FLOAT_PATTERN.findall(tail)]
                if not coeffs:
                    continue
                val = sum(c*c for c in coeffs)
                key = (atom, idx)
                acc.setdefault(key, {'s': 0.0, 'p': 0.0, 'd': 0.0, 'count': 0.0})
                if label == 's':
                    acc[key]['s'] += val
                elif label in ('px', 'py', 'pz'):
                    acc[key]['p'] += val
                elif label.startswith('d'):
                    acc[key]['d'] += val
                # count lines for diagnostics
                acc[key]['count'] += 1
            else:
                # Heuristic end: if we hit a blank line after block or a new header, we can leave in_block when needed
                if line.strip() == '' and in_block:
                    # Keep in_block True; matrix may span multiple pages. We only exit when a new major section starts.
                    continue
                if 'Second Order Perturbation Theory' in line or 'NHO Directionality' in line:
                    in_block = False
    return acc


def make_atom_summary_from_matrix(acc: Dict[Tuple[str, str], Dict[str, float]]) -> List[Dict[str, str]]:
    agg: List[Dict[str, str]] = []
    for (atom, idx), vals in acc.items():
        s = vals['s']
        p = vals['p']
        d = vals['d']
        total = s + p + d
        if total <= 0:
            continue
        agg.append({
            'atom': atom,
            'index': idx,
            'entries': f"{int(vals['count'])}",
            's_pct': f"{100.0*s/total:.2f}",
            'p_pct': f"{100.0*p/total:.2f}",
            'd_pct': f"{100.0*d/total:.2f}",
        })
    # Sort heavy atoms first then hydrogens
    def sort_key(e):
        return (e['atom'] == 'H', int(e['index']))
    agg.sort(key=sort_key)
    return agg

def parse_natural_electron_configuration(lines: List[str]) -> Dict[Tuple[str, str], Dict[str, float]]:
    """
    Parse the "Natural Electron Configuration" table and aggregate s/p/d electron counts per atom.
    Returns mapping: (atom, index) -> {'s': electrons, 'p': electrons, 'd': electrons}
    """
    acc: Dict[Tuple[str, str], Dict[str, float]] = {}
    in_section = False
    header_seen = False
    # Pattern: shell + orbital letter + (value)
    conf_pat = re.compile(r"(\d+)([spdfSPDF])\(\s*([0-9]+(?:\.[0-9]+)?)\)")
    for line in lines:
        if 'Natural Electron Configuration' in line:
            in_section = True
            header_seen = True
            continue
        if in_section:
            if line.strip().startswith('----'):
                # separator line; continue
                continue
            # Terminate section on blank line or next major header
            if line.strip() == '' and header_seen:
                in_section = False
                header_seen = False
                continue
            m_atom = ATOM_PATTERN.search(line)
            if not m_atom:
                # Non-data line; skip
                continue
            atom, idx = m_atom.group(1), m_atom.group(2)
            key = (atom, idx)
            acc.setdefault(key, {'s': 0.0, 'p': 0.0, 'd': 0.0})
            for m in conf_pat.finditer(line):
                shell, orb, val = m.group(1), m.group(2).lower(), float(m.group(3))
                if orb == 's':
                    acc[key]['s'] += val
                elif orb == 'p':
                    acc[key]['p'] += val
                elif orb == 'd':
                    acc[key]['d'] += val
    return acc

def make_atom_summary_from_occupancy(acc: Dict[Tuple[str, str], Dict[str, float]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for (atom, idx), vals in acc.items():
        s = vals['s']; p = vals['p']; d = vals['d']
        total = s + p + d
        if total <= 0:
            continue
        rows.append({
            'atom': atom,
            'index': idx,
            's_e': f"{s:.3f}",
            'p_e': f"{p:.3f}",
            'd_e': f"{d:.3f}",
            's_pct': f"{100.0*s/total:.2f}",
            'p_pct': f"{100.0*p/total:.2f}",
            'd_pct': f"{100.0*d/total:.2f}",
        })
    def sort_key(e):
        return (e['atom'] == 'H', int(e['index']))
    rows.sort(key=sort_key)
    return rows

def parse_nao_mo_labels(lines: List[str]) -> Dict[Tuple[str, str], Dict[str, float]]:
    """
    Parse NAO-MO matrix and accumulate per NAO label (S, px, py, pz, d1..d5) squared coefficients per atom.
    Returns mapping: (atom, index) -> {label: total}
    """
    acc: Dict[Tuple[str, str], Dict[str, float]] = {}
    in_block = False
    for line in lines:
        if 'MOs in the NAO basis' in line:
            in_block = True
            continue
        if in_block:
            if re.match(r"^\s*\d+\.", line):
                m_atom = ATOM_PATTERN.search(line)
                m_label = re.search(r"\(([^)]+)\)", line)
                if not (m_atom and m_label):
                    continue
                atom, idx = m_atom.group(1), m_atom.group(2)
                label = m_label.group(1).strip().lower()
                if label not in ('s', 'px', 'py', 'pz') and not label.startswith('d'):
                    continue
                pos = line.find(')')
                tail = line[pos+1:] if pos != -1 else line
                coeffs = [float(x) for x in FLOAT_PATTERN.findall(tail)]
                if not coeffs:
                    continue
                val = sum(c*c for c in coeffs)
                key = (atom, idx)
                acc.setdefault(key, {})
                acc[key][label] = acc[key].get(label, 0.0) + val
            else:
                if 'Second Order Perturbation Theory' in line or 'NHO Directionality' in line:
                    in_block = False
    return acc

def write_label_breakdown(out_dir: Path, labels_acc: Dict[Tuple[str, str], Dict[str, float]]):
    path = out_dir / 'NAO_labels_by_atom.csv'
    with path.open('w', encoding='utf-8') as f:
        f.write('atom,index,label,weight,pct\n')
        for (atom, idx), labels in sorted(labels_acc.items(), key=lambda k: (k[0][0]=='H', int(k[0][1]))):
            total = sum(labels.values())
            if total <= 0:
                continue
            for label, w in sorted(labels.items()):
                pct = 100.0 * w / total
                f.write(f"{atom},{idx},{label},{w:.6e},{pct:.2f}\n")
    return path


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/parse_nao_spd.py <path-to-gaussian-nbo-log>")
        sys.exit(1)
    log_path = Path(sys.argv[1])
    if not log_path.exists():
        print(f"Error: log file not found: {log_path}")
        sys.exit(2)

    out_dir = Path(__file__).resolve().parents[1] / 'analysis'
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_lines = log_path.read_text(encoding='utf-8', errors='ignore').splitlines()

    # Extract NAO-related lines first for inspection
    nao_related = extract_nao_related_lines(raw_lines)
    (out_dir / 'NAO_blocks_extract.txt').write_text("\n".join(nao_related), encoding='utf-8')

    # Parse composition from the whole log (not only extract) to maximize hit rate
    # Build s/p/d aggregation from NAO-MO matrix
    # 1) Matrix-based distribution (counts proxy of NAO types)
    matrix_acc = parse_nao_mo_matrix(raw_lines)
    if matrix_acc:
        agg = make_atom_summary_from_matrix(matrix_acc)
        per_atom_csv = out_dir / 'NAO_spd_by_atom_from_matrix.csv'
        with per_atom_csv.open('w', encoding='utf-8') as f:
            f.write('atom,index,entries,s_pct,p_pct,d_pct\n')
            for a in agg:
                f.write(f"{a['atom']},{a['index']},{a['entries']},{a['s_pct']},{a['p_pct']},{a['d_pct']}\n")
    else:
        print("Warning: NAO-MO matrix not found or unparsed.")

    # 2) Occupancy-based s/p/d distribution from Natural Electron Configuration
    occ_acc = parse_natural_electron_configuration(raw_lines)
    if occ_acc:
        occ_rows = make_atom_summary_from_occupancy(occ_acc)
        occ_csv = out_dir / 'NAO_spd_by_atom_occupancy.csv'
        with occ_csv.open('w', encoding='utf-8') as f:
            f.write('atom,index,s_e,p_e,d_e,s_pct,p_pct,d_pct\n')
            for r in occ_rows:
                f.write(f"{r['atom']},{r['index']},{r['s_e']},{r['p_e']},{r['d_e']},{r['s_pct']},{r['p_pct']},{r['d_pct']}\n")
        print(f"Done. Wrote: {per_atom_csv if matrix_acc else '(no matrix)'} and {occ_csv}. Also wrote NAO_blocks_extract.txt for inspection.")
    else:
        print("Warning: Natural Electron Configuration section not found.")

    # 3) Combined side-by-side table
    if matrix_acc and occ_acc:
        def pct_from_matrix(atom, idx):
            v = matrix_acc.get((atom, idx))
            if not v:
                return None
            t = v['s'] + v['p'] + v['d']
            if t <= 0:
                return None
            return {
                'entries': int(v['count']),
                's_pct_m': 100.0*v['s']/t,
                'p_pct_m': 100.0*v['p']/t,
                'd_pct_m': 100.0*v['d']/t,
            }
        combined_csv = out_dir / 'NAO_spd_by_atom_combined.csv'
        with combined_csv.open('w', encoding='utf-8') as f:
            f.write('atom,index,entries_m,s_pct_m,p_pct_m,d_pct_m,s_e,p_e,d_e,s_pct_o,p_pct_o,d_pct_o,delta_s,delta_p,delta_d\n')
            keys = set(matrix_acc.keys()) | set(occ_acc.keys())
            for atom, idx in sorted(keys, key=lambda k: (k[0]=='H', int(k[1]))):
                m = pct_from_matrix(atom, idx)
                o = occ_acc.get((atom, idx))
                if not (m and o):
                    continue
                total_o = o['s'] + o['p'] + o['d']
                s_pct_o = 100.0*o['s']/total_o if total_o>0 else 0.0
                p_pct_o = 100.0*o['p']/total_o if total_o>0 else 0.0
                d_pct_o = 100.0*o['d']/total_o if total_o>0 else 0.0
                delta_s = m['s_pct_m'] - s_pct_o
                delta_p = m['p_pct_m'] - p_pct_o
                delta_d = m['d_pct_m'] - d_pct_o
                f.write(
                    f"{atom},{idx},{m['entries']},{m['s_pct_m']:.2f},{m['p_pct_m']:.2f},{m['d_pct_m']:.2f},{o['s']:.3f},{o['p']:.3f},{o['d']:.3f},{s_pct_o:.2f},{p_pct_o:.2f},{d_pct_o:.2f},{delta_s:.2f},{delta_p:.2f},{delta_d:.2f}\n"
                )

        # Generate simple SVG charts for selected atoms (Fe 1, Cu 14)
        figures_dir = out_dir / 'figures'
        figures_dir.mkdir(parents=True, exist_ok=True)
        def render_spd_comparison_svg(atom: str, idx: str, m_vals, o_vals, filename: Path):
            # m_vals and o_vals: tuple/list of (s,p,d) percentages
            width, height = 640, 360
            padding = 40
            bar_width = 40
            gap = 60
            max_pct = 100.0
            def bar_x(i, which):
                # i: 0(S),1(P),2(D); which: 0 matrix, 1 occupancy
                base = padding + i*(bar_width*2 + gap)
                return base + which*bar_width
            def bar_h(pct):
                return int((height - 2*padding) * (pct/max_pct))
            def bar_y(pct):
                h = bar_h(pct)
                return height - padding - h
            colors_m = ['#4e79a7', '#4e79a7', '#4e79a7']
            colors_o = ['#f28e2b', '#f28e2b', '#f28e2b']
            labels = ['S', 'P', 'D']
            # Build SVG
            svg = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}'>"]
            svg.append(f"<rect x='0' y='0' width='{width}' height='{height}' fill='white' stroke='none'/>")
            # Axes
            svg.append(f"<line x1='{padding}' y1='{height-padding}' x2='{width-padding}' y2='{height-padding}' stroke='#333' stroke-width='2' />")
            svg.append(f"<line x1='{padding}' y1='{padding}' x2='{padding}' y2='{height-padding}' stroke='#333' stroke-width='2' />")
            # Bars
            for i in range(3):
                # Matrix bar
                x_m = bar_x(i, 0); y_m = bar_y(m_vals[i]); h_m = bar_h(m_vals[i])
                svg.append(f"<rect x='{x_m}' y='{y_m}' width='{bar_width}' height='{h_m}' fill='{colors_m[i]}'/>")
                # Occupancy bar
                x_o = bar_x(i, 1); y_o = bar_y(o_vals[i]); h_o = bar_h(o_vals[i])
                svg.append(f"<rect x='{x_o}' y='{y_o}' width='{bar_width}' height='{h_o}' fill='{colors_o[i]}'/>")
                # Labels
                cx = padding + i*(bar_width*2 + gap) + bar_width
                svg.append(f"<text x='{cx}' y='{height-padding+18}' text-anchor='middle' font-size='14' fill='#333'>{labels[i]}</text>")
            # Legend
            svg.append(f"<rect x='{width-200}' y='{padding}' width='18' height='18' fill='{colors_m[0]}'/>")
            svg.append(f"<text x='{width-175}' y='{padding+14}' font-size='14' fill='#333'>Matrix</text>")
            svg.append(f"<rect x='{width-200}' y='{padding+26}' width='18' height='18' fill='{colors_o[0]}'/>")
            svg.append(f"<text x='{width-175}' y='{padding+40}' font-size='14' fill='#333'>Occupancy</text>")
            # Title
            svg.append(f"<text x='{padding}' y='{padding-12}' font-size='16' fill='#000'>NAO s/p/d %: {atom} {idx}</text>")
            svg.append("</svg>")
            filename.write_text("\n".join(svg), encoding='utf-8')

        # Collect values for Fe 1 and Cu 14
        def get_vals(atom: str, idx: str):
            m = pct_from_matrix(atom, idx)
            o = occ_acc.get((atom, idx))
            if not (m and o):
                return None
            total_o = o['s'] + o['p'] + o['d']
            s_pct_o = 100.0*o['s']/total_o if total_o>0 else 0.0
            p_pct_o = 100.0*o['p']/total_o if total_o>0 else 0.0
            d_pct_o = 100.0*o['d']/total_o if total_o>0 else 0.0
            return ([m['s_pct_m'], m['p_pct_m'], m['d_pct_m']], [s_pct_o, p_pct_o, d_pct_o])

        fe_vals = get_vals('Fe', '1')
        cu_vals = get_vals('Cu', '14')
        nno_vals = get_vals('N', '12')
        ono_vals = get_vals('O', '13')
        if fe_vals:
            render_spd_comparison_svg('Fe', '1', fe_vals[0], fe_vals[1], figures_dir / 'Fe_1_spd.svg')
        if cu_vals:
            render_spd_comparison_svg('Cu', '14', cu_vals[0], cu_vals[1], figures_dir / 'Cu_14_spd.svg')
        if nno_vals:
            render_spd_comparison_svg('N', '12', nno_vals[0], nno_vals[1], figures_dir / 'N_12_spd.svg')
        if ono_vals:
            render_spd_comparison_svg('O', '13', ono_vals[0], ono_vals[1], figures_dir / 'O_13_spd.svg')

    # 4) Per-atom NAO label breakdown
    labels_acc = parse_nao_mo_labels(raw_lines)
    if labels_acc:
        labels_path = write_label_breakdown(out_dir, labels_acc)
        print(f"Done. Wrote combined and label breakdown: {combined_csv if matrix_acc and occ_acc else '(no combined)'}; {labels_path}.")
    else:
        print("Warning: NAO label breakdown not found.")


if __name__ == '__main__':
    main()
