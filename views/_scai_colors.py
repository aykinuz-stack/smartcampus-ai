"""
SmartCampusAI — Merkezi Renk Sabitleri
==========================================
Tüm modüllerin kullanması gereken canonical renk sabitleri.
Hardcoded hex yerine SCAI.PRIMARY, SCAI.DANGER vb. kullan.

Örnek:
    from views._scai_colors import SCAI
    renk = SCAI.PRIMARY  # #4F46E5
    styled_stat_row([("Öğrenci", "847", SCAI.PRIMARY, "🎓"), ...])
"""
from __future__ import annotations


class SCAI:
    """SmartCampusAI canonical renk paleti — 600-shade tabanlı."""

    # ── PRIMARY BRAND ──
    PRIMARY       = "#4F46E5"   # indigo.600 — ana brand
    PRIMARY_SOFT  = "#A5B4FC"   # indigo.300
    PRIMARY_DARK  = "#4338CA"   # indigo.700

    # ── SEMANTIK DURUMLAR (hep 600) ──
    SUCCESS       = "#059669"   # emerald.600
    SUCCESS_SOFT  = "#6EE7B7"   # emerald.300
    WARNING       = "#D97706"   # amber.600
    WARNING_SOFT  = "#FCD34D"   # amber.300
    DANGER        = "#DC2626"   # red.600
    DANGER_SOFT   = "#FCA5A5"   # red.300
    DANGER_STRONG = "#991B1B"   # red.800 — kritik
    INFO          = "#0284C7"   # sky.600
    INFO_SOFT     = "#7DD3FC"   # sky.300

    # ── KATEGORI RENKLERI ──
    ACADEMIC      = "#2563EB"   # blue.600 — akademik
    GUIDANCE      = "#7C3AED"   # violet.600 — rehberlik/AI
    HEALTH        = "#059669"   # emerald.600 — sağlık
    SAFETY        = "#DC2626"   # red.600 — güvenlik
    COMMUNITY     = "#DB2777"   # pink.600 — topluluk
    SUPPORT       = "#EA580C"   # orange.600 — destek
    FINANCE       = "#D97706"   # amber.600 — finans
    OPERATIONS    = "#52525B"   # zinc.600 — operasyon

    # ── EK RENKLER ──
    TEAL          = "#0D9488"   # teal.600
    CYAN          = "#0891B2"   # cyan.600
    PURPLE        = "#9333EA"   # purple.600
    PINK          = "#DB2777"   # pink.600
    ROSE          = "#EC4899"   # pink.500 — daha soft

    # ── YÜZEY (Zinc tabanlı) ──
    BG_DARKEST    = "#09090B"   # zinc.950
    BG_DARK       = "#18181B"   # zinc.900 — kart
    BG_ELEVATED   = "#27272A"   # zinc.800
    BG_BORDER     = "#3F3F46"   # zinc.700

    # ── METİN (WCAG AAA) ──
    TEXT_PRIMARY     = "#FAFAFA"   # zinc.50 — Lc -107 ✅ A+
    TEXT_SECONDARY   = "#E4E4E7"   # zinc.200
    TEXT_MUTED       = "#A1A1AA"   # zinc.400
    TEXT_DISABLED    = "#52525B"   # zinc.600

    # ── NÖTR GRILER ──
    SLATE_500     = "#64748B"
    SLATE_400     = "#94A3B8"
    SLATE_700     = "#334155"


# Yardımcı kısayol — en çok kullanılan 5 renk
PRIMARY = SCAI.PRIMARY
SUCCESS = SCAI.SUCCESS
WARNING = SCAI.WARNING
DANGER = SCAI.DANGER
INFO = SCAI.INFO


# ── HELPER: Renk adına göre canonical al ──
def get_canonical(role: str) -> str:
    """Semantic role ismine göre canonical renk döndür.

    Örnek: get_canonical("success") → "#059669"
    """
    roles = {
        "primary": SCAI.PRIMARY,
        "success": SCAI.SUCCESS,
        "warning": SCAI.WARNING,
        "danger": SCAI.DANGER,
        "info": SCAI.INFO,
        "academic": SCAI.ACADEMIC,
        "guidance": SCAI.GUIDANCE,
        "health": SCAI.HEALTH,
        "safety": SCAI.SAFETY,
        "community": SCAI.COMMUNITY,
        "support": SCAI.SUPPORT,
        "finance": SCAI.FINANCE,
        "operations": SCAI.OPERATIONS,
    }
    return roles.get(role.lower(), SCAI.PRIMARY)
