"""Anonim Ihbar Hatti router."""
from __future__ import annotations

import hashlib
import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from ..core.data_adapter import DataAdapter, DataPaths
from ..core.deps import get_current_user, get_data_adapter
from ..schemas.ihbar import (
    IHBAR_KATEGORILERI,
    IhbarCreateRequest,
    IhbarCreateResponse,
    IhbarStatusRequest,
    IhbarStatusResponse,
)


router = APIRouter(prefix="/ihbar", tags=["Ihbar Hatti"])


@router.get("/kategoriler")
async def kategoriler(_: Annotated[dict, Depends(get_current_user)]):
    """8 kategori + alt kategoriler."""
    return {
        "akran_zorbaligi": {
            "ad": "Akran Zorbaligi / Siddet",
            "seviye": "Yuksek",
            "alt": ["Fiziksel siddet", "Sozel taciz", "Sosyal dislama", "Siber zorbalik", "Tehdit"],
        },
        "intihar_riski": {
            "ad": "Intihar / Kendine Zarar Riski",
            "seviye": "Kritik",
            "alt": ["Kendine zarar verme isaretleri", "Intihardan bahsetme",
                   "Umutsuzluk ifadeleri", "Sosyal izolasyon"],
        },
        "madde_kullanim": {
            "ad": "Madde Kullanimi",
            "seviye": "Kritik",
            "alt": ["Uyusturucu suphesi", "Alkol kullanimi", "Sigara",
                   "Recetesiz ilac", "Vape/elektronik sigara"],
        },
        "cinsel_taciz": {
            "ad": "Cinsel Taciz / Istismar",
            "seviye": "Kritik",
            "alt": ["Ogrenci-ogrenci arasi", "Yetiskin tarafindan suphe",
                   "Uygunsuz mesaj/goruntu", "Diger"],
        },
        "aile_ici_siddet": {
            "ad": "Aile Ici Siddet / Ihmal",
            "seviye": "Kritik",
            "alt": ["Fiziksel siddet isareti", "Duygusal siddet", "Ihmal", "Evden kacma sinyali"],
        },
        "akademik_kopya": {
            "ad": "Akademik Sahtekarlik",
            "seviye": "Orta",
            "alt": ["Kopya", "Sahte belge", "Toplu kopya", "Baskasinin odevi"],
        },
        "personel_sikayet": {
            "ad": "Personel Sikayeti",
            "seviye": "Yuksek",
            "alt": ["Uygunsuz davranis", "Ayrimcilik", "Mesleki yetersizlik"],
        },
        "diger": {"ad": "Diger", "seviye": "Orta", "alt": ["Diger guvenlik konusu"]},
    }


@router.post("/gonder", response_model=IhbarCreateResponse, status_code=201)
async def gonder(
    req: IhbarCreateRequest,
    _: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """
    Anonim ihbar gonder. Hicbir kisi bilgisi kaydedilmez.

    ETIK: Bu endpoint'te JWT zorunlu (spam korumasi icin) ama kullanici
    bilgisi ihbar kaydina YAZILMAZ. Ihbar tamamen anonim saklanir.
    """
    if req.kategori not in IHBAR_KATEGORILERI:
        raise HTTPException(400, f"Gecersiz kategori. Listeden sec: {IHBAR_KATEGORILERI}")

    # Icerik hash — spam/tekrar tespiti
    content_hash = hashlib.sha256(req.aciklama.lower().strip().encode("utf-8")).hexdigest()[:12]

    # Tekrar kontrol
    mevcut = adapter.load(DataPaths.IHBAR) or []
    duplicate = next(
        (i for i in mevcut
         if i.get("hash") == content_hash
         and i.get("durum") not in ("Cozuldu", "Asilsiz")),
        None
    )
    if duplicate:
        return IhbarCreateResponse(
            anonim_id=duplicate.get("anonim_id", ""),
            takip_kodu=duplicate.get("takip_kodu", ""),
            mesaj=f"Bu konu daha once bildirilmis ve inceleniyor. ID: {duplicate.get('anonim_id')}",
        )

    anonim_id = f"IHB-{uuid.uuid4().hex[:10].upper()}"
    takip_kodu = ""
    if req.geri_donus_istiyor:
        takip_kodu = hashlib.sha256(
            f"{anonim_id}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:8].upper()

    yeni = {
        "anonim_id": anonim_id,
        "hash": content_hash,
        "kategori": req.kategori,
        "kategori_ad": req.kategori.replace("_", " ").title(),
        "alt_kategori": req.alt_kategori,
        "seviye": "Kritik" if req.kategori in ("intihar_riski", "madde_kullanim",
                                              "cinsel_taciz", "aile_ici_siddet") else "Yuksek",
        "aciklama": req.aciklama.strip(),
        "nerede": req.nerede.strip(),
        "ne_zaman": req.ne_zaman.strip(),
        "kim_icin": req.kim_icin,
        "geri_donus_istiyor": req.geri_donus_istiyor,
        "durum": "Yeni",
        "olusturma_tarihi": datetime.now().isoformat(),
        "guncelleme_tarihi": datetime.now().isoformat(),
        "rehber_notlari": [],
        "aksiyon_gecmisi": [],
        "takip_kodu": takip_kodu,
    }
    adapter.append(DataPaths.IHBAR, yeni)

    return IhbarCreateResponse(
        anonim_id=anonim_id,
        takip_kodu=takip_kodu,
        mesaj="Ihbariniz güvenli bir sekilde iletildi. Rehber ekibi 24 saat icinde değerlendirecek.",
    )


@router.post("/durum", response_model=IhbarStatusResponse)
async def durum(
    req: IhbarStatusRequest,
    _: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Takip kodu ile ihbarin durumunu sorgula (anonim)."""
    ihbarlar = adapter.load(DataPaths.IHBAR) or []
    i = next((x for x in ihbarlar if x.get("takip_kodu") == req.takip_kodu.upper()), None)
    if not i:
        raise HTTPException(404, "Takip kodu bulunamadi")

    # Rehber notu — son not
    notlar = i.get("rehber_notlari", [])
    son_not = notlar[-1].get("not", "") if notlar else ""

    return IhbarStatusResponse(
        anonim_id=i.get("anonim_id", ""),
        kategori=i.get("kategori", ""),
        durum=i.get("durum", ""),
        rehber_notu=son_not,
        olusturma_tarihi=i.get("olusturma_tarihi", ""),
    )
