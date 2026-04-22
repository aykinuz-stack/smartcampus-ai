"""Ogrenci odakli endpoint'ler — notlar, devamsizlik, odev."""
from __future__ import annotations

import uuid
from collections import defaultdict
from datetime import date, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from ..core.data_adapter import DataAdapter, DataPaths
from ..core.deps import get_current_user, get_data_adapter
from ..schemas.ogrenci import (
    AttendanceItem,
    AttendanceResponse,
    GradeItem,
    GradeSummary,
    GradesResponse,
    OdevItem,
    OdevListResponse,
    OdevTeslimRequest,
)


router = APIRouter(prefix="/ogrenci", tags=["Ogrenci"])


def _target_student_id(user: dict, query_sid: str | None = None) -> str:
    """Hangi ogrencinin verisi? Veli ise cocuk ID, ogrenci ise kendi ID."""
    role = user.get("role", "").lower()
    if role == "ogrenci":
        return user.get("student_id") or user.get("user_id")
    if role == "veli":
        children = user.get("children_ids", [])
        if query_sid and query_sid in children:
            return query_sid
        return children[0] if children else ""
    # Yetkili (rehber/mudur/ogretmen) her ogrenciye bakabilir
    if query_sid:
        return query_sid
    raise HTTPException(400, "student_id gerekli")


# ══════════════════════════════════════════════════════════════
# NOTLAR
# ══════════════════════════════════════════════════════════════

@router.get("/notlar", response_model=GradesResponse)
async def get_notlar(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    student_id: str | None = None,
    donem: str | None = None,   # "1. Donem" / "2. Donem" / None=hepsi
):
    """Ogrenci notlari — ders, donem, not turu bazli."""
    sid = _target_student_id(user, student_id)
    all_grades = adapter.load(DataPaths.GRADES) or []

    mine = [g for g in all_grades if g.get("student_id") == sid]
    if donem:
        mine = [g for g in mine if g.get("donem") == donem]

    # Tarih DESC siralama
    mine.sort(key=lambda g: g.get("tarih", ""), reverse=True)

    notlar = [
        GradeItem(
            id=g.get("id", ""),
            ders=g.get("ders", ""),
            donem=g.get("donem", ""),
            not_turu=g.get("not_turu", ""),
            not_sirasi=int(g.get("not_sirasi", 0) or 0),
            puan=float(g.get("puan", 0) or 0),
            tarih=g.get("tarih", ""),
            aciklama=g.get("aciklama", ""),
        )
        for g in mine
    ]

    # Ders bazli ortalama
    ders_puanlari: dict[str, list[float]] = defaultdict(list)
    for n in notlar:
        ders_puanlari[n.ders].append(n.puan)

    ders_ozetleri = [
        GradeSummary(
            ders=ders,
            ortalama=round(sum(p) / len(p), 1),
            not_sayisi=len(p),
            en_yuksek=max(p),
            en_dusuk=min(p),
        )
        for ders, p in sorted(ders_puanlari.items())
    ]

    # Genel ortalama
    tum_puanlar = [n.puan for n in notlar]
    genel = round(sum(tum_puanlar) / len(tum_puanlar), 1) if tum_puanlar else 0.0

    # Donem ortalaması (mevcut donem)
    if donem:
        donem_ort = genel
    else:
        now = datetime.now()
        curr_donem = "1. Donem" if now.month >= 9 or now.month <= 1 else "2. Donem"
        donem_puanlari = [n.puan for n in notlar if n.donem == curr_donem]
        donem_ort = round(sum(donem_puanlari) / len(donem_puanlari), 1) \
            if donem_puanlari else 0.0

    return GradesResponse(
        notlar=notlar,
        donem_ortalamasi=donem_ort,
        genel_ortalama=genel,
        ders_ozetleri=ders_ozetleri,
    )


# ══════════════════════════════════════════════════════════════
# DEVAMSIZLIK
# ══════════════════════════════════════════════════════════════

@router.get("/devamsizlik", response_model=AttendanceResponse)
async def get_devamsizlik(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    student_id: str | None = None,
):
    """Ogrenci devamsizlik kayitlari ve ozet."""
    sid = _target_student_id(user, student_id)
    all_att = adapter.load(DataPaths.ATTENDANCE) or []
    mine = [a for a in all_att if a.get("student_id") == sid]
    mine.sort(key=lambda a: a.get("tarih", ""), reverse=True)

    kayitlar = [
        AttendanceItem(
            id=a.get("id", ""),
            tarih=a.get("tarih", ""),
            ders=a.get("ders", ""),
            ders_saati=int(a.get("ders_saati", 0) or 0),
            turu=a.get("turu", ""),
            aciklama=a.get("aciklama", ""),
        )
        for a in mine
    ]

    ozursuz = sum(1 for k in kayitlar if k.turu.lower() in ("devamsiz", "ozursuz"))
    ozurlu = sum(1 for k in kayitlar if k.turu.lower() in ("izinli", "raporlu", "ozurlu"))
    gec = sum(1 for k in kayitlar if k.turu.lower() == "gec")

    # Son 30 gun
    cutoff = (date.today() - timedelta(days=30)).isoformat()
    son_30 = sum(1 for k in kayitlar if k.tarih >= cutoff and k.turu.lower() in ("devamsiz", "ozursuz"))

    total = len(kayitlar)
    oran = round(ozursuz / max(total, 1) * 100, 1)

    return AttendanceResponse(
        kayitlar=kayitlar,
        toplam_ders_saati=ozursuz,
        ozursuz=ozursuz,
        ozurlu=ozurlu,
        gec=gec,
        oran=oran,
        son_30_gun=son_30,
    )


# ══════════════════════════════════════════════════════════════
# ODEVLER
# ══════════════════════════════════════════════════════════════

@router.get("/odevler", response_model=OdevListResponse)
async def get_odevler(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    student_id: str | None = None,
):
    """Ogrencinin odev listesi — bekleyen/geciken/teslim edilen."""
    sid = _target_student_id(user, student_id)

    # Ogrencinin sinif/sube bilgisi
    students = adapter.load(DataPaths.STUDENTS) or []
    student = next((s for s in students if s.get("id") == sid), None)
    sinif, sube = (student.get("sinif", ""), student.get("sube", "")) if student else ("", "")

    all_odev = adapter.load(DataPaths.HOMEWORK) or []
    # Ogrencinin sinif/subesi icin verilen odevler
    mine_odev = [
        o for o in all_odev
        if str(o.get("sinif", "")) == str(sinif) and o.get("sube", "") == sube
    ]

    # Teslim kayitlarinda bu ogrenciye ait olanlar
    all_teslim = adapter.load(DataPaths.HOMEWORK_SUBMISSIONS) or []
    mine_teslim = {t.get("odev_id"): t for t in all_teslim
                  if t.get("student_id") == sid}

    today = date.today().isoformat()
    bekleyen, geciken, teslim_edilen = [], [], []

    for o in mine_odev:
        teslim = mine_teslim.get(o.get("id"))
        teslim_tarihi = o.get("teslim_tarihi", "")
        durum = o.get("durum", "")

        item = OdevItem(
            id=o.get("id", ""),
            baslik=o.get("baslik", ""),
            ders=o.get("ders", ""),
            ogretmen_adi=o.get("ogretmen_adi", ""),
            tur=o.get("tur", ""),
            aciklama=o.get("aciklama", ""),
            verilis_tarihi=o.get("verilis_tarihi", ""),
            teslim_tarihi=teslim_tarihi,
            durum=durum,
            teslim_edildi=teslim is not None,
            teslim_tarih=teslim.get("teslim_tarihi") if teslim else None,
            puan=teslim.get("puan") if teslim else None,
            gec_teslim=teslim.get("gec_teslim", False) if teslim else False,
        )

        if teslim:
            teslim_edilen.append(item)
        elif teslim_tarihi and teslim_tarihi < today:
            geciken.append(item)
        else:
            bekleyen.append(item)

    # Bekleyenler: en yakın teslim tarihi önce
    bekleyen.sort(key=lambda o: o.teslim_tarihi or "9999")
    geciken.sort(key=lambda o: o.teslim_tarihi or "9999", reverse=True)
    teslim_edilen.sort(key=lambda o: o.teslim_tarih or "", reverse=True)

    return OdevListResponse(
        bekleyen=bekleyen,
        geciken=geciken,
        teslim_edilen=teslim_edilen,
        toplam=len(mine_odev),
    )


@router.post("/odev/teslim")
async def teslim_et(
    req: OdevTeslimRequest,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Odev teslim kaydi. Sadece ogrenci kendi odevini teslim edebilir."""
    role = user.get("role", "").lower()
    if role != "ogrenci":
        raise HTTPException(403, "Sadece ogrenci teslim edebilir")

    sid = user.get("student_id") or user.get("user_id")
    if not sid:
        raise HTTPException(400, "student_id yok")

    # Ödev var mı
    odevler = adapter.load(DataPaths.HOMEWORK) or []
    odev = next((o for o in odevler if o.get("id") == req.odev_id), None)
    if not odev:
        raise HTTPException(404, "Odev bulunamadi")

    # Zaten teslim mi
    teslimler = adapter.load(DataPaths.HOMEWORK_SUBMISSIONS) or []
    existing = next((t for t in teslimler
                    if t.get("odev_id") == req.odev_id and t.get("student_id") == sid),
                   None)

    today = date.today().isoformat()
    teslim_tarihi = odev.get("teslim_tarihi", "")
    gec = today > teslim_tarihi if teslim_tarihi else False

    if existing:
        # Guncelle
        existing["teslim_tarihi"] = today
        existing["durum"] = "teslim_edildi"
        existing["gec_teslim"] = gec
        if req.dosya_url:
            existing["dosya_url"] = req.dosya_url
        if req.not_:
            existing["not"] = req.not_
        adapter.save(DataPaths.HOMEWORK_SUBMISSIONS, teslimler)
        return {"id": existing["id"], "updated": True}

    # Yeni teslim
    yeni = {
        "id": f"ot_{uuid.uuid4().hex[:8]}",
        "odev_id": req.odev_id,
        "student_id": sid,
        "teslim_tarihi": today,
        "puan": None,
        "durum": "teslim_edildi",
        "gec_teslim": gec,
        "dosya_url": req.dosya_url or "",
        "not": req.not_,
    }
    adapter.append(DataPaths.HOMEWORK_SUBMISSIONS, yeni)
    return {"id": yeni["id"], "created": True}


# ══════════════════════════════════════════════════════════════
# YAKLASAN SINAVLAR
# ══════════════════════════════════════════════════════════════

@router.get("/yaklasan-sinavlar")
async def get_yaklasan_sinavlar(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    student_id: str | None = None,
):
    """Öğrencinin sınıfı için yaklaşan sınav/yazılı takvimi."""
    sid = _target_student_id(user, student_id)
    students = adapter.load(DataPaths.STUDENTS) or []
    student = next((s for s in students if s.get("id") == sid), None)
    sinif = int(student.get("sinif", 0)) if student else 0

    today = date.today().isoformat()

    # 1) olcme_takvim.json
    takvim = adapter.load(DataPaths.OLCME_TAKVIM) or []
    yaklasan = [
        t for t in takvim
        if t.get("tarih", "") >= today
        and (not sinif or int(t.get("sinif", 0)) == sinif)
    ]

    # 2) olcme/exams.json (status=scheduled)
    exams = adapter.load(DataPaths.EXAMS) or []
    for e in exams:
        if e.get("status") in ("scheduled", "active"):
            e_sinif = int(e.get("sinif", 0))
            e_tarih = e.get("exam_date") or e.get("created_at", "")
            if e_tarih >= today and (not sinif or e_sinif == sinif):
                yaklasan.append({
                    "id": e.get("id"),
                    "ders": e.get("ders", ""),
                    "sinif": e_sinif,
                    "tarih": e_tarih,
                    "tur": e.get("type", "yazili"),
                    "baslik": e.get("name", ""),
                    "sure_dk": e.get("duration_minutes", 40),
                })

    yaklasan.sort(key=lambda x: x.get("tarih", ""))
    return {"sinavlar": yaklasan[:20]}


# ══════════════════════════════════════════════════════════════
# DASHBOARD (tek cagri ile tum KPI)
# ══════════════════════════════════════════════════════════════

@router.get("/dashboard")
async def get_dashboard(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    student_id: str | None = None,
):
    """Tek çağrıda tüm home KPI'ları — ağ trafiğini azaltır."""
    sid = _target_student_id(user, student_id)
    students = adapter.load(DataPaths.STUDENTS) or []
    student = next((s for s in students if s.get("id") == sid), None)
    sinif = int(student.get("sinif", 0)) if student else 0
    sube = student.get("sube", "") if student else ""

    today = date.today().isoformat()

    # Notlar
    all_grades = adapter.load(DataPaths.GRADES) or []
    my_grades = [g for g in all_grades if g.get("student_id") == sid]
    my_grades.sort(key=lambda g: g.get("tarih", ""), reverse=True)
    puanlar = [float(g.get("puan", 0) or 0) for g in my_grades]
    genel_ort = round(sum(puanlar) / len(puanlar), 1) if puanlar else 0.0

    # Devamsızlık
    all_att = adapter.load(DataPaths.ATTENDANCE) or []
    my_att = [a for a in all_att if a.get("student_id") == sid]
    ozursuz = sum(1 for a in my_att if a.get("turu", "").lower() in ("devamsiz", "ozursuz"))

    # Ödevler
    all_odev = adapter.load(DataPaths.HOMEWORK) or []
    my_odev = [o for o in all_odev
               if str(o.get("sinif", "")) == str(sinif) and o.get("sube", "") == sube]
    all_teslim = adapter.load(DataPaths.HOMEWORK_SUBMISSIONS) or []
    teslim_ids = {t.get("odev_id") for t in all_teslim if t.get("student_id") == sid}

    bekleyen_odevler = []
    for o in my_odev:
        if o.get("id") not in teslim_ids:
            bekleyen_odevler.append({
                "id": o.get("id"),
                "baslik": o.get("baslik", ""),
                "ders": o.get("ders", ""),
                "teslim_tarihi": o.get("teslim_tarihi", ""),
            })
    bekleyen_odevler.sort(key=lambda x: x.get("teslim_tarihi", "9999"))

    # Yaklaşan sınavlar
    takvim = adapter.load(DataPaths.OLCME_TAKVIM) or []
    yaklasan_sinav = [
        t for t in takvim
        if t.get("tarih", "") >= today
        and (not sinif or int(t.get("sinif", 0)) == sinif)
    ]
    yaklasan_sinav.sort(key=lambda x: x.get("tarih", ""))

    # Bugünkü ders programı
    from calendar import day_name
    gun_map = {0: "Pazartesi", 1: "Sali", 2: "Carsamba", 3: "Persembe", 4: "Cuma"}
    bugun_gun = gun_map.get(date.today().weekday(), "")
    schedule = adapter.load(DataPaths.SCHEDULE) or []
    bugun_ders = [
        s for s in schedule
        if s.get("gun", "") == bugun_gun
        and str(s.get("sinif", "")) == str(sinif)
        and s.get("sube", "") == sube
    ]
    bugun_ders.sort(key=lambda x: int(x.get("saat", 0)))

    return {
        "genel_ortalama": genel_ort,
        "son_notlar": [
            {"ders": g.get("ders"), "puan": float(g.get("puan", 0) or 0),
             "not_turu": g.get("not_turu"), "tarih": g.get("tarih")}
            for g in my_grades[:10]
        ],
        "devamsizlik_ozursuz": ozursuz,
        "bekleyen_odev_sayisi": len(bekleyen_odevler),
        "bekleyen_odevler": bekleyen_odevler[:5],
        "yaklasan_sinavlar": yaklasan_sinav[:5],
        "bugun_ders_sayisi": len(bugun_ders),
        "bugun_dersler": [
            {"saat": s.get("saat"), "ders": s.get("ders"),
             "ogretmen": s.get("ogretmen", "")}
            for s in bugun_ders
        ],
    }


# ══════════════════════════════════════════════════════════════
# SINAV SONUCLARI
# ══════════════════════════════════════════════════════════════

@router.get("/sinav-sonuclari")
async def get_sinav_sonuclari(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    student_id: str | None = None,
):
    """Ogrencinin sinav sonuclari — olcme modulu verisiyle."""
    sid = _target_student_id(user, student_id)

    # Olcme sessions + results
    sessions = adapter.load("olcme/sessions.json") or []
    results = adapter.load("olcme/results.json") or []
    exams = adapter.load(DataPaths.EXAMS) or []

    my_sessions = [s for s in sessions if s.get("student_id") == sid]
    result_map = {r.get("session_id"): r for r in results}
    exam_map = {e.get("id"): e for e in exams}

    sonuclar = []
    for sess in my_sessions:
        result = result_map.get(sess.get("id"))
        exam = exam_map.get(sess.get("exam_id"))
        if not result or not exam:
            continue
        sonuclar.append({
            "sinav_adi": exam.get("name", ""),
            "ders": exam.get("ders", ""),
            "sinif": exam.get("sinif"),
            "tarih": sess.get("started_at", ""),
            "puan": result.get("score", 0),
            "dogru": result.get("correct_count", 0),
            "yanlis": result.get("wrong_count", 0),
            "bos": result.get("empty_count", 0),
            "toplam_soru": result.get("total_questions", 0),
            "sure_dk": result.get("duration_minutes", 0),
        })

    # Grades tablosundaki yazili sonuclari da ekle
    all_grades = adapter.load(DataPaths.GRADES) or []
    my_grades = [g for g in all_grades if g.get("student_id") == sid]
    for g in my_grades:
        if g.get("not_turu", "").lower() in ("yazili", "sinav", "deneme"):
            sonuclar.append({
                "sinav_adi": f"{g.get('ders', '')} {g.get('not_turu', '')}",
                "ders": g.get("ders", ""),
                "sinif": None,
                "tarih": g.get("tarih", ""),
                "puan": float(g.get("puan", 0) or 0),
                "dogru": None,
                "yanlis": None,
                "bos": None,
                "toplam_soru": None,
                "sure_dk": None,
            })

    sonuclar.sort(key=lambda x: x.get("tarih", ""), reverse=True)

    # Ders bazli ortalamalar
    ders_map: dict[str, list[float]] = defaultdict(list)
    for s in sonuclar:
        if s.get("puan") is not None:
            ders_map[s["ders"]].append(float(s["puan"]))
    ders_ort = {d: round(sum(p) / len(p), 1) for d, p in ders_map.items()}

    return {
        "sonuclar": sonuclar[:30],
        "toplam": len(sonuclar),
        "ders_ortalamalari": ders_ort,
    }


# ══════════════════════════════════════════════════════════════
# KAZANIM BORCLARI
# ══════════════════════════════════════════════════════════════

@router.get("/kazanim-borclari")
async def get_kazanim_borclari(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    student_id: str | None = None,
):
    """Ogrencinin eksik kazanimlari — dusuk puanli sinavlardan."""
    sid = _target_student_id(user, student_id)

    all_grades = adapter.load(DataPaths.GRADES) or []
    my_grades = [g for g in all_grades if g.get("student_id") == sid]

    # Telafi tasklari
    telafi = adapter.load("olcme/telafi_tasks.json") or []
    my_telafi = [t for t in telafi if t.get("student_id") == sid]

    # Kazanim borclari: puan < 70 olan dersler
    borclar = []
    ders_set = set()
    for g in my_grades:
        puan = float(g.get("puan", 0) or 0)
        if puan < 70:
            ders = g.get("ders", "")
            if ders not in ders_set:
                ders_set.add(ders)
                borclar.append({
                    "ders": ders,
                    "puan": puan,
                    "not_turu": g.get("not_turu", ""),
                    "tarih": g.get("tarih", ""),
                    "renk": "RED" if puan < 50 else "YELLOW",
                    "telafi_var": any(
                        t.get("ders") == ders for t in my_telafi
                    ),
                })

    borclar.sort(key=lambda x: x.get("puan", 0))

    return {
        "borclar": borclar,
        "toplam": len(borclar),
        "kritik": sum(1 for b in borclar if b["renk"] == "RED"),
        "uyari": sum(1 for b in borclar if b["renk"] == "YELLOW"),
    }


# ══════════════════════════════════════════════════════════════
# OGRENCI FOTOSU
# ══════════════════════════════════════════════════════════════

@router.get("/foto/{student_id}")
async def get_foto(
    student_id: str,
    user: Annotated[dict, Depends(get_current_user)],
):
    """Ogrenci fotosu — base64 veya placeholder."""
    import base64
    from pathlib import Path

    _PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
    foto_dir = _PROJECT_ROOT / "data" / "ogrenci_foto"

    # jpg, png, jpeg arasin
    for ext in ("jpg", "jpeg", "png"):
        foto_path = foto_dir / f"{student_id}.{ext}"
        if foto_path.exists():
            try:
                with open(foto_path, "rb") as f:
                    data = base64.b64encode(f.read()).decode("utf-8")
                mime = "image/jpeg" if ext in ("jpg", "jpeg") else "image/png"
                return {
                    "student_id": student_id,
                    "foto": f"data:{mime};base64,{data}",
                    "has_foto": True,
                }
            except Exception:
                break

    # Placeholder — foto yok
    return {
        "student_id": student_id,
        "foto": None,
        "has_foto": False,
    }


# ══════════════════════════════════════════════════════════════
# TELAFI GOREVLERI
# ══════════════════════════════════════════════════════════════

@router.get("/telafi-gorevleri")
async def get_telafi_gorevleri(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    student_id: str | None = None,
):
    """Ogrencinin telafi gorevleri — renk bandi bazli."""
    sid = _target_student_id(user, student_id)

    telafi = adapter.load("olcme/telafi_tasks.json") or []
    my_telafi = [t for t in telafi if t.get("student_id") == sid]
    my_telafi.sort(key=lambda t: t.get("created_at", ""), reverse=True)

    aktif = [t for t in my_telafi if t.get("status") != "completed"]
    tamamlanan = [t for t in my_telafi if t.get("status") == "completed"]

    return {
        "aktif": aktif,
        "tamamlanan": tamamlanan,
        "toplam": len(my_telafi),
        "aktif_sayisi": len(aktif),
        "tamamlanan_sayisi": len(tamamlanan),
    }
