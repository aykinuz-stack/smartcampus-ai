"""SmartCampusAI — 10+ tab'li st.tabs() bloklarini otomatik gruplara ayirir.

Her 10+ tab'li st.tabs() blogunu:
1. radio ile ust seviye grup secimi
2. Secili grubun alt tablari
3. Secilmemis tablara if-guard (None check)

Yedekleme: her dosyanin .bak kopyasini olusturur.
"""
import re
import os
import math
import shutil

VIEWS_DIR = "views"
MIN_TABS = 12  # Bu sayidan fazla tab'i grupla
MAX_GROUP_SIZE = 7  # Her grupta max tab

# Emoji listesi — gruplara atanacak
GROUP_EMOJIS = ["📋", "📊", "🔧", "📈", "🎯", "⚡", "🏆", "🔍", "📌", "🗂️"]
GROUP_NAMES = ["Grup A", "Grup B", "Grup C", "Grup D", "Grup E", "Grup F", "Grup G", "Grup H", "Grup I", "Grup J"]


def find_tabs_blocks(content):
    """st.tabs([...]) bloklarini bul. 10+ tab olanlari dondur."""
    blocks = []

    # Pattern: var1, var2, ... = st.tabs(["label1", "label2", ...])
    pattern = r'([ \t]*)([\w, ]+)\s*=\s*st\.tabs\(\[([^\]]+)\]\)'

    for m in re.finditer(pattern, content, re.DOTALL):
        indent = m.group(1)
        vars_str = m.group(2).strip()
        labels_str = m.group(3)

        # Tab isimlerini parse et
        labels = []
        for line in labels_str.split('\n'):
            line = line.strip().rstrip(',')
            if line.startswith('"') or line.startswith("'"):
                labels.append(line.strip('"').strip("'"))

        if len(labels) == 0:
            # Tek satirda olabilir
            labels = [l.strip().strip('"').strip("'") for l in labels_str.split(',') if l.strip()]

        # Variable isimlerini parse et
        var_names = [v.strip() for v in vars_str.split(',') if v.strip()]

        if len(labels) >= MIN_TABS and len(var_names) == len(labels):
            blocks.append({
                'match': m,
                'indent': indent,
                'vars': var_names,
                'labels': labels,
                'start': m.start(),
                'end': m.end(),
                'full_text': m.group(0),
            })

    return blocks


def group_tabs(labels, max_size=MAX_GROUP_SIZE):
    """Tab'lari gruplara bol."""
    n = len(labels)
    num_groups = math.ceil(n / max_size)
    groups = []

    for i in range(num_groups):
        start = i * max_size
        end = min(start + max_size, n)
        emoji = GROUP_EMOJIS[i % len(GROUP_EMOJIS)]
        name = f"{emoji} {GROUP_NAMES[i]}" if i < len(GROUP_NAMES) else f"{emoji} Grup {i+1}"
        groups.append({
            'name': name,
            'start_idx': start,
            'end_idx': end,
            'count': end - start,
        })

    return groups


def generate_replacement(block, func_prefix=""):
    """Gruplama kodu uret."""
    indent = block['indent']
    labels = block['labels']
    var_names = block['vars']

    groups = group_tabs(labels)

    lines = []
    lines.append(f"{indent}# -- Tab Gruplama ({len(labels)} tab -> {len(groups)} grup) --")

    # Grup tanimlari
    lines.append(f"{indent}_GRP_TABS = {{")
    for g in groups:
        items = []
        for idx in range(g['start_idx'], g['end_idx']):
            items.append(f'("{labels[idx]}", {idx})')
        items_str = ", ".join(items)
        lines.append(f'{indent}    "{g["name"]}": [{items_str}],')
    lines.append(f"{indent}}}")

    # Radio secimi
    uid = f"_grp_{abs(hash(tuple(var_names)))%99999}"
    lines.append(f'{indent}_sg{uid} = st.radio("", list(_GRP_TABS.keys()), horizontal=True, label_visibility="collapsed", key="rg{uid}")')
    lines.append(f'{indent}_gt{uid} = _GRP_TABS[_sg{uid}]')
    lines.append(f'{indent}_tn{uid} = [t[0] for t in _gt{uid}]')
    lines.append(f'{indent}_ti{uid} = [t[1] for t in _gt{uid}]')
    lines.append(f'{indent}_tabs{uid} = st.tabs(_tn{uid})')

    # Variable mapping
    lines.append(f'{indent}_tmap{uid} = {{i: t for i, t in zip(_ti{uid}, _tabs{uid})}}')

    for idx, var in enumerate(var_names):
        lines.append(f'{indent}{var} = _tmap{uid}.get({idx})')

    return "\n".join(lines)


def add_if_guards(content, var_names):
    """'with varN:' -> 'if varN is not None: \\n  with varN:' """
    for var in var_names:
        # Pattern: indent + with var:
        pattern = re.compile(r'^([ \t]+)(with ' + re.escape(var) + r':)', re.MULTILINE)

        def replacer(m):
            ind = m.group(1)
            with_stmt = m.group(2)
            return f"{ind}if {var} is not None:\n{ind}  {with_stmt}"

        content = pattern.sub(replacer, content, count=1)  # Sadece ilk occurrence

    return content


def process_file(filepath):
    """Tek dosyayi isle."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = find_tabs_blocks(content)
    if not blocks:
        return 0

    # Yedekle
    shutil.copy2(filepath, filepath + '.bak')

    # Sondan basa isle (index kaymamasi icin)
    blocks.sort(key=lambda b: b['start'], reverse=True)

    modified = 0
    for block in blocks:
        replacement = generate_replacement(block)
        content = content[:block['start']] + replacement + content[block['end']:]
        content = add_if_guards(content, block['vars'])
        modified += 1

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return modified


def main():
    total = 0
    files_modified = []

    for f in sorted(os.listdir(VIEWS_DIR)):
        if not f.endswith('.py') or f.startswith('__'):
            continue
        # kayit_modulu zaten yapildi
        if f == 'kayit_modulu.py':
            continue

        path = os.path.join(VIEWS_DIR, f)
        count = process_file(path)
        if count > 0:
            files_modified.append((f, count))
            total += count
            print(f"  {count} blok | {f}")

    print(f"\nToplam: {total} blok, {len(files_modified)} dosya islendi")

    # Syntax check
    print("\nSyntax kontrol...")
    import py_compile
    errors = 0
    for f, _ in files_modified:
        path = os.path.join(VIEWS_DIR, f)
        try:
            py_compile.compile(path, doraise=True)
        except py_compile.PyCompileError as e:
            print(f"  HATA: {f} — {e}")
            errors += 1
            # Restore from backup
            shutil.copy2(path + '.bak', path)
            print(f"  GERI ALINDI: {f}")

    if errors == 0:
        print("  Tum dosyalar SYNTAX OK!")
        # Backup dosyalarini sil
        for f, _ in files_modified:
            bak = os.path.join(VIEWS_DIR, f + '.bak')
            if os.path.exists(bak):
                os.remove(bak)
    else:
        print(f"\n{errors} dosyada hata — backup'lardan geri alindi")


if __name__ == "__main__":
    main()
