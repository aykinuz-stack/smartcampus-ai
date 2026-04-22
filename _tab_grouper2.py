"""tabs[N] formatindaki 10+ tab bloklarini gruplara ayirir.

Pattern: tabs = st.tabs(["a", "b", ...])  -> with tabs[0]: ...
"""
import re
import os
import math
import shutil
import py_compile

VIEWS_DIR = "views"
MIN_TABS = 12
MAX_GROUP_SIZE = 7

GROUP_EMOJIS = ["📋", "📊", "🔧", "📈", "🎯", "⚡", "🏆", "🔍", "📌", "🗂️"]
GROUP_NAMES = ["Grup A", "Grup B", "Grup C", "Grup D", "Grup E", "Grup F", "Grup G", "Grup H"]


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # tabs = st.tabs(["...", "...", ...]) formatini bul
    pattern = r'([ \t]*)(tabs)\s*=\s*st\.tabs\(\[([^\]]+)\]\)'

    blocks = list(re.finditer(pattern, content, re.DOTALL))
    if not blocks:
        return 0

    modified = 0

    for block in reversed(blocks):
        indent = block.group(1)
        var_name = block.group(2)  # "tabs"
        labels_str = block.group(3)

        # Label'lari parse et
        labels = []
        for line in labels_str.split('\n'):
            line = line.strip().rstrip(',')
            if line.startswith('"') or line.startswith("'"):
                labels.append(line.strip('"').strip("'"))
        if len(labels) == 0:
            labels = [l.strip().strip('"').strip("'") for l in labels_str.split(',') if l.strip()]

        if len(labels) < MIN_TABS:
            continue

        # Gruplara bol
        num_groups = math.ceil(len(labels) / MAX_GROUP_SIZE)
        groups = []
        for i in range(num_groups):
            s = i * MAX_GROUP_SIZE
            e = min(s + MAX_GROUP_SIZE, len(labels))
            emoji = GROUP_EMOJIS[i % len(GROUP_EMOJIS)]
            gname = f"{emoji} {GROUP_NAMES[i]}" if i < len(GROUP_NAMES) else f"{emoji} Grup {i+1}"
            groups.append((gname, s, e))

        # Replacement kod uret
        uid = f"_{abs(hash(filepath + str(block.start())))%99999}"
        lines = []
        lines.append(f"{indent}# -- Tab Gruplama ({len(labels)} tab -> {num_groups} grup) --")
        lines.append(f"{indent}_GRP{uid} = {{")
        for gname, s, e in groups:
            items = ", ".join(f'("{labels[idx]}", {idx})' for idx in range(s, e))
            lines.append(f'{indent}    "{gname}": [{items}],')
        lines.append(f"{indent}}}")
        lines.append(f'{indent}_sg{uid} = st.radio("", list(_GRP{uid}.keys()), horizontal=True, label_visibility="collapsed", key="rg{uid}")')
        lines.append(f'{indent}_gt{uid} = _GRP{uid}[_sg{uid}]')
        lines.append(f'{indent}_aktif_idx{uid} = set(t[1] for t in _gt{uid})')
        lines.append(f'{indent}_tab_names{uid} = [t[0] for t in _gt{uid}]')
        lines.append(f'{indent}tabs = st.tabs(_tab_names{uid})')
        lines.append(f'{indent}_tab_real{uid} = {{idx: t for idx, t in zip((t[1] for t in _gt{uid}), tabs)}}')

        replacement = "\n".join(lines)
        content = content[:block.start()] + replacement + content[block.end():]

        # with tabs[N]: -> if N in _aktif_idx: \n  with _tab_real.get(N, tabs[0]):
        for idx in range(len(labels) - 1, -1, -1):
            old_pattern = re.compile(
                r'^([ \t]+)(with tabs\[' + str(idx) + r'\]:)',
                re.MULTILINE
            )
            def make_replacer(i, u):
                def replacer(m):
                    ind = m.group(1)
                    return f"{ind}if {i} in _aktif_idx{u}:\n{ind}  with _tab_real{u}[{i}]:"
                return replacer
            content = old_pattern.sub(make_replacer(idx, uid), content, count=1)

        modified += 1

    # Kaydet
    shutil.copy2(filepath, filepath + '.bak2')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # Syntax check
    try:
        py_compile.compile(filepath, doraise=True)
        os.remove(filepath + '.bak2')
        return modified
    except py_compile.PyCompileError as e:
        print(f"  SYNTAX HATA: {os.path.basename(filepath)} — geri aliniyor")
        shutil.copy2(filepath + '.bak2', filepath)
        os.remove(filepath + '.bak2')
        return 0


def main():
    targets = [
        "erken_uyari.py", "rehberlik.py", "insan_kaynaklari.py",
        "bilisim_vadisi.py", "destek_hizmetleri.py",
        "matematik_dunyasi.py", "sosyal_etkinlik.py",
        "toplanti_kurullar.py", "sivil_savunma_isg.py",
        "stem_merkezi.py", "ogrenci_veli_panel.py",
    ]

    total = 0
    for f in targets:
        path = os.path.join(VIEWS_DIR, f)
        if not os.path.exists(path):
            continue
        count = process_file(path)
        if count > 0:
            print(f"  {count} blok | {f}")
            total += count
        else:
            print(f"  - atla  | {f}")

    print(f"\nToplam: {total} blok islendi")


if __name__ == "__main__":
    main()
