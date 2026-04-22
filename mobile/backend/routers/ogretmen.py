"""Ogretmen endpoint'leri — yoklama, not, ders defteri, odev atama."""
from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from ..core.data_adapter import DataAdapter, DataPaths
from ..core.deps import get_current_user, get_data_adapter, require_roles
from ..schemas.ogretmen import (
    DersDefteriItem,
    DersDefteriRequest,
    NotBatchRequest,
    NotBatchResponse,
    OdevAtaRequest,
    SinifListResponse,
    SinifOgrenci,
    YoklamaBatchRequest,
    YoklamaBatchResponse,
)


router = APIRouter(prefix="/ogretmen", tags=["Ogretmen"])


# Ders defteri path (DataPaths'te yok)
class OgretmenPaths:
    DERS_DEFTERI = "akademik/ders_defteri.json"


def _require_ogretmen(user: dict):
    role = user.get("role", "").lower()
    if role not in ("ogretmen", "superadmin", "yonetici", "mudur", "mudur_yardimcisi",
                    "sinif_ogretmeni", "brans_ogretmeni"):
        raise HTTPException(403, "Sadece ogretmen bu endpoint'i kullanabilir")


# ══════════════════════════════════════════════════════════════
# SINIF LISTESI
# ══════════════════════════════════════════════════════════════

@router.get("/sinif/{sinif}/{sube}", response_model=SinifListResponse)
async def sinif_ogrencileri(
    sinif: str,
    sube: str,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Belirli sinif/sube icinn ogrenci listesi."""
    _require_ogretmen(user)
    students = adapter.load(DataPaths.STUDENTS) or []
    mine = [s for s in students
            if str(s.get("sinif", "")) == str(sinif)
            and s.get("sube", "") == sube
            and s.get("durum", "aktif") == "aktif"]
    def _numara_key(s):
        n = s.get("numara", "0") or "0"
        try:
            return int(n)
        except ValueError:
            return 0
    mine.sort(key=_numara_key)

    ogrenciler = [
        SinifOgrenci(
            id=s.get("id", ""),
            ad_soyad=f"{s.get('ad','')} {s.get('soyad','')}".strip(),
            numara=str(s.get("numara", "")),
            sinif=str(s.get("sinif", "")),
            sube=s.get("sube", ""),
        )
        for s in mine
    ]
    return SinifListResponse(sinif=sinif, sube=sube, ogrenciler=ogrenciler)


@router.get("/siniflarim")
async def siniflarim(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Ogretmene atanmis sinif/sube listesi."""
    _require_ogretmen(user)
    students = adapter.load(DataPaths.STUDENTS) or []
    # Basit: tum unique sinif/sube kombinasyonlari
    combos = set()
    for s in students:
        if s.get("durum", "aktif") == "aktif":
            combos.add((str(s.get("sinif", "")), s.get("sube", "")))
    return [{"sinif": c[0], "sube": c[1],
            "ogrenci_sayisi": sum(1 for s in students
                                 if str(s.get("sinif", "")) == c[0]
                                 and s.get("sube", "") == c[1])}
            for c in sorted(combos)]


# ══════════════════════════════════════════════════════════════
# YOKLAMA
# ══════════════════════════════════════════════════════════════

@router.post("/yoklama", response_model=YoklamaBatchResponse)
async def yoklama_batch(
    req: YoklamaBatchRequest,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Toplu yoklama girisi — tum sinif icin."""
    _require_ogretmen(user)

    existing = adapter.load(DataPaths.ATTENDANCE) or []
    now = datetime.now()
    akademik_yil = f"{now.year if now.month >= 9 else now.year - 1}-{now.year + 1 if now.month >= 9 else now.year}"

    eklenen, guncellenen = 0, 0

    for y in req.yoklamalar:
        # Ayni ogrenci/tarih/ders/saat varsa guncelle
        idx = next(
            (i for i, a in enumerate(existing)
             if a.get("student_id") == y.student_id
             and a.get("tarih") == req.tarih
             and a.get("ders") == req.ders
             and int(a.get("ders_saati", 0) or 0) == req.ders_saati),
            None,
        )
        if idx is not None:
            existing[idx]["turu"] = y.turu
            existing[idx]["aciklama"] = y.aciklama
            guncellenen += 1
        else:
            existing.append({
                "id": f"dev_{uuid.uuid4().hex[:8]}",
                "student_id": y.student_id,
                "tarih": req.tarih,
                "ders": req.ders,
                "ders_saati": req.ders_saati,
                "turu": y.turu,
                "aciklama": y.aciklama,
                "akademik_yil": akademik_yil,
            })
            eklenen += 1

    adapter.save(DataPaths.ATTENDANCE, existing)

    # ── SMS/Email devamsızlık bildirimi (BildirimServisi) ──
    try:
        from utils.bildirim_servisi import get_bildirim_servisi
        bs = get_bildirim_servisi()
        for y in req.yoklamalar:
            if y.turu in ('devamsiz', 'ozursuz'):
                bs.devamsizlik_bildirimi(y.student_id, req.tarih, req.ders)
    except Exception:
        pass  # SMS failure should not block yoklama save

    # ── Veliye otomatik devamsızlık bildirimi ──
    _yoklama_veli_bildirim(adapter, req, existing, user)

    return YoklamaBatchResponse(eklenen=eklenen, guncellenen=guncellenen, tarih=req.tarih)


def _yoklama_veli_bildirim(
    adapter: DataAdapter,
    req: YoklamaBatchRequest,
    all_attendance: list[dict],
    teacher: dict,
):
    """Yoklama sonrası veliye otomatik bildirim gönderir.

    Kurallar:
    - 1. ders yoklamasında devamsız → "Öğrencimiz X bugün okula gelmemiştir."
    - Sonraki derslerde devam var AMA önceki derslerde devamsızdı
      → "Öğrencimiz X N. derste okula gelmiştir."
    """
    students = adapter.load(DataPaths.STUDENTS) or []
    users = adapter.load("users.json") or []
    mesaj_path = "akademik/veli_mesajlar.json"

    stu_map = {s.get("id"): s for s in students}
    # Veli haritası: ogrenci_id → veli user
    veli_map: dict[str, dict] = {}
    for u in users:
        if u.get("role", "").lower() == "veli" and u.get("ogrenci_id"):
            veli_map[u["ogrenci_id"]] = u

    ogretmen_adi = teacher.get("ad_soyad", teacher.get("name", "Öğretmen"))
    ogretmen_id = teacher.get("user_id", "")
    tarih = req.tarih
    tarih_gosterim = f"{tarih[8:10]}.{tarih[5:7]}.{tarih[:4]}" if len(tarih) >= 10 else tarih

    for y in req.yoklamalar:
        stu = stu_map.get(y.student_id)
        if not stu:
            continue
        ad_soyad = f"{stu.get('ad', '')} {stu.get('soyad', '')}".strip()
        veli = veli_map.get(y.student_id)
        if not veli:
            continue

        if y.turu in ("devamsiz", "ozursuz"):
            # 1. ders: "okula gelmemiştir"
            if req.ders_saati == 1:
                mesaj_text = (
                    f"Sayın Veli, öğrencimiz {ad_soyad} bugün ({tarih_gosterim}) "
                    f"okula gelmemiştir. Bilginize."
                )
                _yoklama_mesaj_ekle(adapter, mesaj_path, y.student_id,
                                   veli, ogretmen_id, ogretmen_adi, mesaj_text)

        elif y.turu == "devam" and req.ders_saati > 1:
            # Önceki derslerde devamsız mıydı?
            onceki_devamsiz = any(
                a for a in all_attendance
                if a.get("student_id") == y.student_id
                and a.get("tarih") == tarih
                and int(a.get("ders_saati", 0) or 0) < req.ders_saati
                and a.get("turu") in ("devamsiz", "ozursuz")
            )
            if onceki_devamsiz:
                mesaj_text = (
                    f"Sayın Veli, öğrencimiz {ad_soyad} bugün ({tarih_gosterim}) "
                    f"{req.ders_saati}. derste okula gelmiştir. Bilginize."
                )
                _yoklama_mesaj_ekle(adapter, mesaj_path, y.student_id,
                                   veli, ogretmen_id, ogretmen_adi, mesaj_text)


def _yoklama_mesaj_ekle(
    adapter: DataAdapter,
    path: str,
    student_id: str,
    veli: dict,
    ogretmen_id: str,
    ogretmen_adi: str,
    mesaj_text: str,
):
    """Yoklama bildirimini veli mesajlarına ekler."""
    yeni = {
        "id": f"vm_{uuid.uuid4().hex[:8]}",
        "student_id": student_id,
        "veli_adi": veli.get("name", ""),
        "ogretmen_id": ogretmen_id,
        "ogretmen_adi": ogretmen_adi,
        "tarih": datetime.now().isoformat(),
        "mesaj": mesaj_text,
        "yon": "sistem_to_veli",
        "okundu": False,
    }
    adapter.append(path, yeni)


@router.get("/yoklama/bugun/{sinif}/{sube}")
async def yoklama_bugun(
    sinif: str,
    sube: str,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    ders: str | None = None,
    ders_saati: int | None = None,
):
    """Bugun girilen yoklama (varsa)."""
    _require_ogretmen(user)
    today = date.today().isoformat()
    att = adapter.load(DataPaths.ATTENDANCE) or []

    students = adapter.load(DataPaths.STUDENTS) or []
    student_ids = {s.get("id") for s in students
                  if str(s.get("sinif", "")) == str(sinif) and s.get("sube", "") == sube}

    mine = [
        a for a in att
        if a.get("student_id") in student_ids
        and a.get("tarih") == today
        and (ders is None or a.get("ders") == ders)
        and (ders_saati is None or int(a.get("ders_saati", 0) or 0) == ders_saati)
    ]
    return {"tarih": today, "kayitlar": mine}


# ══════════════════════════════════════════════════════════════
# NOT GIRISI
# ══════════════════════════════════════════════════════════════

@router.post("/not", response_model=NotBatchResponse)
async def not_batch(
    req: NotBatchRequest,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Toplu not girisi."""
    _require_ogretmen(user)

    grades = adapter.load(DataPaths.GRADES) or []
    now = datetime.now()
    akademik_yil = f"{now.year if now.month >= 9 else now.year - 1}-{now.year + 1 if now.month >= 9 else now.year}"

    eklenen = 0
    for n in req.notlar:
        grades.append({
            "id": f"not_{uuid.uuid4().hex[:8]}",
            "student_id": n.student_id,
            "ders": req.ders,
            "sinif": req.sinif,
            "sube": req.sube,
            "donem": req.donem,
            "not_turu": req.not_turu,
            "not_sirasi": req.not_sirasi,
            "puan": n.puan,
            "tarih": req.tarih,
            "aciklama": n.aciklama,
            "akademik_yil": akademik_yil,
        })
        eklenen += 1

    adapter.save(DataPaths.GRADES, grades)
    return NotBatchResponse(eklenen=eklenen, tarih=req.tarih)


# ══════════════════════════════════════════════════════════════
# DERS DEFTERI
# ══════════════════════════════════════════════════════════════

@router.post("/ders-defteri", response_model=DersDefteriItem, status_code=201)
async def ders_defteri_ekle(
    req: DersDefteriRequest,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Ders defteri kaydi ekle."""
    _require_ogretmen(user)

    yeni = {
        "id": f"dd_{uuid.uuid4().hex[:8]}",
        "sinif": req.sinif,
        "sube": req.sube,
        "ders": req.ders,
        "ders_saati": req.ders_saati,
        "tarih": req.tarih,
        "islenen_konu": req.islenen_konu,
        "ozel_not": req.ozel_not,
        "online_link": req.online_link,
        "kazanimlar": req.kazanimlar,
        "ogretmen_id": user.get("user_id", ""),
        "ogretmen_adi": user.get("ad_soyad", ""),
    }
    adapter.append(OgretmenPaths.DERS_DEFTERI, yeni)

    return DersDefteriItem(
        id=yeni["id"], sinif=yeni["sinif"], sube=yeni["sube"],
        ders=yeni["ders"], ders_saati=yeni["ders_saati"], tarih=yeni["tarih"],
        islenen_konu=yeni["islenen_konu"], ozel_not=yeni["ozel_not"],
        online_link=yeni["online_link"],
        ogretmen_id=yeni["ogretmen_id"], ogretmen_adi=yeni["ogretmen_adi"],
    )


@router.get("/ders-defteri/{sinif}/{sube}")
async def ders_defteri_list(
    sinif: str, sube: str,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    limit: int = 30,
):
    """Sinif/sube icin son N ders defteri kaydi."""
    _require_ogretmen(user)
    all_dd = adapter.load(OgretmenPaths.DERS_DEFTERI) or []
    mine = [d for d in all_dd
           if d.get("sinif") == sinif and d.get("sube") == sube]
    mine.sort(key=lambda d: (d.get("tarih", ""), d.get("ders_saati", 0)),
             reverse=True)
    return mine[:limit]


# ══════════════════════════════════════════════════════════════
# ODEV ATA
# ══════════════════════════════════════════════════════════════

@router.post("/odev/ata", status_code=201)
async def odev_ata(
    req: OdevAtaRequest,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Yeni odev ata. Sinif/sube tum ogrencilerine verilir."""
    _require_ogretmen(user)
    now = datetime.now()
    akademik_yil = f"{now.year if now.month >= 9 else now.year - 1}-{now.year + 1 if now.month >= 9 else now.year}"

    yeni = {
        "id": f"odev_{uuid.uuid4().hex[:8]}",
        "baslik": req.baslik,
        "ders": req.ders,
        "sinif": req.sinif,
        "sube": req.sube,
        "ogretmen_id": user.get("user_id", ""),
        "ogretmen_adi": user.get("ad_soyad", ""),
        "tur": req.tur,
        "aciklama": req.aciklama,
        "verilis_tarihi": req.verilis_tarihi,
        "teslim_tarihi": req.teslim_tarihi,
        "durum": "aktif",
        "kaynak_url": req.kaynak_url,
        "akademik_yil": akademik_yil,
    }
    adapter.append(DataPaths.HOMEWORK, yeni)
    return {"id": yeni["id"]}


# ══════════════════════════════════════════════════════════════
# OGRETMEN ICIN OGRENCI OZETI
# ══════════════════════════════════════════════════════════════

@router.get("/ogrenci-ozet/{student_id}")
async def ogrenci_ozet(
    student_id: str,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Ogretmen icin ogrenci hizli ozet (not ort, devamsizlik, son not)."""
    _require_ogretmen(user)

    students = adapter.load(DataPaths.STUDENTS) or []
    s = next((x for x in students if x.get("id") == student_id), None)
    if not s:
        raise HTTPException(404, "Ogrenci bulunamadi")

    grades = adapter.load(DataPaths.GRADES) or []
    att = adapter.load(DataPaths.ATTENDANCE) or []

    mine_grades = [g for g in grades if g.get("student_id") == student_id]
    mine_att = [a for a in att if a.get("student_id") == student_id]

    puanlar = [float(g.get("puan", 0) or 0) for g in mine_grades]
    devamsizlik = sum(1 for a in mine_att if a.get("turu", "").lower() in ("devamsiz", "ozursuz"))

    return {
        "student_id": student_id,
        "ad_soyad": f"{s.get('ad','')} {s.get('soyad','')}",
        "sinif": s.get("sinif", ""),
        "sube": s.get("sube", ""),
        "numara": s.get("numara", ""),
        "not_ortalamasi": round(sum(puanlar) / len(puanlar), 1) if puanlar else 0.0,
        "not_sayisi": len(puanlar),
        "devamsizlik_sayisi": devamsizlik,
    }


# ══════════════════════════════════════════════════════════════
# SINAV SONUCLARI — sinif/ders bazli
# ══════════════════════════════════════════════════════════════

@router.get("/sinav-sonuclari")
async def sinav_sonuclari(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    sinif: str | None = None,
    sube: str | None = None,
    ders: str | None = None,
):
    """Sinif/ders bazli sinav sonuclari — ogretmen + yonetici."""
    _require_ogretmen(user)
    all_grades = adapter.load(DataPaths.GRADES) or []

    sinavlar = [g for g in all_grades
                if g.get("not_turu", "").lower() in ("yazili", "sinav", "deneme")]

    if sinif:
        sinavlar = [g for g in sinavlar if str(g.get("sinif", "")) == sinif]
    if sube:
        sinavlar = [g for g in sinavlar if g.get("sube", "") == sube]
    if ders:
        sinavlar = [g for g in sinavlar if g.get("ders", "").lower() == ders.lower()]

    sinavlar.sort(key=lambda g: g.get("tarih", ""), reverse=True)

    students = adapter.load(DataPaths.STUDENTS) or []
    stu_map = {s.get("id"): f"{s.get('ad', '')} {s.get('soyad', '')}".strip()
               for s in students}

    from collections import defaultdict
    sinav_gruplari: dict[str, list] = defaultdict(list)
    for g in sinavlar:
        key = f"{g.get('ders','')}|{g.get('not_turu','')} {g.get('not_sirasi','')}|{g.get('tarih','')}"
        sinav_gruplari[key].append(g)

    sonuc_listesi = []
    for key, notlar in list(sinav_gruplari.items())[:20]:
        parts = key.split("|")
        puanlar = [float(n.get("puan", 0) or 0) for n in notlar]
        sonuc_listesi.append({
            "ders": parts[0] if parts else "",
            "sinav_adi": parts[1] if len(parts) > 1 else "",
            "tarih": parts[2] if len(parts) > 2 else "",
            "sinif": f"{notlar[0].get('sinif','')}/{notlar[0].get('sube','')}" if notlar else "",
            "ogrenci_sayisi": len(notlar),
            "ortalama": round(sum(puanlar) / len(puanlar), 1) if puanlar else 0,
            "en_yuksek": max(puanlar) if puanlar else 0,
            "en_dusuk": min(puanlar) if puanlar else 0,
            "basari_orani": round(sum(1 for p in puanlar if p >= 50) / len(puanlar) * 100, 1) if puanlar else 0,
            "detay": [
                {"ogrenci": stu_map.get(n.get("student_id"), "?"),
                 "puan": n.get("puan")}
                for n in sorted(notlar, key=lambda x: float(x.get("puan", 0) or 0), reverse=True)
            ][:30],
        })

    tum_dersler = sorted(set(g.get("ders", "") for g in all_grades if g.get("ders")))
    tum_siniflar = sorted(set(f"{g.get('sinif','')}/{g.get('sube','')}" for g in all_grades if g.get("sinif")))

    return {
        "toplam_sinav": len(sinav_gruplari),
        "sonuclar": sonuc_listesi,
        "filtreler": {"dersler": tum_dersler, "siniflar": tum_siniflar},
    }
