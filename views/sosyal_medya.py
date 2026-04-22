"""
Sosyal Medya Yonetimi Modulu (SMM-01)
======================================
Okul sosyal medya hesaplarini tek panelden yonetme:
icerik olusturma, direkt/onayli yayin, takvim, analytics,
gelen kutusu, uyarilar.
"""

from __future__ import annotations

import base64
import calendar
import json
import os
import time
import urllib.parse
import uuid
from datetime import datetime, timedelta

import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

from utils.chart_utils import SC_COLORS, sc_pie, sc_bar, SC_CHART_CFG
from utils.tenant import get_tenant_dir, ensure_tenant_dir
from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("sosyal_medya")
except Exception:
    pass
try:
    from utils.ui_common import modul_hosgeldin, bildirim_cani
    bildirim_cani(0)
    modul_hosgeldin("sosyal_medya",
        "Coklu platform yonetimi, icerik takvimi, sentiment analiz, rakip izleme",
        [("5", "Platform"), ("AI", "Sentiment"), ("30", "Gun Plan")])
except Exception:
    pass
from models.sosyal_medya import (
    SMMDataStore, SMMPost, SMMAccount, SMMAsset, SMMInboxMessage, SMMAlert,
    Rakip, HashtagPerformans, MarkaAyar, MarkaKontrolcu,
    SentimentAnalyzer, EngelliSaatOnerici, HashtagTracker,
    check_smm_yetki, get_smm_store,
    PLATFORM_KARAKTER_LIMITI, VARSAYILAN_EN_IYI_SAATLER,
    SENTIMENT_LABELS, SMM_YETKILER as SMM_YETKILER_MODEL,
)

# ===================== SABITLER =====================

PLATFORMLAR = [
    ("instagram", "\U0001f4f8", "Instagram", "#E4405F"),
    ("facebook", "\U0001f4d8", "Facebook", "#1877F2"),
    ("linkedin", "\U0001f4bc", "LinkedIn", "#0A66C2"),
    ("tiktok", "\U0001f3b5", "TikTok", "#000000"),
    ("youtube", "\U0001f3ac", "YouTube", "#FF0000"),
    ("x_twitter", "\U0001f426\u200d\u2b1b", "X (Twitter)", "#000000"),
    ("whatsapp_business", "\U0001f4ac", "WhatsApp Business", "#25D366"),
    ("email", "\U0001f4e7", "E-posta", "#4285F4"),
]

PLATFORM_MAP = {p[0]: {"icon": p[1], "label": p[2], "color": p[3]} for p in PLATFORMLAR}

STATUSLER = [
    ("DRAFT", "Taslak", "#94a3b8"),
    ("READY_TO_PUBLISH", "Yayina Hazir", "#3b82f6"),
    ("SUBMITTED", "Onaya Gonderildi", "#f59e0b"),
    ("IN_REVIEW", "Incelemede", "#8b5cf6"),
    ("CHANGES_REQUESTED", "Revizyon Istendi", "#ef4444"),
    ("APPROVED", "Onaylandi", "#10b981"),
    ("SCHEDULED", "Planlandi", "#0d9488"),
    ("PUBLISHING", "Yayinlaniyor", "#6366f1"),
    ("PUBLISHED", "Yayinlandi", "#22c55e"),
    ("PUBLISH_FAILED", "Yayin Hatasi", "#dc2626"),
    ("MANUAL_ACTION_REQUIRED", "Manuel Tamamlama", "#f97316"),
    ("CANCELED", "Iptal", "#6b7280"),
]

STATUS_MAP = {s[0]: {"label": s[1], "color": s[2]} for s in STATUSLER}

KAMPANYA_ETIKETLERI = [
    "Bursluluk", "Gezi", "Kayıt", "Duyuru", "Başarı",
    "Etkinlik", "Mezuniyet", "Spor", "Kultur", "Diger",
]

SMM_YETKILER = [
    ("hesap_baglama", "Hesap Baglama"),
    ("icerik_olusturma", "İçerik Oluşturma"),
    ("direkt_yayin", "Direkt Yayin"),
    ("planlama", "Planlama"),
    ("onay", "Onay"),
    ("rapor", "Rapor Görüntüleme"),
    ("gelen_kutusu", "Gelen Kutusu Yönetimi"),
]

_EXCEL_PALETTE = ["#4472C4", "#FFC000", "#ED7D31", "#A5A5A5", "#5B9BD5"]

GRAPH_API = "https://graph.facebook.com/v21.0"
LINKEDIN_API = "https://api.linkedin.com/v2"
TIKTOK_API = "https://open.tiktokapis.com/v2"
YOUTUBE_API = "https://www.googleapis.com/youtube/v3"
X_API = "https://api.x.com/2"
WHATSAPP_BIZ_API = "https://graph.facebook.com/v21.0"  # WhatsApp Business Cloud API


# ===================== SOSYAL MEDYA API ENTEGRASYONU =====================

class SocialMediaAPI:
    """Gercek sosyal medya platformlari API entegrasyonu."""

    # ---------- BAGLANTI TESTI ----------

    @staticmethod
    def test_connection(platform: str, creds: dict) -> dict:
        """API baglanti testi. Returns {"ok": bool, "message": str, "data": dict}"""
        try:
            if platform == "facebook":
                return SocialMediaAPI._test_facebook(creds)
            elif platform == "instagram":
                return SocialMediaAPI._test_instagram(creds)
            elif platform == "linkedin":
                return SocialMediaAPI._test_linkedin(creds)
            elif platform == "tiktok":
                return SocialMediaAPI._test_tiktok(creds)
            elif platform == "youtube":
                return SocialMediaAPI._test_youtube(creds)
            elif platform == "x_twitter":
                return SocialMediaAPI._test_x_twitter(creds)
            elif platform == "whatsapp_business":
                return SocialMediaAPI._test_whatsapp_business(creds)
            elif platform == "email":
                return SocialMediaAPI._test_email(creds)
            return {"ok": False, "message": "Bilinmeyen platform"}
        except requests.exceptions.ConnectionError:
            return {"ok": False, "message": "Baglanti hatasi - internet baglantinizi kontrol edin"}
        except Exception as e:
            return {"ok": False, "message": f"Hata: {str(e)}"}

    @staticmethod
    def _test_facebook(creds: dict) -> dict:
        token = creds.get("access_token", "")
        page_id = creds.get("page_id", "")
        if not token:
            return {"ok": False, "message": "Access Token gerekli"}
        url = f"{GRAPH_API}/{page_id or 'me'}"
        r = requests.get(url, params={"access_token": token, "fields": "id,name"}, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return {"ok": True, "message": f"Bagli: {data.get('name', '')} (ID: {data.get('id', '')})", "data": data}
        err = r.json().get("error", {}).get("message", r.text)
        return {"ok": False, "message": f"Facebook API hatasi: {err}"}

    @staticmethod
    def _test_instagram(creds: dict) -> dict:
        token = creds.get("access_token", "")
        ig_id = creds.get("page_id", "")
        if not token or not ig_id:
            return {"ok": False, "message": "Access Token ve Instagram Business Account ID gerekli"}
        url = f"{GRAPH_API}/{ig_id}"
        r = requests.get(url, params={"access_token": token, "fields": "id,username,followers_count,media_count"}, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return {"ok": True, "message": f"Bagli: @{data.get('username', '')} ({data.get('followers_count', 0)} takipci)", "data": data}
        err = r.json().get("error", {}).get("message", r.text)
        return {"ok": False, "message": f"Instagram API hatasi: {err}"}

    @staticmethod
    def _test_linkedin(creds: dict) -> dict:
        token = creds.get("access_token", "")
        if not token:
            return {"ok": False, "message": "Access Token gerekli"}
        url = f"{LINKEDIN_API}/me"
        r = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=10)
        if r.status_code == 200:
            data = r.json()
            name = f"{data.get('localizedFirstName', '')} {data.get('localizedLastName', '')}"
            return {"ok": True, "message": f"Bagli: {name}", "data": data}
        return {"ok": False, "message": f"LinkedIn API hatasi: {r.status_code} - {r.text[:200]}"}

    @staticmethod
    def _test_tiktok(creds: dict) -> dict:
        token = creds.get("access_token", "")
        if not token:
            return {"ok": False, "message": "Access Token gerekli"}
        url = f"{TIKTOK_API}/user/info/"
        r = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=10)
        if r.status_code == 200:
            data = r.json().get("data", {}).get("user", {})
            return {"ok": True, "message": f"Bagli: @{data.get('display_name', '')}", "data": data}
        return {"ok": False, "message": f"TikTok API hatasi: {r.status_code}"}

    @staticmethod
    def _test_youtube(creds: dict) -> dict:
        token = creds.get("access_token", "")
        if not token:
            return {"ok": False, "message": "Access Token (OAuth2) gerekli"}
        url = f"{YOUTUBE_API}/channels"
        r = requests.get(url, params={"part": "snippet", "mine": "true"},
                         headers={"Authorization": f"Bearer {token}"}, timeout=10)
        if r.status_code == 200:
            items = r.json().get("items", [])
            if items:
                name = items[0].get("snippet", {}).get("title", "")
                return {"ok": True, "message": f"Bagli: {name}", "data": items[0]}
            return {"ok": False, "message": "Kanal bulunamadı"}
        return {"ok": False, "message": f"YouTube API hatasi: {r.status_code}"}

    @staticmethod
    def _test_x_twitter(creds: dict) -> dict:
        token = creds.get("access_token", "")
        if not token:
            return {"ok": False, "message": "Bearer Token gerekli"}
        url = f"{X_API}/users/me"
        r = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=10)
        if r.status_code == 200:
            data = r.json().get("data", {})
            return {"ok": True, "message": f"Bagli: @{data.get('username', '')}", "data": data}
        return {"ok": False, "message": f"X API hatasi: {r.status_code}"}

    @staticmethod
    def _test_whatsapp_business(creds: dict) -> dict:
        token = creds.get("access_token", "")
        phone_id = creds.get("phone_number_id", "")
        if not token or not phone_id:
            return {"ok": False, "message": "Access Token ve Phone Number ID gerekli"}
        url = f"{WHATSAPP_BIZ_API}/{phone_id}"
        r = requests.get(url, params={"access_token": token}, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return {"ok": True, "message": f"Bagli: {data.get('display_phone_number', phone_id)}", "data": data}
        return {"ok": False, "message": f"WhatsApp Business API hatasi: {r.status_code}"}

    @staticmethod
    def _test_email(creds: dict) -> dict:
        smtp_host = creds.get("api_key", "")  # API Key alaninda SMTP Host
        smtp_port = creds.get("api_secret", "587")  # API Secret alaninda SMTP Port
        email_addr = creds.get("page_id", "")  # Page ID alaninda E-posta adresi
        pwd = creds.get("access_token", "")  # Access Token alaninda SMTP sifre
        if not smtp_host or not email_addr:
            return {"ok": False, "message": "SMTP Host ve E-posta adresi gerekli"}
        try:
            import smtplib
            with smtplib.SMTP(smtp_host, int(smtp_port or 587), timeout=10, local_hostname="localhost") as s:
                s.ehlo()
                s.starttls()
                if pwd:
                    s.login(email_addr, pwd)
            return {"ok": True, "message": f"SMTP baglantisi basarili: {email_addr}"}
        except Exception as e:
            return {"ok": False, "message": f"SMTP hatasi: {str(e)}"}

    # ---------- YAYINLAMA ----------

    @staticmethod
    def publish(platform: str, creds: dict, text: str, media_paths: list,
                hashtags: list | None = None) -> dict:
        """Icerik yayinla. Returns {"ok": bool, "message": str, "post_id": str}"""
        full_text = text
        if hashtags:
            full_text += "\n\n" + " ".join(hashtags)
        try:
            if platform == "facebook":
                return SocialMediaAPI._publish_facebook(creds, full_text, media_paths)
            elif platform == "instagram":
                return SocialMediaAPI._publish_instagram(creds, full_text, media_paths)
            elif platform == "linkedin":
                return SocialMediaAPI._publish_linkedin(creds, full_text, media_paths)
            elif platform == "tiktok":
                return SocialMediaAPI._publish_tiktok(creds, full_text, media_paths)
            elif platform == "youtube":
                return SocialMediaAPI._publish_youtube(creds, full_text, media_paths)
            elif platform == "x_twitter":
                return SocialMediaAPI._publish_x_twitter(creds, full_text, media_paths)
            elif platform == "whatsapp_business":
                return {"ok": False, "message": "WhatsApp Business için mesaj gonderimi Kullanıcı Yönetimi uzerinden yapilir"}
            elif platform == "email":
                return {"ok": False, "message": "E-posta gonderimi İletişim sekmesi uzerinden yapilir"}
            return {"ok": False, "message": "Bilinmeyen platform"}
        except requests.exceptions.ConnectionError:
            return {"ok": False, "message": "Baglanti hatasi"}
        except Exception as e:
            return {"ok": False, "message": f"Yayinlama hatasi: {str(e)}"}

    # --- FACEBOOK ---
    @staticmethod
    def _publish_facebook(creds: dict, text: str, media_paths: list) -> dict:
        token = creds.get("access_token", "")
        page_id = creds.get("page_id", "")
        if not token or not page_id:
            return {"ok": False, "message": "Page ID ve Access Token gerekli"}

        images = [m for m in media_paths if m.get("tip") == "image"]
        videos = [m for m in media_paths if m.get("tip") == "video"]

        # Coklu gorsel: once her gorseli upload et, sonra multi-photo post olustur
        if len(images) > 1:
            photo_ids = []
            for img in images:
                fpath = img.get("dosya", "")
                if not os.path.exists(fpath):
                    continue
                with open(fpath, "rb") as f:
                    r = requests.post(
                        f"{GRAPH_API}/{page_id}/photos",
                        data={"access_token": token, "published": "false"},
                        files={"source": f}, timeout=60
                    )
                if r.status_code == 200:
                    photo_ids.append(r.json().get("id"))
            # Multi-photo post
            params = {"message": text, "access_token": token}
            for i, pid in enumerate(photo_ids):
                params[f"attached_media[{i}]"] = json.dumps({"media_fbid": pid})
            r = requests.post(f"{GRAPH_API}/{page_id}/feed", data=params, timeout=30)
            if r.status_code == 200:
                return {"ok": True, "post_id": r.json().get("id", ""), "message": "Facebook coklu gorsel paylasim basarili"}
            err = r.json().get("error", {}).get("message", r.text)
            return {"ok": False, "message": f"Facebook post hatasi: {err}"}

        # Tek gorsel
        elif len(images) == 1:
            fpath = images[0].get("dosya", "")
            if os.path.exists(fpath):
                with open(fpath, "rb") as f:
                    r = requests.post(
                        f"{GRAPH_API}/{page_id}/photos",
                        data={"message": text, "access_token": token},
                        files={"source": f}, timeout=60
                    )
                if r.status_code == 200:
                    return {"ok": True, "post_id": r.json().get("id", ""), "message": "Facebook gorsel paylasim basarili"}
                err = r.json().get("error", {}).get("message", r.text)
                return {"ok": False, "message": f"Facebook foto hatasi: {err}"}

        # Video
        elif videos:
            fpath = videos[0].get("dosya", "")
            if os.path.exists(fpath):
                with open(fpath, "rb") as f:
                    r = requests.post(
                        f"{GRAPH_API}/{page_id}/videos",
                        data={"description": text, "access_token": token},
                        files={"source": f}, timeout=120
                    )
                if r.status_code == 200:
                    return {"ok": True, "post_id": r.json().get("id", ""), "message": "Facebook video paylasim basarili"}
                err = r.json().get("error", {}).get("message", r.text)
                return {"ok": False, "message": f"Facebook video hatasi: {err}"}

        # Sadece metin
        r = requests.post(
            f"{GRAPH_API}/{page_id}/feed",
            data={"message": text, "access_token": token}, timeout=30
        )
        if r.status_code == 200:
            return {"ok": True, "post_id": r.json().get("id", ""), "message": "Facebook metin paylasim basarili"}
        err = r.json().get("error", {}).get("message", r.text)
        return {"ok": False, "message": f"Facebook hatasi: {err}"}

    # --- INSTAGRAM ---
    @staticmethod
    def _publish_instagram(creds: dict, text: str, media_paths: list) -> dict:
        token = creds.get("access_token", "")
        ig_id = creds.get("page_id", "")
        if not token or not ig_id:
            return {"ok": False, "message": "IG Business ID ve Access Token gerekli"}

        images = [m for m in media_paths if m.get("tip") == "image"]
        videos = [m for m in media_paths if m.get("tip") == "video"]

        # Instagram gorsel gerektiriyor (sadece metin post yok)
        if not images and not videos:
            return {"ok": False, "message": "Instagram için gorsel veya video gerekli"}

        # Carousel (coklu gorsel)
        if len(images) > 1:
            children_ids = []
            for img in images:
                fpath = img.get("dosya", "")
                # Instagram Graph API için gorsel URL gerekiyor
                # Lokal dosya icin: once Facebook'a yukle, URL al
                image_url = _get_hosted_url(creds, fpath)
                if not image_url:
                    continue
                r = requests.post(
                    f"{GRAPH_API}/{ig_id}/media",
                    data={"image_url": image_url, "is_carousel_item": "true", "access_token": token},
                    timeout=30
                )
                if r.status_code == 200:
                    children_ids.append(r.json().get("id"))

            if children_ids:
                # Carousel container
                r = requests.post(
                    f"{GRAPH_API}/{ig_id}/media",
                    data={
                        "media_type": "CAROUSEL",
                        "children": ",".join(children_ids),
                        "caption": text,
                        "access_token": token,
                    }, timeout=30
                )
                if r.status_code == 200:
                    container_id = r.json().get("id")
                    # Publish
                    r2 = requests.post(
                        f"{GRAPH_API}/{ig_id}/media_publish",
                        data={"creation_id": container_id, "access_token": token},
                        timeout=30
                    )
                    if r2.status_code == 200:
                        return {"ok": True, "post_id": r2.json().get("id", ""), "message": "Instagram carousel basarili"}
                    return {"ok": False, "message": f"IG publish hatasi: {r2.text[:200]}"}
            return {"ok": False, "message": "Carousel için gorsel yuklenemedi"}

        # Tek gorsel
        if images:
            fpath = images[0].get("dosya", "")
            image_url = _get_hosted_url(creds, fpath)
            if not image_url:
                return {"ok": False, "message": "Görsel URL'i alınamadı"}
            r = requests.post(
                f"{GRAPH_API}/{ig_id}/media",
                data={"image_url": image_url, "caption": text, "access_token": token},
                timeout=30
            )
            if r.status_code == 200:
                container_id = r.json().get("id")
                # Publish
                r2 = requests.post(
                    f"{GRAPH_API}/{ig_id}/media_publish",
                    data={"creation_id": container_id, "access_token": token},
                    timeout=30
                )
                if r2.status_code == 200:
                    return {"ok": True, "post_id": r2.json().get("id", ""), "message": "Instagram gorsel paylasim basarili"}
                return {"ok": False, "message": f"IG publish hatasi: {r2.text[:200]}"}
            err = r.json().get("error", {}).get("message", r.text)
            return {"ok": False, "message": f"IG container hatasi: {err}"}

        # Video (Reels)
        if videos:
            fpath = videos[0].get("dosya", "")
            video_url = _get_hosted_url(creds, fpath)
            if not video_url:
                return {"ok": False, "message": "Video URL'i alinamadi"}
            r = requests.post(
                f"{GRAPH_API}/{ig_id}/media",
                data={
                    "video_url": video_url,
                    "caption": text,
                    "media_type": "REELS",
                    "access_token": token,
                }, timeout=60
            )
            if r.status_code == 200:
                container_id = r.json().get("id")
                # Video isleme bekleme (polling)
                for _ in range(30):
                    time.sleep(2)
                    check = requests.get(
                        f"{GRAPH_API}/{container_id}",
                        params={"fields": "status_code", "access_token": token}, timeout=10
                    )
                    if check.status_code == 200 and check.json().get("status_code") == "FINISHED":
                        break
                r2 = requests.post(
                    f"{GRAPH_API}/{ig_id}/media_publish",
                    data={"creation_id": container_id, "access_token": token},
                    timeout=30
                )
                if r2.status_code == 200:
                    return {"ok": True, "post_id": r2.json().get("id", ""), "message": "Instagram video paylasim basarili"}
                return {"ok": False, "message": f"IG video publish hatasi: {r2.text[:200]}"}
            err = r.json().get("error", {}).get("message", r.text)
            return {"ok": False, "message": f"IG video container hatasi: {err}"}

        return {"ok": False, "message": "Instagram için medya bulunamadı"}

    # --- LINKEDIN ---
    @staticmethod
    def _publish_linkedin(creds: dict, text: str, media_paths: list) -> dict:
        token = creds.get("access_token", "")
        if not token:
            return {"ok": False, "message": "Access Token gerekli"}

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }

        # Kullanici ID al
        me_r = requests.get(f"{LINKEDIN_API}/me", headers={"Authorization": f"Bearer {token}"}, timeout=10)
        if me_r.status_code != 200:
            return {"ok": False, "message": f"LinkedIn profil alinamadi: {me_r.status_code}"}
        person_id = me_r.json().get("id", "")
        author = f"urn:li:person:{person_id}"

        # Organization ID varsa, org olarak paylas
        org_id = creds.get("page_id", "")
        if org_id:
            author = f"urn:li:organization:{org_id}"

        # Medya yukle
        asset_urns = []
        images = [m for m in media_paths if m.get("tip") == "image"]
        for img in images[:1]:  # LinkedIn tek gorsel destekler (basit paylasim)
            fpath = img.get("dosya", "")
            if not os.path.exists(fpath):
                continue
            # Register upload
            reg_body = {
                "registerUploadRequest": {
                    "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                    "owner": author,
                    "serviceRelationships": [{"relationshipType": "OWNER", "identifier": "urn:li:userGeneratedContent"}],
                }
            }
            reg_r = requests.post(
                f"{LINKEDIN_API}/assets?action=registerUpload",
                headers=headers, json=reg_body, timeout=15
            )
            if reg_r.status_code in (200, 201):
                reg_data = reg_r.json().get("value", {})
                upload_url = reg_data.get("uploadMechanism", {}).get(
                    "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest", {}
                ).get("uploadUrl", "")
                asset_urn = reg_data.get("asset", "")
                if upload_url:
                    with open(fpath, "rb") as f:
                        up_r = requests.put(upload_url, data=f, headers={
                            "Authorization": f"Bearer {token}",
                        }, timeout=60)
                    if up_r.status_code in (200, 201):
                        asset_urns.append(asset_urn)

        # UGC Post olustur
        ugc_body = {
            "author": author,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "IMAGE" if asset_urns else "NONE",
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }

        if asset_urns:
            ugc_body["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [
                {"status": "READY", "media": urn} for urn in asset_urns
            ]

        r = requests.post(f"{LINKEDIN_API}/ugcPosts", headers=headers, json=ugc_body, timeout=30)
        if r.status_code in (200, 201):
            post_id = r.json().get("id", r.headers.get("X-RestLi-Id", ""))
            return {"ok": True, "post_id": post_id, "message": "LinkedIn paylasim basarili"}
        return {"ok": False, "message": f"LinkedIn hatasi: {r.status_code} - {r.text[:200]}"}

    # --- TIKTOK ---
    @staticmethod
    def _publish_tiktok(creds: dict, text: str, media_paths: list) -> dict:
        token = creds.get("access_token", "")
        if not token:
            return {"ok": False, "message": "Access Token gerekli"}

        videos = [m for m in media_paths if m.get("tip") == "video"]
        images = [m for m in media_paths if m.get("tip") == "image"]

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        # TikTok foto post (photo mode)
        if images and not videos:
            image_urls = []
            for img in images[:35]:  # TikTok max 35 gorsel
                fpath = img.get("dosya", "")
                # TikTok için public URL gerekli
                # Lokal dosyalar için uyari ver
                if fpath.startswith("http"):
                    image_urls.append(fpath)
            if not image_urls:
                return {"ok": False, "message": "TikTok için gorsellerin public URL olarak erislebilir olmasi gerekli"}

            body = {
                "post_info": {
                    "title": text[:150],
                    "privacy_level": "PUBLIC_TO_EVERYONE",
                },
                "source_info": {
                    "source": "PULL_FROM_URL",
                    "photo_images": image_urls,
                },
                "post_mode": "DIRECT_POST",
                "media_type": "PHOTO",
            }
            r = requests.post(f"{TIKTOK_API}/post/publish/content/init/", headers=headers, json=body, timeout=30)
            if r.status_code == 200 and r.json().get("error", {}).get("code") == "ok":
                pub_id = r.json().get("data", {}).get("publish_id", "")
                return {"ok": True, "post_id": pub_id, "message": "TikTok foto paylasim basarili"}
            err_msg = r.json().get("error", {}).get("message", r.text)
            return {"ok": False, "message": f"TikTok hatasi: {err_msg}"}

        # TikTok video post
        if videos:
            fpath = videos[0].get("dosya", "")
            if not os.path.exists(fpath):
                return {"ok": False, "message": "Video dosyasi bulunamadı"}

            file_size = os.path.getsize(fpath)

            # Chunk upload init
            body = {
                "post_info": {
                    "title": text[:150],
                    "privacy_level": "PUBLIC_TO_EVERYONE",
                },
                "source_info": {
                    "source": "FILE_UPLOAD",
                    "video_size": file_size,
                    "chunk_size": file_size,
                    "total_chunk_count": 1,
                },
                "post_mode": "DIRECT_POST",
                "media_type": "VIDEO",
            }
            r = requests.post(f"{TIKTOK_API}/post/publish/inbox/video/init/", headers=headers, json=body, timeout=30)
            if r.status_code == 200:
                upload_url = r.json().get("data", {}).get("upload_url", "")
                pub_id = r.json().get("data", {}).get("publish_id", "")
                if upload_url:
                    with open(fpath, "rb") as f:
                        chunk_data = f.read()
                    up_headers = {
                        "Content-Type": "video/mp4",
                        "Content-Range": f"bytes 0-{file_size - 1}/{file_size}",
                    }
                    up_r = requests.put(upload_url, data=chunk_data, headers=up_headers, timeout=120)
                    if up_r.status_code in (200, 201):
                        return {"ok": True, "post_id": pub_id, "message": "TikTok video paylasim basarili"}
                    return {"ok": False, "message": f"TikTok video yukleme hatasi: {up_r.status_code}"}
            err_msg = r.json().get("error", {}).get("message", r.text) if r.text else "Bilinmeyen hata"
            return {"ok": False, "message": f"TikTok init hatasi: {err_msg}"}

        return {"ok": False, "message": "TikTok için video veya gorsel gerekli"}

    # --- YOUTUBE ---
    @staticmethod
    def _publish_youtube(creds: dict, text: str, media_paths: list) -> dict:
        token = creds.get("access_token", "")
        if not token:
            return {"ok": False, "message": "OAuth2 Access Token gerekli"}
        videos = [m for m in media_paths if m.get("tip") == "video"]
        if not videos:
            return {"ok": False, "message": "YouTube için video dosyasi gerekli"}
        fpath = videos[0].get("dosya", "")
        if not os.path.exists(fpath):
            return {"ok": False, "message": "Video dosyasi bulunamadı"}
        title = text[:100] if text else "SmartCampus AI Video"
        meta = json.dumps({
            "snippet": {"title": title, "description": text, "categoryId": "22"},
            "status": {"privacyStatus": "public"},
        })
        headers = {"Authorization": f"Bearer {token}"}
        with open(fpath, "rb") as f:
            r = requests.post(
                f"{YOUTUBE_API}/videos?uploadType=multipart&part=snippet,status",
                headers=headers,
                files={"metadata": ("meta.json", meta, "application/json"), "media": f},
                timeout=120,
            )
        if r.status_code == 200:
            vid_id = r.json().get("id", "")
            return {"ok": True, "post_id": vid_id, "message": f"YouTube video yuklendi: {vid_id}"}
        return {"ok": False, "message": f"YouTube hatasi: {r.status_code} - {r.text[:200]}"}

    # --- X (TWITTER) ---
    @staticmethod
    def _publish_x_twitter(creds: dict, text: str, media_paths: list) -> dict:
        token = creds.get("access_token", "")
        if not token:
            return {"ok": False, "message": "Bearer Token gerekli"}
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        body = {"text": text[:280]}
        r = requests.post(f"{X_API}/tweets", headers=headers, json=body, timeout=15)
        if r.status_code in (200, 201):
            tweet_id = r.json().get("data", {}).get("id", "")
            return {"ok": True, "post_id": tweet_id, "message": f"Tweet paylasildi: {tweet_id}"}
        return {"ok": False, "message": f"X API hatasi: {r.status_code} - {r.text[:200]}"}

    # ---------- ANALYTICS ----------

    @staticmethod
    def get_analytics(platform: str, creds: dict, post_id: str) -> dict:
        """Paylasim analizlerini cek. Returns {"begeni": int, "yorum": int, "paylasim": int, "goruntulenme": int}"""
        try:
            if platform == "facebook":
                return SocialMediaAPI._analytics_facebook(creds, post_id)
            elif platform == "instagram":
                return SocialMediaAPI._analytics_instagram(creds, post_id)
            elif platform == "linkedin":
                return SocialMediaAPI._analytics_linkedin(creds, post_id)
        except Exception:
            pass
        return {"begeni": 0, "yorum": 0, "paylasim": 0, "goruntulenme": 0}

    @staticmethod
    def _analytics_facebook(creds: dict, post_id: str) -> dict:
        token = creds.get("access_token", "")
        r = requests.get(
            f"{GRAPH_API}/{post_id}",
            params={"fields": "likes.summary(true),comments.summary(true),shares", "access_token": token},
            timeout=10
        )
        if r.status_code == 200:
            data = r.json()
            return {
                "begeni": data.get("likes", {}).get("summary", {}).get("total_count", 0),
                "yorum": data.get("comments", {}).get("summary", {}).get("total_count", 0),
                "paylasim": data.get("shares", {}).get("count", 0),
                "goruntulenme": 0,
            }
        return {"begeni": 0, "yorum": 0, "paylasim": 0, "goruntulenme": 0}

    @staticmethod
    def _analytics_instagram(creds: dict, post_id: str) -> dict:
        token = creds.get("access_token", "")
        r = requests.get(
            f"{GRAPH_API}/{post_id}/insights",
            params={"metric": "impressions,reach,likes,comments,shares", "access_token": token},
            timeout=10
        )
        result = {"begeni": 0, "yorum": 0, "paylasim": 0, "goruntulenme": 0}
        if r.status_code == 200:
            for item in r.json().get("data", []):
                name = item.get("name", "")
                val = item.get("values", [{}])[0].get("value", 0)
                if name == "likes":
                    result["begeni"] = val
                elif name == "comments":
                    result["yorum"] = val
                elif name == "shares":
                    result["paylasim"] = val
                elif name == "impressions":
                    result["goruntulenme"] = val
        return result

    @staticmethod
    def _analytics_linkedin(creds: dict, post_id: str) -> dict:
        token = creds.get("access_token", "")
        r = requests.get(
            f"{LINKEDIN_API}/socialActions/{post_id}",
            headers={"Authorization": f"Bearer {token}"}, timeout=10
        )
        if r.status_code == 200:
            data = r.json()
            return {
                "begeni": data.get("likesSummary", {}).get("totalLikes", 0),
                "yorum": data.get("commentsSummary", {}).get("totalFirstLevelComments", 0),
                "paylasim": 0,
                "goruntulenme": 0,
            }
        return {"begeni": 0, "yorum": 0, "paylasim": 0, "goruntulenme": 0}

    # ---------- GELEN KUTUSU (YORUM / MENTION) ----------

    @staticmethod
    def get_comments(platform: str, creds: dict, post_id: str = "") -> list:
        """Yorumlari / mention'lari cek. Returns [{"kullanici": str, "metin": str, "tarih": str}]"""
        try:
            if platform == "facebook":
                return SocialMediaAPI._comments_facebook(creds, post_id)
            elif platform == "instagram":
                return SocialMediaAPI._comments_instagram(creds, post_id)
        except Exception:
            pass
        return []

    @staticmethod
    def _comments_facebook(creds: dict, post_id: str) -> list:
        token = creds.get("access_token", "")
        page_id = creds.get("page_id", "")
        target = post_id or f"{page_id}/feed"
        r = requests.get(
            f"{GRAPH_API}/{target}/comments",
            params={"access_token": token, "fields": "from,message,created_time", "limit": 50},
            timeout=10
        )
        results = []
        if r.status_code == 200:
            for c in r.json().get("data", []):
                results.append({
                    "id": c.get("id", ""),
                    "kullanici": c.get("from", {}).get("name", ""),
                    "metin": c.get("message", ""),
                    "tarih": c.get("created_time", ""),
                    "platform": "facebook",
                    "tip": "yorum",
                })
        return results

    @staticmethod
    def _comments_instagram(creds: dict, post_id: str) -> list:
        token = creds.get("access_token", "")
        ig_id = creds.get("page_id", "")
        # Belirli post veya son medyalar
        if post_id:
            url = f"{GRAPH_API}/{post_id}/comments"
        else:
            # Son medyalarin yorumlari
            media_r = requests.get(
                f"{GRAPH_API}/{ig_id}/media",
                params={"access_token": token, "fields": "id", "limit": 10}, timeout=10
            )
            if media_r.status_code != 200:
                return []
            results = []
            for m in media_r.json().get("data", []):
                comments = SocialMediaAPI._comments_instagram(creds, m["id"])
                results.extend(comments)
            return results[:50]

        r = requests.get(url, params={
            "access_token": token,
            "fields": "from,text,timestamp,username",
            "limit": 50,
        }, timeout=10)
        results = []
        if r.status_code == 200:
            for c in r.json().get("data", []):
                results.append({
                    "id": c.get("id", ""),
                    "kullanici": c.get("username", c.get("from", {}).get("username", "")),
                    "metin": c.get("text", ""),
                    "tarih": c.get("timestamp", ""),
                    "platform": "instagram",
                    "tip": "yorum",
                })
        return results



def _get_hosted_url(creds: dict, local_path: str) -> str:
    """Lokal dosyayi Facebook'a yuklayerek URL al (Instagram için gerekli)."""
    if not os.path.exists(local_path):
        return ""
    token = creds.get("access_token", "")
    page_id = creds.get("page_id", "")
    # Gecici olarak Facebook'a unpublished foto olarak yukle
    try:
        with open(local_path, "rb") as f:
            r = requests.post(
                f"{GRAPH_API}/{page_id}/photos",
                data={"access_token": token, "published": "false", "temporary": "true"},
                files={"source": f}, timeout=60
            )
        if r.status_code == 200:
            photo_id = r.json().get("id", "")
            # Foto URL'ini al
            url_r = requests.get(
                f"{GRAPH_API}/{photo_id}",
                params={"fields": "images", "access_token": token}, timeout=10
            )
            if url_r.status_code == 200:
                imgs = url_r.json().get("images", [])
                if imgs:
                    return imgs[0].get("source", "")
    except Exception:
        pass
    return ""


# ===================== VERI KATMANI =====================

def _smm_dir() -> str:
    return ensure_tenant_dir()


def _load_json(filename: str) -> list:
    path = os.path.join(_smm_dir(), filename)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _save_json(filename: str, data: list) -> None:
    path = os.path.join(_smm_dir(), filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _load_dict_json(filename: str) -> dict:
    path = os.path.join(_smm_dir(), filename)
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _save_dict_json(filename: str, data: dict) -> None:
    path = os.path.join(_smm_dir(), filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# Kisa erisim
def _posts() -> list:
    return _load_json("smm_posts.json")

def _save_posts(data: list):
    _save_json("smm_posts.json", data)

def _accounts() -> list:
    return _load_json("smm_accounts.json")

def _save_accounts(data: list):
    _save_json("smm_accounts.json", data)

def _assets() -> list:
    return _load_json("smm_assets.json")

def _save_assets(data: list):
    _save_json("smm_assets.json", data)

def _settings() -> dict:
    return _load_dict_json("smm_settings.json")

def _save_settings(data: dict):
    _save_dict_json("smm_settings.json", data)

def _inbox() -> list:
    return _load_json("smm_inbox.json")

def _save_inbox(data: list):
    _save_json("smm_inbox.json", data)

def _alerts() -> list:
    return _load_json("smm_alerts.json")

def _save_alerts(data: list):
    _save_json("smm_alerts.json", data)


def _new_id(prefix: str = "smm") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


# ===================== STIL FONKSIYONLARI =====================


def _inject_css():
    inject_common_css("smm")
    st.markdown("""
    <style>
    .block-container {padding-top: 1.5rem !important;}
    [data-testid="stSidebar"] .block-container {padding-top: 1rem !important;}
    div[data-testid="stMarkdownContainer"] p {margin-bottom: 0.4rem;}
    </style>
    """, unsafe_allow_html=True)


def _status_badge(status_key: str) -> str:
    info = STATUS_MAP.get(status_key, {"label": status_key, "color": "#94a3b8"})
    return (f'<span style="background:{info["color"]}20;color:{info["color"]};'
            f'padding:3px 10px;border-radius:20px;font-size:0.75rem;font-weight:600;'
            f'border:1px solid {info["color"]}40">{info["label"]}</span>')


def _platform_badge(platform_key: str) -> str:
    info = PLATFORM_MAP.get(platform_key, {"icon": "🌐", "label": platform_key, "color": "#64748b"})
    return (f'<span style="background:{info["color"]}15;color:{info["color"]};'
            f'padding:3px 10px;border-radius:20px;font-size:0.75rem;font-weight:600;'
            f'border:1px solid {info["color"]}30">{info["icon"]} {info["label"]}</span>')


# ===================== KULLANIM KILAVUZU PDF =====================

def _generate_kullanim_kilavuzu_pdf() -> bytes:
    """Sosyal Medya Yonetimi A'dan Z'ye kullanim kilavuzu PDF."""
    try:
        from utils.report_utils import ReportPDFGenerator
        from utils.shared_data import load_kurum_profili

        kp = load_kurum_profili()
        k_adi = kp.get("kurum_adi", "") or kp.get("name", "Kurum")

        pdf = ReportPDFGenerator(
            "Sosyal Medya Yonetimi - Kullanim Kilavuzu",
            "A'dan Z'ye Tam Rehber"
        )
        pdf.add_header(k_adi)

        # ── GIRIS ──
        pdf.add_section("1. GIRIS VE GENEL BAKIS")
        pdf.add_text(
            "Sosyal Medya Yonetimi (SMM-01) modulu, kurumunuzun tum sosyal medya "
            "hesaplarini tek bir panelden yonetmenizi saglar. Instagram, Facebook, LinkedIn, "
            "TikTok, YouTube, X (Twitter), WhatsApp Business ve E-posta kanallarinizi "
            "entegre ederek icerik olusturma, planlama, onay surecleri, analitik takip ve "
            "raporlama islemlerini merkezi olarak gerceklestirebilirsiniz."
        )
        pdf.add_text(
            "Modul 14 ana sekmeden olusur: Ayarlar, Icerikler, Yeni Paylasim, Onay Kuyrugu, "
            "Takvim, Dashboard, Gelen Kutusu, Uyarilar, AI Asistan, Rakip Analizi, "
            "Hashtag Takibi, Marka Ayarlari, Raporlar ve Entegrasyonlar."
        )
        pdf.add_spacer(0.3)
        pdf.add_text("Desteklenen Platformlar:")
        pdf.add_text(
            "* Instagram (Gorsel/Video/Story/Reels)\n"
            "* Facebook (Sayfa paylasimi/Hikaye)\n"
            "* LinkedIn (Sirket sayfasi/Makale)\n"
            "* TikTok (Video paylasimi)\n"
            "* YouTube (Video/Shorts)\n"
            "* X / Twitter (Tweet/Thread)\n"
            "* WhatsApp Business (Toplu mesaj)\n"
            "* E-posta (Bulten gonderimi)"
        )

        # ── AYARLAR ──
        pdf.add_section("2. AYARLAR (Hesap Yonetimi)")
        pdf.add_text(
            "Ayarlar sekmesi iki ana bolumden olusur: Sistem API Ayarlari ve Platform Hesap Baglama."
        )
        pdf.add_text(
            "2.1 Sistem API Ayarlari (Yonetici):\n"
            "Bu bolum tek seferlik ayarlanir. Her platform icin Developer App kimlik bilgilerini girin. "
            "Facebook/Instagram ayni uygulamayi kullanir.\n"
            "* Facebook/Instagram: App ID + App Secret (developers.facebook.com)\n"
            "* LinkedIn: Client ID + Client Secret (linkedin.com/developers/apps)\n"
            "* TikTok: Client Key + Client Secret (developers.tiktok.com)\n"
            "Redirect URI: https://localhost/callback"
        )
        pdf.add_text(
            "2.2 Calisma Modu Secimi:\n"
            "* Direkt Yayin: Icerikler onay sureci olmadan dogrudan yayinlanir\n"
            "* Onayli Yayin: Her icerik onay kuyuguna duser, yetkili onaylar\n"
            "* Her Ikisi: Yetkiye gore direkt veya onayli yayin secenegi sunulur"
        )
        pdf.add_text(
            "2.3 Platform Hesabi Baglama:\n"
            "Her platform icin 'Kolay Kurulum' sihirbazini kullanin:\n"
            "1. Ilgili platformun sekmesini acin\n"
            "2. 'Bagla' butonuna tiklayin\n"
            "3. Acilan sayfada hesabinizi yetkilendirin\n"
            "4. Donen kodu yapiistirin ve 'Onayla' tiklayin\n"
            "5. Baglanti testi ile dogrulayin\n"
            "Token suresi dolmadan once sistem otomatik uyari uretir."
        )

        # ── ICERIKLER ──
        pdf.add_section("3. ICERIKLER (Medya Kutuphanesi)")
        pdf.add_text(
            "Icerikler sekmesi 4 alt bolumden olusur:"
        )
        pdf.add_text(
            "3.1 Medya Galeri:\n"
            "Gorsel ve video dosyalarinizi yukleyin (PNG, JPG, GIF, MP4, MOV - max 50MB). "
            "Yuklenen dosyalar 4 sutunlu galeri gorunumunde listelenir. "
            "Dosyalari paylasim olustururken kutuphaneden secebilirsiniz."
        )
        pdf.add_text(
            "3.2 Metin Sablonlari:\n"
            "Sik kullanilan paylasim metinlerini sablon olarak kaydedin. "
            "Sablon Adi ve Metni girin, platform secerek kaydedin. "
            "Yeni paylasim olustururken 'Sablondan Yukle' ile otomatik doldurun."
        )
        pdf.add_text(
            "3.3 Hashtag Havuzu:\n"
            "Kurum hashtag'lerinizi merkezi olarak yonetin. "
            "Yeni hashtag eklerken # isareti otomatik eklenir. "
            "Paylasim olustururken havuzdan secim yapabilirsiniz."
        )
        pdf.add_text(
            "3.4 Kampanya Etiketleri:\n"
            "Paylasimlarinizi kategorize edin: Bursluluk, Gezi, Kayit, Duyuru, Basari, "
            "Etkinlik, Mezuniyet, Spor, Kultur vb. "
            "Kampanya bazli performans raporlari olusturabilirsiniz."
        )

        # ── YENI PAYLASIM ──
        pdf.add_section("4. YENI PAYLASIM OLUSTURMA")
        pdf.add_text(
            "Yeni paylasim 6 adimda olusturulur:"
        )
        pdf.add_text(
            "Adim 1 - Platform Secimi: Paylasimi yapacaginiz platformlari secin. "
            "Bagli platformlar oncelikli listelenir. Birden fazla platform secebilirsiniz.\n\n"
            "Adim 2 - Medya Ekleme: 'Dosya Yukle' ile yeni dosya veya "
            "'Kutuphaneden Sec' ile mevcut medyalarinizi ekleyin.\n\n"
            "Adim 3 - Metin Yazma: Paylasim metnini yazin veya sablondan yukleyin. "
            "Platform bazli karakter limitleri otomatik kontrol edilir "
            "(Instagram: 2200, X: 280, LinkedIn: 3000 vb.)\n\n"
            "Adim 4 - Hashtag ve Kampanya: Hashtag havuzundan secin veya "
            "yeni hashtag ekleyin. Kampanya etiketi atayin.\n\n"
            "Adim 5 - Onizleme: Her platform icin ayri onizleme karti goruntulenir.\n\n"
            "Adim 6 - Kaydet/Paylas: Uc seceneginiz var:\n"
            "  * 'Taslak Kaydet' - Daha sonra duzenlemek icin\n"
            "  * 'Direkt Paylas' - Hemen yayinla (direkt yayin modunda)\n"
            "  * 'Onaya Gonder' - Yetkili onayina gonder (onayli modda)"
        )
        pdf.add_text(
            "Platform Ozel Metin: Birden fazla platform sectiyseniz, "
            "her birine farkli metin yazabilirsiniz. Ornegin Instagram icin kisa ve emoji'li, "
            "LinkedIn icin uzun ve resmi metin olusturabilirsiniz."
        )

        # ── ONAY KUYRUGU ──
        pdf.add_section("5. ONAY KUYRUGU")
        pdf.add_text(
            "Onayli yayin modunda, icerikler bu kuyrukta toplanir. "
            "Ust kisimda ozet kartlar gosterilir:\n"
            "* Onay Bekliyor (SUBMITTED)\n"
            "* Incelemede (IN_REVIEW)\n"
            "* Revizyon Istendi (CHANGES_REQUESTED)"
        )
        pdf.add_text(
            "Her icerik icin 3 aksiyon vardir:\n"
            "1. Onayla: Icerik yayina hazir hale gelir (APPROVED)\n"
            "2. Revizyon Iste: Icerik olusturana geri doner, yorum eklenir\n"
            "3. Reddet: Icerik iptal edilir (CANCELED)\n\n"
            "Tum islemler onay gecmisinde (tarih, kisi, islem, yorum) kayit altina alinir."
        )

        # ── TAKVIM ──
        pdf.add_section("6. ICERIK TAKVIMI")
        pdf.add_text(
            "Takvim sekmesi 3 gorunum modu sunar:\n\n"
            "* Aylik Gorunum: Tum ayin takvim grid'inde paylasimlar goruntulenir. "
            "Her gunde kac paylasim oldugu badge ile gosterilir.\n\n"
            "* Haftalik Gorunum: 7 kolonlu haftalik gorunum, her gunde "
            "planlanan/yayinlanan icerikler kart olarak listelenir.\n\n"
            "* Gunluk Gorunum: Secilen gune ait tum iceriklerin detayli listesi."
        )
        pdf.add_text(
            "EN IYI PAYLASIM SAATLERI:\n"
            "Takvim sekmesinin alt kisimda 'En Iyi Paylasim Saatleri' bolumu bulunur. "
            "Sistem, yayinlanmis paylasimlarinizin engagement verilerini analiz ederek "
            "her platform icin en verimli gun ve saat onerisi sunar. "
            "Yeterli veri yoksa sektordeki en iyi pratikler gosterilir.\n"
            "Ornek: Instagram - Sali 11:00, Carsamba 11:00, Persembe 14:00"
        )

        # ── DASHBOARD ──
        pdf.add_section("7. DASHBOARD (Analitik)")
        pdf.add_text(
            "Dashboard sekmesi performansinizi gorsellestirmek icin kullanilir:\n\n"
            "* Genel Metrikler: Toplam begeni, yorum, paylasim ve goruntulenme sayilari\n\n"
            "* Platform Bazli KPI: Her platform icin ayri performans kartlari\n\n"
            "* En Iyi 5 Icerik: En yuksek etkilesim alan 5 paylasim\n\n"
            "* Kampanya Performansi: Bar grafik ile kampanya bazli karsilastirma\n\n"
            "* Platform Dagilimi: Pasta grafik ile platform bazli paylasim orani\n\n"
            "* Zaman Bazli Trend: Cizgi grafik ile gunluk etkilesim trendi\n\n"
            "'Analiz Verilerini Guncelle (API)' butonu ile platformlardan "
            "gercek zamanli veri cekilir."
        )

        # ── GELEN KUTUSU ──
        pdf.add_section("8. GELEN KUTUSU")
        pdf.add_text(
            "Sosyal medya hesaplariniza gelen yorum, etiketleme ve mesajlari "
            "tek panelden takip edin.\n\n"
            "Ozellikler:\n"
            "* Platform, sentiment ve tip bazli filtreleme\n"
            "* Okundu/okunmamis durumu takibi\n"
            "* Dogrudan yanit gonderme\n"
            "* Gorev atama (ekip uyelerine)\n"
            "* Toplu sentiment analizi calistirma\n\n"
            "SENTIMENT ANALIZI:\n"
            "Her mesaj otomatik olarak 'pozitif', 'notr' veya 'negatif' olarak siniflandirilir. "
            "Sistem 54 Turkce anahtar kelime ile kural tabanli analiz yapar. "
            "OpenAI entegrasyonu aktifse GPT-4o-mini ile daha hassas sonuclar alinir."
        )

        # ── UYARILAR ──
        pdf.add_section("9. UYARI MERKEZI")
        pdf.add_text(
            "Sistem otomatik uyarilari olusturur:\n\n"
            "* 48 Saat Paylasim Yok: Son paylasimdan 48+ saat gectiyse uyari\n"
            "* Token Suresi Dolmak Uzere: Platform token'i 7 gun icinde dolacaksa uyari\n"
            "* Token Suresi Doldu: Token gecersiz hale geldiyse hata\n"
            "* Yayin Hatasi: Paylasim yayinlanamadiysa hata\n\n"
            "Uyari seviyeleri: Bilgi (mavi), Uyari (sari), Hata (kirmizi), Basari (yesil)\n"
            "Toplu 'Tumunu Okundu Isaretle' ve 'Gecmisi Temizle' secenekleri mevcuttur."
        )

        # ── AI ASISTAN ──
        pdf.add_section("10. AI ICERIK ASISTANI")
        pdf.add_text(
            "Yapay zeka destekli icerik olusturma araci. OpenAI GPT-4o-mini modeli kullanir.\n\n"
            "10.1 Caption Uretici:\n"
            "Konu, ton (Resmi/Samimi/Enerjik/Bilgilendirici/Ilham Verici), platform, "
            "uzunluk ve emoji tercihi girerek profesyonel caption uretin. "
            "Uretilen metin dogrudan taslak olarak kaydedilebilir.\n\n"
            "10.2 Hashtag Onerici:\n"
            "Paylasim metninizi yapisitirin, istediginiz hashtag sayisini secin (3-15). "
            "AI iceriginize uygun Turkce hashtag'ler onerir.\n\n"
            "10.3 A/B Test Uretici:\n"
            "Ayni konu icin 2 farkli versiyon uretir: Versiyon A (resmi/bilgilendirici) ve "
            "Versiyon B (samimi/enerjik). Hangisinin daha iyi performans gosterecegini test edin.\n\n"
            "10.4 Coklu Dil Cevirisi:\n"
            "Turkce metninizi English, Deutsch, Francais, Espanol ve Arabca'ya cevirin. "
            "Uluslararasi ogrenci/veli kitlesine ulasmak icin idealdir."
        )

        # ── RAKIP ANALIZI ──
        pdf.add_section("11. RAKIP ANALIZI")
        pdf.add_text(
            "Rakip okullarin sosyal medya hesaplarini takip edin ve kiyaslayin.\n\n"
            "Nasil Kullanilir:\n"
            "1. 'Yeni Rakip Ekle' ile kurum adi, platform, hesap URL'si ve kullanici adi girin\n"
            "2. Periyodik olarak metrik girisi yapin: Takipci, Paylasim Sayisi, "
            "Ort. Begeni, Ort. Yorum, Engagement Rate (%)\n"
            "3. Takipci trendi grafigi ile buyumeyi izleyin\n"
            "4. Metrik gecmisi tablosunda tum kayitlari karsilastirin\n\n"
            "Onerilen Takip Sikligi:\n"
            "* Takipci sayisi: Haftalik\n"
            "* Engagement verileri: Aylik\n"
            "* Paylasim analizi: 2 haftada bir"
        )

        # ── HASHTAG TAKIBI ──
        pdf.add_section("12. HASHTAG PERFORMANS TAKIBI")
        pdf.add_text(
            "Kullandiginiz hashtag'lerin performansini analiz edin.\n\n"
            "Gosterilen Metrikler:\n"
            "* Kullanim Sayisi: Hashtag kac paylasimda kullanildi\n"
            "* Toplam Begeni/Yorum/Goruntulenme: Bu hashtag'li paylasimlardan gelen metrikler\n"
            "* Ortalama Etkilesim: (Begeni + Yorum) / Kullanim Sayisi\n"
            "* Platformlar: Hangi platformlarda kullanildigi\n\n"
            "Top 10 Hashtag grafiginde en etkili hashtag'lerinizi gorun. "
            "Dusuk performansli hashtag'leri eleyerek stratejinizi optimize edin."
        )

        # ── MARKA AYARLARI ──
        pdf.add_section("13. MARKA TUTARLILIGI AYARLARI")
        pdf.add_text(
            "Kurumsal marka tutarliligini saglamak icin kurallar tanimlayip kontrol edin.\n\n"
            "Tanimlanan Ayarlar:\n"
            "* Kurum Adi ve Slogan\n"
            "* Birincil ve Ikincil Renk (kurumsal palet)\n"
            "* Logo Dosya Yolu\n"
            "* Zorunlu Hashtag'ler: Her paylasimda bulunmasi gereken hashtag'ler\n"
            "* Yasak Kelimeler: Paylasimda kesinlikle olmamasi gereken kelimeler\n"
            "* Minimum Karakter Sayisi: Paylasim metni alt siniri\n\n"
            "MARKA KONTROL TESTI:\n"
            "Herhangi bir metni yayinlamadan once kontrol edebilirsiniz. "
            "Sistem 100 uzerinden skor verir:\n"
            "* 80+ Yesil: Marka uyumlu\n"
            "* 50-79 Sari: Kismi uyumsuzluk\n"
            "* 50 alti Kirmizi: Ciddi uyumsuzluk\n\n"
            "Kontrol Edilen Kurallar:\n"
            "* Zorunlu hashtag eksikmi? (-20 puan)\n"
            "* Yasak kelime var mi? (-30 puan)\n"
            "* Platform karakter limiti asildi mi? (-15 puan)\n"
            "* Minimum karakter sayisinin altinda mi? (-10 puan)"
        )

        # ── RAPORLAR ──
        pdf.add_section("14. RAPORLAR VE EXPORT")
        pdf.add_text(
            "Performans verilerinizi raporlayin ve disari aktarin.\n\n"
            "14.1 Genel Ozet:\n"
            "Tum yayinlanmis paylasimlarinizin toplam metriklerini, platform dagilimini "
            "ve icerik durum dagilimini goruntuleyin.\n\n"
            "14.2 Donemsel Rapor:\n"
            "Baslangic ve bitis tarihi secerek belirli bir donemin performansini analiz edin. "
            "Gunluk paylasim sayisi grafigi ile trendi takip edin.\n\n"
            "14.3 Export:\n"
            "Verilerinizi 3 formatta disari aktarin:\n"
            "* Excel (.xlsx): Detayli tablo, sutunlar: Tarih, Metin, Platformlar, "
            "Begeni, Yorum, Paylasim, Goruntulenme, Hashtagler, Kampanya\n"
            "* CSV: Hafif format, tum veri programlariyla uyumlu\n"
            "* PDF: Kurumsal baslikli, ozet tablolu profesyonel rapor"
        )

        # ── ENTEGRASYONLAR ──
        pdf.add_section("15. MODUL ENTEGRASYONLARI")
        pdf.add_text(
            "Diger SmartCampus modullerile entegrasyon:\n\n"
            "15.1 Etkinlik -> Paylasim:\n"
            "Kurum Hizmetleri modulundeki etkinlik ve duyurulari otomatik olarak "
            "sosyal medya taslagi haline donusturun. Etkinlik baslik ve aciklamasi "
            "otomatik metin olarak yazilir, platformlari secip 'Taslak Olustur' tiklayin.\n\n"
            "15.2 Halkla Iliskiler:\n"
            "PR modulundeki basin bultenleri ve medya icerikleri buradan "
            "sosyal medya paylasimlarina donusturulur. LinkedIn ve Facebook icin idealdir.\n\n"
            "15.3 Yetki Yonetimi:\n"
            "Kullanici rollerine gore 10 farkli yetki atanabilir:\n"
            "* Hesap Baglama: Platform hesaplarini baglama/ayirma\n"
            "* Icerik Olusturma: Paylasim taslagi olusturma\n"
            "* Direkt Yayin: Onay olmadan yayinlama\n"
            "* Planlama: Icerik zamanlama\n"
            "* Onay: Icerik onaylama/reddetme\n"
            "* Rapor Goruntuleme: Analitik ve rapor erisimi\n"
            "* Gelen Kutusu: Yorum/mesaj yonetimi\n"
            "* AI Asistan: AI araclarini kullanma\n"
            "* Rakip Analizi: Rakip verilerini yonetme\n"
            "* Marka Ayarlari: Marka kurallarini duzenleme\n\n"
            "Admin ve Yonetici rolleri tum yetkilere otomatik sahiptir."
        )

        # ── ICERIK IS AKISI ──
        pdf.add_section("16. ICERIK IS AKISI (WORKFLOW)")
        pdf.add_text(
            "Bir icerigin yasam dongusu 12 asamadan olusur:\n\n"
            "1. TASLAK (DRAFT): Icerik olusturuldu, henuz gonderilmedi\n"
            "2. YAYINA HAZIR (READY_TO_PUBLISH): Duzenleme tamamlandi\n"
            "3. ONAYA GONDERILDI (SUBMITTED): Yetkili onayina sunuldu\n"
            "4. INCELEMEDE (IN_REVIEW): Yetkili inceliyor\n"
            "5. REVIZYON ISTENDI (CHANGES_REQUESTED): Duzenleme gerekiyor\n"
            "6. ONAYLANDI (APPROVED): Yayin icin hazir\n"
            "7. PLANLANDI (SCHEDULED): Belirli tarih/saate zamanlanmis\n"
            "8. YAYINLANIYOR (PUBLISHING): API uzerinden gonderiliyor\n"
            "9. YAYINLANDI (PUBLISHED): Basariyla yayinlandi\n"
            "10. YAYIN HATASI (PUBLISH_FAILED): API hatasi olustu\n"
            "11. MANUEL TAMAMLAMA: Otomatik yayin yapilamiyor, elle tamamlanmali\n"
            "12. IPTAL (CANCELED): Icerik iptal edildi"
        )

        # ── PLATFORM LIMITLERI ──
        pdf.add_section("17. PLATFORM KARAKTER LIMITLERI")
        import pandas as _pd
        limit_rows = [
            {"Platform": "Instagram", "Karakter Limiti": "2.200", "Onerilen": "150-200"},
            {"Platform": "Facebook", "Karakter Limiti": "63.206", "Onerilen": "40-80"},
            {"Platform": "LinkedIn", "Karakter Limiti": "3.000", "Onerilen": "150-300"},
            {"Platform": "TikTok", "Karakter Limiti": "2.200", "Onerilen": "80-150"},
            {"Platform": "YouTube", "Karakter Limiti": "5.000", "Onerilen": "200-500"},
            {"Platform": "X (Twitter)", "Karakter Limiti": "280", "Onerilen": "100-200"},
            {"Platform": "WhatsApp Business", "Karakter Limiti": "4.096", "Onerilen": "100-300"},
            {"Platform": "E-posta", "Karakter Limiti": "Sinirsiz", "Onerilen": "500-1000"},
        ]
        pdf.add_table(_pd.DataFrame(limit_rows))

        # ── SIKCA SORULAN SORULAR ──
        pdf.add_section("18. SIKCA SORULAN SORULAR")
        pdf.add_text(
            "S: Platform hesabimi nasil baglarim?\n"
            "C: Ayarlar > Kolay Kurulum sihirbazini kullanin. Ilgili platformun "
            "sekmesine gidin, 'Bagla' butonuna tiklayin ve acilan sayfada hesabinizi "
            "yetkilendirin.\n"
        )
        pdf.add_text(
            "S: Token suresi doldu uyarisi aliyorum, ne yapmaliyim?\n"
            "C: Ayarlar sekmesinden ilgili platformun baglantisini kesin ve "
            "yeniden baglanin. Token otomatik yenilenir.\n"
        )
        pdf.add_text(
            "S: AI ozellikleri neden calismyor?\n"
            "C: AI ozellikleri OpenAI API anahtari gerektirir. Sistem yoneticinizden "
            "OPENAI_API_KEY ortam degiskeninin tanimlandigini kontrol etmesini isteyin.\n"
        )
        pdf.add_text(
            "S: Paylasimim neden 'Yayin Hatasi' aldi?\n"
            "C: Platform API'si paylasimi reddetti. Olasi nedenler: token suresi dolmus, "
            "dosya formati uyumsuz, karakter limiti asilmis veya platform politikasi ihlali.\n"
        )
        pdf.add_text(
            "S: Birden fazla platforma ayni anda nasil paylasirim?\n"
            "C: Yeni Paylasim sekmesinde birden fazla platform secin. "
            "Her birine ozel metin yazabilir veya ayni metni tum platformlara gonderebilirsiniz.\n"
        )
        pdf.add_text(
            "S: Rakip verileri otomatik cekilebiliyor mu?\n"
            "C: Hayir, rakip metrikleri su an manuel girilir. Ilgili platformlarin "
            "herkese acik verilerini kullanarak duzenli giris yapabilirsiniz.\n"
        )

        # ── VERI DOSYALARI ──
        pdf.add_section("19. TEKNIK BILGI - VERI DOSYALARI")
        pdf.add_text(
            "Modul verileri JSON formatinda saklanir:\n"
            "* smm_posts.json - Paylasimlar (taslak, yayinlanan, planlanan)\n"
            "* smm_accounts.json - Platform hesap baglantilari\n"
            "* smm_assets.json - Medya kutuphanesi kayitlari\n"
            "* smm_inbox.json - Gelen kutusu mesajlari\n"
            "* smm_alerts.json - Sistem uyarilari\n"
            "* smm_rakipler.json - Rakip kurum verileri\n"
            "* smm_hashtag_performans.json - Hashtag analitik verileri\n"
            "* smm_marka.json - Marka tutarlilik ayarlari\n"
            "* smm_settings.json - Genel modul ayarlari (API, sablonlar, havuzlar)\n"
            "* smm_media/ - Yuklenen gorsel ve video dosyalari"
        )

        pdf.add_spacer(0.5)
        pdf.add_text(
            "Bu kilavuz SmartCampus AI - Sosyal Medya Yonetimi (SMM-01) modulu icin "
            "hazirlanmistir. Sorulariniz icin sistem yoneticinize basvurun."
        )

        return pdf.generate()
    except Exception:
        return b""


# ===================== ANA RENDER =====================

def render_sosyal_medya():
    """Sosyal Medya Yonetimi ana ekrani - 14 alt sekme."""

    _inject_css()
    styled_header("Sosyal Medya Yonetimi", subtitle="Tum sosyal medya hesaplarinizi tek panelden yonetin", icon="📱")

    # Kullanim Kilavuzu PDF indirme
    with st.expander("📖 Kullanim Kilavuzu (A'dan Z'ye Rehber)"):
        st.info(
            "Sosyal Medya Yonetimi modulunun tum ozelliklerini iceren kapsamli "
            "kullanim kilavuzunu PDF olarak indirin. 19 bolum, 14 sekme aciklamasi, "
            "platform limitleri tablosu ve SSS bolumu yer almaktadir."
        )
        kilavuz_bytes = _generate_kullanim_kilavuzu_pdf()
        if kilavuz_bytes:
            st.download_button(
                "📄 Kullanim Kilavuzu PDF Indir",
                data=kilavuz_bytes,
                file_name=f"SMM_Kullanim_Kilavuzu_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                key="smm_kilavuz_pdf_dl",
                use_container_width=True,
            )
        else:
            st.warning("PDF olusturulamadi. ReportLab kutuphanesinin kurulu oldugundan emin olun.")

    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("sosyal_medya_egitim_yili")

    # -- Tab Gruplama (25 tab -> 4 grup) --
    _GRP_TABS = {
        "📋 Grup A": [("  ⚙️ Ayarlar  ", 0), ("  📂 Icerikler  ", 1), ("  📝 Yeni Paylasim  ", 2), ("  ✅ Onay Kuyrugu  ", 3), ("  📅 Takvim  ", 4), ("  📊 Dashboard  ", 5), ("  📬 Gelen Kutusu  ", 6)],
        "📊 Grup B": [("  🔔 Uyarilar  ", 7), ("  🤖 AI Asistan  ", 8), ("  🏆 Rakip Analizi  ", 9), ("  📈 Hashtag Takibi  ", 10), ("  🎨 Marka Ayarlari  ", 11), ("  📋 Raporlar  ", 12), ("  🔗 Entegrasyonlar  ", 13)],
        "🔧 Grup C": [("  📖 Kullanim Kilavuzu  ", 14), ("  🎛️ Komuta Merkezi  ", 15), ("  🏭 Icerik Fabrikasi  ", 16), ("  💎 Kampanya ROI  ", 17), ("  🚨 Kriz Yonetim  ", 18), ("  🌟 Veli Elci  ", 19), ("  🧬 Icerik DNA  ", 20)],
        "📈 Grup D": [("  📡 Sosyal Dinleme  ", 21), ("  🤖 Otopilot  ", 22), ("  🧩 Etki Analizi  ", 23), ("  🤖 Smarti  ", 24)],
    }
    _sg_grp_56763 = st.radio("", list(_GRP_TABS.keys()), horizontal=True, label_visibility="collapsed", key="rg_grp_56763")
    _gt_grp_56763 = _GRP_TABS[_sg_grp_56763]
    _tn_grp_56763 = [t[0] for t in _gt_grp_56763]
    _ti_grp_56763 = [t[1] for t in _gt_grp_56763]
    _tabs_grp_56763 = st.tabs(_tn_grp_56763)
    _tmap_grp_56763 = {i: t for i, t in zip(_ti_grp_56763, _tabs_grp_56763)}
    tab1 = _tmap_grp_56763.get(0)
    tab2 = _tmap_grp_56763.get(1)
    tab3 = _tmap_grp_56763.get(2)
    tab4 = _tmap_grp_56763.get(3)
    tab5 = _tmap_grp_56763.get(4)
    tab6 = _tmap_grp_56763.get(5)
    tab7 = _tmap_grp_56763.get(6)
    tab8 = _tmap_grp_56763.get(7)
    tab9 = _tmap_grp_56763.get(8)
    tab10 = _tmap_grp_56763.get(9)
    tab11 = _tmap_grp_56763.get(10)
    tab12 = _tmap_grp_56763.get(11)
    tab13 = _tmap_grp_56763.get(12)
    tab14 = _tmap_grp_56763.get(13)
    tab15 = _tmap_grp_56763.get(14)
    tab16 = _tmap_grp_56763.get(15)
    tab17 = _tmap_grp_56763.get(16)
    tab18 = _tmap_grp_56763.get(17)
    tab19 = _tmap_grp_56763.get(18)
    tab20 = _tmap_grp_56763.get(19)
    tab21 = _tmap_grp_56763.get(20)
    tab22 = _tmap_grp_56763.get(21)
    tab23 = _tmap_grp_56763.get(22)
    tab24 = _tmap_grp_56763.get(23)
    tab_smarti = _tmap_grp_56763.get(24)

    if tab1 is not None:
      with tab1:
        _render_ayarlar()
    if tab2 is not None:
      with tab2:
        _render_icerikler()
    if tab3 is not None:
      with tab3:
        _render_yeni_paylasim()
    if tab4 is not None:
      with tab4:
        _render_onay_kuyrugu()
    if tab5 is not None:
      with tab5:
        _render_takvim_v2()
    if tab6 is not None:
      with tab6:
        _render_dashboard()
    if tab7 is not None:
      with tab7:
        _render_gelen_kutusu_v2()
    if tab8 is not None:
      with tab8:
        _render_uyarilar()
    if tab9 is not None:
      with tab9:
        _render_ai_asistan()
    if tab10 is not None:
      with tab10:
        _render_rakip_analizi()
    if tab11 is not None:
      with tab11:
        _render_hashtag_takibi()
    if tab12 is not None:
      with tab12:
        _render_marka_ayarlari()
    if tab13 is not None:
      with tab13:
        _render_raporlar()
    if tab14 is not None:
      with tab14:
        _render_entegrasyonlar()
    if tab15 is not None:
      with tab15:
        _render_kullanim_kilavuzu()

    # ZIRVE: Sosyal Medya Komuta Merkezi
    if tab16 is not None:
      with tab16:
        try:
            from views._smm_zirve import render_komuta_merkezi
            render_komuta_merkezi()
        except Exception as _e:
            st.error(f"Komuta Merkezi yuklenemedi: {_e}")

    # ZIRVE: AI Icerik Fabrikasi
    if tab17 is not None:
      with tab17:
        try:
            from views._smm_zirve import render_icerik_fabrikasi
            render_icerik_fabrikasi()
        except Exception as _e:
            st.error(f"Icerik Fabrikasi yuklenemedi: {_e}")

    # ZIRVE: Kampanya ROI
    if tab18 is not None:
      with tab18:
        try:
            from views._smm_zirve import render_kampanya_roi
            render_kampanya_roi()
        except Exception as _e:
            st.error(f"Kampanya ROI yuklenemedi: {_e}")

    # SUPER: Kriz Yonetim Merkezi
    if tab19 is not None:
      with tab19:
        try:
            from views._smm_super import render_kriz_yonetim
            render_kriz_yonetim()
        except Exception as _e:
            st.error(f"Kriz Yonetim yuklenemedi: {_e}")

    # SUPER: Veli Elci Programi
    if tab20 is not None:
      with tab20:
        try:
            from views._smm_super import render_veli_elci
            render_veli_elci()
        except Exception as _e:
            st.error(f"Veli Elci yuklenemedi: {_e}")

    # SUPER: Icerik DNA + Akilli Takvim
    if tab21 is not None:
      with tab21:
        try:
            from views._smm_super import render_icerik_dna
            render_icerik_dna()
        except Exception as _e:
            st.error(f"Icerik DNA yuklenemedi: {_e}")

    # MEGA: Sosyal Dinleme Radari
    if tab22 is not None:
      with tab22:
        try:
            from views._smm_mega import render_sosyal_dinleme
            render_sosyal_dinleme()
        except Exception as _e:
            st.error(f"Sosyal Dinleme yuklenemedi: {_e}")

    # MEGA: Otopilot Scheduler
    if tab23 is not None:
      with tab23:
        try:
            from views._smm_mega import render_otopilot
            render_otopilot()
        except Exception as _e:
            st.error(f"Otopilot yuklenemedi: {_e}")

    # MEGA: Cross-Module Impact Tracker
    if tab24 is not None:
      with tab24:
        try:
            from views._smm_mega import render_etki_analizi
            render_etki_analizi()
        except Exception as _e:
            st.error(f"Etki Analizi yuklenemedi: {_e}")

    if tab_smarti is not None:
      with tab_smarti:
        try:
            from views.ai_destek import render_smarti_chat
            render_smarti_chat(modul="sosyal_medya")
        except Exception:
            st.markdown(
                '<div style="background:linear-gradient(135deg,#6366F1,#8B5CF6);color:#fff;'
                'padding:20px;border-radius:12px;text-align:center;margin:20px 0">'
                '<h3 style="margin:0">🤖 Smarti AI</h3>'
                '<p style="margin:8px 0 0;opacity:.85">Smarti AI asistanı bu modülde aktif. '
                'Sorularınızı yazın, AI destekli yanıtlar alın.</p></div>',
                unsafe_allow_html=True)
            user_q = st.text_area("Smarti'ye sorunuzu yazın:", key="smarti_q_sosyal_medya")
            if st.button("Gönder", key="smarti_send_sosyal_medya"):
                if user_q.strip():
                    try:
                        from openai import OpenAI
                        import os
                        api_key = os.environ.get("OPENAI_API_KEY", "")
                        if api_key:
                            client = OpenAI(api_key=api_key)
                            resp = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {"role": "system", "content": "Sen SmartCampus AI'nin Smarti asistanısın. sosyal_medya modülü hakkında Türkçe yardım et."},
                                    {"role": "user", "content": user_q}
                                ],
                                temperature=0.7, max_tokens=500)
                            st.markdown(resp.choices[0].message.content)
                        else:
                            st.warning("API anahtarı tanımlı değil.")
                    except Exception as e:
                        st.error(f"Hata: {e}")


# ===================== 1. AYARLAR (HESAP YONETIMI) =====================

_OAUTH_REDIRECT = "https://localhost/callback"


class OAuthHelper:
    """Platform OAuth akislarini yoneten yardimci sinif."""

    # --- FACEBOOK / INSTAGRAM ---
    @staticmethod
    def fb_auth_url(app_id: str) -> str:
        scopes = (
            "pages_manage_posts,pages_read_engagement,pages_show_list,"
            "instagram_basic,instagram_content_publish,instagram_manage_comments,"
            "instagram_manage_insights"
        )
        return (
            f"https://www.facebook.com/v21.0/dialog/oauth?"
            f"client_id={app_id}&redirect_uri={urllib.parse.quote(_OAUTH_REDIRECT)}"
            f"&scope={scopes}&response_type=code"
        )

    @staticmethod
    def fb_exchange_code(app_id: str, app_secret: str, code: str) -> dict:
        """Facebook auth code -> short-lived token -> long-lived token."""
        # Code -> Short-lived token
        r = requests.get(f"{GRAPH_API}/oauth/access_token", params={
            "client_id": app_id,
            "client_secret": app_secret,
            "redirect_uri": _OAUTH_REDIRECT,
            "code": code,
        }, timeout=15)
        if r.status_code != 200:
            return {"ok": False, "message": f"Token alinamadi: {r.text[:200]}"}
        short_token = r.json().get("access_token", "")

        # Short -> Long-lived token (60 gun)
        r2 = requests.get(f"{GRAPH_API}/oauth/access_token", params={
            "grant_type": "fb_exchange_token",
            "client_id": app_id,
            "client_secret": app_secret,
            "fb_exchange_token": short_token,
        }, timeout=15)
        if r2.status_code != 200:
            return {"ok": False, "message": f"Uzun sureli token alinamadi: {r2.text[:200]}"}
        long_token = r2.json().get("access_token", "")
        expires_in = r2.json().get("expires_in", 5184000)  # ~60 gun
        from datetime import datetime, timedelta
        expires_at = (datetime.now() + timedelta(seconds=expires_in)).strftime("%Y-%m-%d %H:%M:%S")

        return {"ok": True, "token": long_token, "expires_at": expires_at}

    @staticmethod
    def fb_get_pages(token: str) -> list:
        """Kullanicinin yonettigi Facebook sayfalarini listele."""
        r = requests.get(f"{GRAPH_API}/me/accounts", params={
            "access_token": token,
            "fields": "id,name,access_token,instagram_business_account",
        }, timeout=15)
        if r.status_code != 200:
            return []
        return r.json().get("data", [])

    # --- LINKEDIN ---
    @staticmethod
    def linkedin_auth_url(client_id: str) -> str:
        scopes = "w_member_social r_liteprofile"
        return (
            f"https://www.linkedin.com/oauth/v2/authorization?"
            f"response_type=code&client_id={client_id}"
            f"&redirect_uri={urllib.parse.quote(_OAUTH_REDIRECT)}"
            f"&scope={urllib.parse.quote(scopes)}"
        )

    @staticmethod
    def linkedin_exchange_code(client_id: str, client_secret: str, code: str) -> dict:
        r = requests.post("https://www.linkedin.com/oauth/v2/accessToken", data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": _OAUTH_REDIRECT,
            "client_id": client_id,
            "client_secret": client_secret,
        }, timeout=15)
        if r.status_code != 200:
            return {"ok": False, "message": f"LinkedIn token alinamadi: {r.text[:200]}"}
        data = r.json()
        token = data.get("access_token", "")
        expires_in = data.get("expires_in", 5184000)
        expires_at = (datetime.now() + timedelta(seconds=expires_in)).strftime("%Y-%m-%d %H:%M:%S")
        return {"ok": True, "token": token, "expires_at": expires_at}

    # --- TIKTOK ---
    @staticmethod
    def tiktok_auth_url(client_key: str) -> str:
        scopes = "user.info.basic,video.publish,video.upload"
        return (
            f"https://www.tiktok.com/v2/auth/authorize/?"
            f"client_key={client_key}&scope={scopes}"
            f"&response_type=code&redirect_uri={urllib.parse.quote(_OAUTH_REDIRECT)}"
        )

    @staticmethod
    def tiktok_exchange_code(client_key: str, client_secret: str, code: str) -> dict:
        r = requests.post("https://open.tiktokapis.com/v2/oauth/token/", json={
            "client_key": client_key,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": _OAUTH_REDIRECT,
        }, timeout=15)
        if r.status_code != 200:
            return {"ok": False, "message": f"TikTok token alinamadi: {r.text[:200]}"}
        data = r.json()
        if data.get("error"):
            return {"ok": False, "message": data.get("error_description", data.get("error"))}
        token = data.get("access_token", "")
        expires_in = data.get("expires_in", 86400)
        expires_at = (datetime.now() + timedelta(seconds=expires_in)).strftime("%Y-%m-%d %H:%M:%S")
        return {"ok": True, "token": token, "expires_at": expires_at}


def _render_kolay_kurulum():
    """Basitlestirilmis hesap baglama — okul sadece 'Bagla' butonuna tiklar."""
    settings = _settings()
    sys_creds = settings.get("system_api_credentials", {})

    st.markdown("""<div style="background:linear-gradient(135deg,#ffffff 0%,#dbeafe 100%);
    border-radius:14px;padding:18px 24px;margin-bottom:16px;border:1px solid #bae6fd">
    <h4 style="color:#0c4a6e;margin:0">Hesap Baglama</h4>
    <p style="color:#475569;margin:4px 0 0 0;font-size:0.85rem">
    Platform hesaplarinizi baglayin. "Bagla" butonuna tiklayin, acilan sayfada
    hesabinizi yetkilendirin, donen kodu yapisitirin.</p>
    </div>""", unsafe_allow_html=True)

    # Sistem kimlikleri kontrol
    has_fb = sys_creds.get("facebook_app_id") and sys_creds.get("facebook_app_secret")
    has_li = sys_creds.get("linkedin_client_id") and sys_creds.get("linkedin_client_secret")
    has_tt = sys_creds.get("tiktok_client_key") and sys_creds.get("tiktok_client_secret")

    if not (has_fb or has_li or has_tt):
        st.warning(
            "Henuz Sistem API kimlik bilgileri ayarlanmamis. "
            "Yukaridaki **Sistem API Ayarlari** bolumunu acarak platform kimliklerini girin."
        )
        return

    accounts = _accounts()

    wiz1, wiz3, wiz4, wiz5 = st.tabs([
        "📘 Facebook + Instagram", "💼 LinkedIn", "🎵 TikTok", "📋 Durum Özeti"
    ])

    # ==================== FACEBOOK + INSTAGRAM ====================
    with wiz1:
        fb_acc = next((a for a in accounts if a.get("platform") == "facebook" and a.get("status") == "connected"), None)
        ig_acc = next((a for a in accounts if a.get("platform") == "instagram" and a.get("status") == "connected"), None)

        if fb_acc:
            st.success("Facebook hesabi bagli!")
        if ig_acc:
            st.success("Instagram hesabi bagli!")

        if not has_fb:
            st.info("Facebook/Instagram için sistem kimlikleri henuz ayarlanmamis.")
        else:
            st.markdown(
                "Facebook ve Instagram **ayni uygulama** uzerinden calisir. "
                "Tek seferde ikisini de baglayabilirsiniz."
            )

            fb_app_id = sys_creds["facebook_app_id"]
            fb_app_secret = sys_creds["facebook_app_secret"]

            auth_url = OAuthHelper.fb_auth_url(fb_app_id)

            st.markdown("**Adim 1:** Asagidaki butona tiklayin ve Facebook'ta hesabinizi yetkilendirin:")
            st.markdown(
                f'<a href="{auth_url}" target="_blank" style="display:inline-block;background:#1877F2;'
                f'color:#fff;padding:10px 24px;border-radius:8px;text-decoration:none;font-weight:700;'
                f'font-size:0.9rem">Facebook ile Baglan</a>',
                unsafe_allow_html=True
            )

            st.markdown(
                "**Adim 2:** Yetkilendirdikten sonra tarayiciniz `https://localhost/callback?code=XXXX...` "
                "adresine yonlendirilecek. Adres cubugundaki URL'yi veya **code** degerini yapisitirin:"
            )
            fb_code = st.text_input("Yetkilendirme Kodu veya URL", key="wiz_fb_code",
                                    help="URL'nin tamamini veya ?code= sonrasindaki degeri yapisitirin")

            if fb_code and "code=" in fb_code:
                parsed = urllib.parse.urlparse(fb_code)
                params = urllib.parse.parse_qs(parsed.query)
                fb_code = params.get("code", [fb_code])[0]

            if fb_code:
                if st.button("Hesabi Bagla", key="wiz_fb_connect", type="primary"):
                    with st.spinner("Token aliniyor..."):
                        result = OAuthHelper.fb_exchange_code(fb_app_id, fb_app_secret, fb_code)

                    if result["ok"]:
                        long_token = result["token"]
                        expires_at = result["expires_at"]
                        st.success(f"Token alindi! (Gecerlilik: {expires_at})")

                        with st.spinner("Facebook sayfalari yukleniyor..."):
                            pages = OAuthHelper.fb_get_pages(long_token)

                        if pages:
                            st.markdown("**Adim 3:** Sayfa secin:")
                            page_names = [f"{p['name']} (ID: {p['id']})" for p in pages]
                            selected_page = st.selectbox("Facebook Sayfasi", page_names, key="wiz_fb_page_sel")
                            sel_idx = page_names.index(selected_page)
                            page = pages[sel_idx]
                            page_token = page.get("access_token", long_token)
                            page_id = page["id"]

                            _save_oauth_account(accounts, "facebook", {
                                "api_key": fb_app_id,
                                "api_secret": fb_app_secret,
                                "access_token": page_token,
                                "page_id": page_id,
                                "token_expires": expires_at,
                            })
                            st.success(f"Facebook sayfasi '{page['name']}' basariyla baglandi!")

                            ig_account = page.get("instagram_business_account", {})
                            ig_id = ig_account.get("id", "")
                            if ig_id:
                                _save_oauth_account(accounts, "instagram", {
                                    "api_key": fb_app_id,
                                    "api_secret": fb_app_secret,
                                    "access_token": page_token,
                                    "page_id": ig_id,
                                    "token_expires": expires_at,
                                })
                                st.success(f"Instagram Business hesabi da baglandi! (IG ID: {ig_id})")
                            else:
                                st.warning(
                                    "Bu sayfaya bagli Instagram Business hesabi bulunamadı. "
                                    "Instagram'dan Profesyonel Hesaba gecis yapin ve Facebook sayfaniza baglayin."
                                )
                            st.rerun()
                        else:
                            st.warning("Yonettiginiz Facebook sayfasi bulunamadı.")
                    else:
                        st.error(result["message"])

    # ==================== LINKEDIN ====================
    with wiz3:
        li_acc = next((a for a in accounts if a.get("platform") == "linkedin" and a.get("status") == "connected"), None)
        if li_acc:
            st.success("LinkedIn hesabi bagli!")

        if not has_li:
            st.info("LinkedIn için sistem kimlikleri henuz ayarlanmamis.")
        else:
            li_client_id = sys_creds["linkedin_client_id"]
            li_client_secret = sys_creds["linkedin_client_secret"]

            auth_url = OAuthHelper.linkedin_auth_url(li_client_id)

            st.markdown("**Adim 1:** Asagidaki butona tiklayin ve LinkedIn hesabinizi yetkilendirin:")
            st.markdown(
                f'<a href="{auth_url}" target="_blank" style="display:inline-block;background:#0A66C2;'
                f'color:#fff;padding:10px 24px;border-radius:8px;text-decoration:none;font-weight:700;'
                f'font-size:0.9rem">LinkedIn ile Baglan</a>',
                unsafe_allow_html=True
            )

            st.markdown(
                "**Adim 2:** Yetkilendirdikten sonra URL'deki kodu yapisitirin:"
            )
            li_code = st.text_input("Yetkilendirme Kodu veya URL", key="wiz_li_code")

            if li_code and "code=" in li_code:
                parsed = urllib.parse.urlparse(li_code)
                params = urllib.parse.parse_qs(parsed.query)
                li_code = params.get("code", [li_code])[0]

            if li_code:
                li_org_id = st.text_input(
                    "Organization ID (sirket sayfasi icin, kisisel için bos birakin)",
                    key="wiz_li_org_id"
                )

                if st.button("Hesabi Bagla", key="wiz_li_connect", type="primary"):
                    with st.spinner("LinkedIn token aliniyor..."):
                        result = OAuthHelper.linkedin_exchange_code(li_client_id, li_client_secret, li_code)

                    if result["ok"]:
                        _save_oauth_account(accounts, "linkedin", {
                            "api_key": li_client_id,
                            "api_secret": li_client_secret,
                            "access_token": result["token"],
                            "page_id": li_org_id,
                            "token_expires": result["expires_at"],
                        })
                        st.success(f"LinkedIn baglandi! Token gecerliligi: {result['expires_at']}")
                        st.rerun()
                    else:
                        st.error(result["message"])

    # ==================== TIKTOK ====================
    with wiz4:
        tt_acc = next((a for a in accounts if a.get("platform") == "tiktok" and a.get("status") == "connected"), None)
        if tt_acc:
            st.success("TikTok hesabi bagli!")

        if not has_tt:
            st.info("TikTok için sistem kimlikleri henuz ayarlanmamis.")
        else:
            tt_client_key = sys_creds["tiktok_client_key"]
            tt_client_secret = sys_creds["tiktok_client_secret"]

            auth_url = OAuthHelper.tiktok_auth_url(tt_client_key)

            st.markdown("**Adim 1:** Asagidaki butona tiklayin ve TikTok hesabinizi yetkilendirin:")
            st.markdown(
                f'<a href="{auth_url}" target="_blank" style="display:inline-block;background:#000;'
                f'color:#fff;padding:10px 24px;border-radius:8px;text-decoration:none;font-weight:700;'
                f'font-size:0.9rem">TikTok ile Baglan</a>',
                unsafe_allow_html=True
            )

            st.markdown(
                "**Adim 2:** Yetkilendirdikten sonra URL'deki kodu yapisitirin:"
            )
            tt_code = st.text_input("Yetkilendirme Kodu veya URL", key="wiz_tt_code")

            if tt_code and "code=" in tt_code:
                parsed = urllib.parse.urlparse(tt_code)
                params = urllib.parse.parse_qs(parsed.query)
                tt_code = params.get("code", [tt_code])[0]

            if tt_code:
                if st.button("Hesabi Bagla", key="wiz_tt_connect", type="primary"):
                    with st.spinner("TikTok token aliniyor..."):
                        result = OAuthHelper.tiktok_exchange_code(tt_client_key, tt_client_secret, tt_code)

                    if result["ok"]:
                        _save_oauth_account(accounts, "tiktok", {
                            "api_key": tt_client_key,
                            "api_secret": tt_client_secret,
                            "access_token": result["token"],
                            "page_id": "",
                            "token_expires": result["expires_at"],
                        })
                        st.success(f"TikTok baglandi! Token gecerliligi: {result['expires_at']}")
                        st.rerun()
                    else:
                        st.error(result["message"])

    # ==================== DURUM OZETI ====================
    with wiz5:
        st.markdown("#### Platform Baglanti Durumu")
        accounts = _accounts()
        for plat_key, plat_icon, plat_label, plat_color in PLATFORMLAR:
            acc = next((a for a in accounts if a.get("platform") == plat_key), None)
            is_connected = acc and acc.get("status") == "connected"
            if is_connected:
                token_exp = acc.get("token_expires", "")
                exp_info = f" — Token: {token_exp}" if token_exp else ""
                st.markdown(
                    f"""<div style="background:#22c55e10;border:1px solid #22c55e40;
                    border-radius:12px;padding:12px 16px;margin-bottom:8px;
                    display:flex;justify-content:space-between;align-items:center">
                    <div><span style="font-size:1.2rem">{plat_icon}</span>
                    <span style="font-weight:700;color:#0B0F19;margin-left:8px">{plat_label}</span></div>
                    <div><span style="background:#22c55e;color:#fff;padding:4px 12px;border-radius:20px;
                    font-size:0.78rem;font-weight:600">Bagli</span>
                    <span style="font-size:0.72rem;color:#64748b;margin-left:8px">{exp_info}</span></div>
                    </div>""", unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""<div style="background:#ef444410;border:1px solid #ef444440;
                    border-radius:12px;padding:12px 16px;margin-bottom:8px;
                    display:flex;justify-content:space-between;align-items:center">
                    <div><span style="font-size:1.2rem">{plat_icon}</span>
                    <span style="font-weight:700;color:#0B0F19;margin-left:8px">{plat_label}</span></div>
                    <span style="background:#ef4444;color:#fff;padding:4px 12px;border-radius:20px;
                    font-size:0.78rem;font-weight:600">Bagli Degil</span>
                    </div>""", unsafe_allow_html=True
                )

        connected_accs = [a for a in accounts if a.get("status") == "connected"]
        if connected_accs:
            st.markdown("---")
            if st.button("Tüm Baglantilari Test Et", key="wiz_test_all", type="primary"):
                for acc in connected_accs:
                    plat_key = acc.get("platform", "")
                    plat_label = PLATFORM_MAP.get(plat_key, {}).get("label", plat_key)
                    plat_icon = PLATFORM_MAP.get(plat_key, {}).get("icon", "")
                    creds = {k: acc.get(k, "") for k in
                             ["api_key", "api_secret", "access_token", "page_id"]}
                    with st.spinner(f"{plat_icon} {plat_label} test ediliyor..."):
                        result = SocialMediaAPI.test_connection(plat_key, creds)
                    if result["ok"]:
                        st.success(f"{plat_icon} {plat_label}: {result['message']}")
                    else:
                        st.error(f"{plat_icon} {plat_label}: {result['message']}")


def _save_oauth_account(accounts: list, platform: str, creds: dict):
    """OAuth ile alinan bilgileri accounts.json'a kaydet."""
    new_acc = {
        "id": next((a["id"] for a in accounts if a.get("platform") == platform), _new_id("acc")),
        "platform": platform,
        "api_key": creds.get("api_key", ""),
        "api_secret": creds.get("api_secret", ""),
        "access_token": creds.get("access_token", ""),

        "page_id": creds.get("page_id", ""),
        "status": "connected",
        "token_expires": creds.get("token_expires", ""),
        "updated_at": _now(),
    }
    found = False
    for i, a in enumerate(accounts):
        if a.get("platform") == platform:
            accounts[i] = new_acc
            found = True
            break
    if not found:
        accounts.append(new_acc)
    _save_accounts(accounts)


def _render_ayarlar():
    styled_section("Platform Hesap Yönetimi", "#2563eb")

    settings = _settings()
    accounts = _accounts()

    # ---- Sistem API Ayarlari (global, tek seferlik) ----
    sys_creds = settings.get("system_api_credentials", {})

    with st.expander("Sistem API Ayarlari (Yonetici)", expanded=not sys_creds):
        st.markdown("""<div style="background:#fef3c7;border-left:4px solid #f59e0b;
        padding:12px 16px;border-radius:0 8px 8px 0;margin-bottom:12px;font-size:0.85rem">
        <strong>Bu alan tek seferlik ayarlanir.</strong> Her platform için Developer App kimlik bilgilerini
        girin. Okullar bu bilgileri gormez — sadece "Bagla" butonuyla hesaplarini yetkilendirir.
        </div>""", unsafe_allow_html=True)

        _SYS_FIELDS = {
            "facebook": {"id_label": "Facebook App ID", "secret_label": "Facebook App Secret",
                         "help": "developers.facebook.com → Uygulama Oluştur → Business"},
            "instagram": {"same_as": "facebook"},
            "linkedin": {"id_label": "LinkedIn Client ID", "secret_label": "LinkedIn Client Secret",
                         "help": "linkedin.com/developers/apps → Uygulama Oluştur"},
            "tiktok": {"id_label": "TikTok Client Key", "secret_label": "TikTok Client Secret",
                       "help": "developers.tiktok.com → Manage Apps → Uygulama Oluştur"},
        }

        st.markdown("**Facebook & Instagram** *(ayni uygulama kullanilir)*")
        st.caption("developers.facebook.com → Uygulama Oluştur → Business")
        s1, s2 = st.columns(2)
        with s1:
            fb_sys_id = st.text_input("App ID", value=sys_creds.get("facebook_app_id", ""),
                                      key="sys_fb_app_id", type="password")
        with s2:
            fb_sys_secret = st.text_input("App Secret", value=sys_creds.get("facebook_app_secret", ""),
                                          key="sys_fb_app_secret", type="password")

        st.markdown("---")
        st.markdown("**LinkedIn**")
        st.caption("linkedin.com/developers/apps → Uygulama Oluştur")
        s3, s4 = st.columns(2)
        with s3:
            li_sys_id = st.text_input("Client ID", value=sys_creds.get("linkedin_client_id", ""),
                                      key="sys_li_client_id", type="password")
        with s4:
            li_sys_secret = st.text_input("Client Secret", value=sys_creds.get("linkedin_client_secret", ""),
                                          key="sys_li_client_secret", type="password")

        st.markdown("---")
        st.markdown("**TikTok**")
        st.caption("developers.tiktok.com → Manage Apps → Content Posting API izni ekleyin")
        s5, s6 = st.columns(2)
        with s5:
            tt_sys_id = st.text_input("Client Key", value=sys_creds.get("tiktok_client_key", ""),
                                      key="sys_tt_client_key", type="password")
        with s6:
            tt_sys_secret = st.text_input("Client Secret", value=sys_creds.get("tiktok_client_secret", ""),
                                          key="sys_tt_client_secret", type="password")

        st.markdown("---")
        st.caption(f"Tüm platformlar için Redirect URI: `{_OAUTH_REDIRECT}`")

        if st.button("Sistem Kimlik Bilgilerini Kaydet", key="sys_save_api_creds", type="primary"):
            settings["system_api_credentials"] = {
                "facebook_app_id": fb_sys_id,
                "facebook_app_secret": fb_sys_secret,
                "linkedin_client_id": li_sys_id,
                "linkedin_client_secret": li_sys_secret,
                "tiktok_client_key": tt_sys_id,
                "tiktok_client_secret": tt_sys_secret,
            }
            _save_settings(settings)
            st.success("Sistem API kimlik bilgileri kaydedildi!")
            st.rerun()

    st.markdown("")

    # Kolay Kurulum / Manuel secimi
    ayar_mode = st.radio(
        "Mod", ["Kolay Kurulum", "Manuel Ayarlar"],
        horizontal=True, key="smm_ayar_mode", label_visibility="collapsed"
    )

    if ayar_mode == "Kolay Kurulum":
        _render_kolay_kurulum()
        return

    # Calisma modu
    col_mod1, col_mod2 = st.columns([2, 3])
    with col_mod1:
        current_mod = settings.get("calisma_modu", "her_ikisi")
        mod_options = ["direkt", "onayli", "her_ikisi"]
        mod_labels = {"direkt": "Direkt Yayin", "onayli": "Onayli Yayin", "her_ikisi": "Her Ikisi"}
        selected_mod = st.selectbox(
            "Calisma Modu",
            mod_options,
            index=mod_options.index(current_mod) if current_mod in mod_options else 2,
            format_func=lambda x: mod_labels.get(x, x),
            key="smm_calisma_modu"
        )
        if selected_mod != current_mod:
            settings["calisma_modu"] = selected_mod
            _save_settings(settings)
            st.success("Calisma modu güncellendi.")

    st.markdown("---")

    # Platform listesi
    for plat_key, plat_icon, plat_label, plat_color in PLATFORMLAR:
        acc = next((a for a in accounts if a.get("platform") == plat_key), None)
        is_connected = acc and acc.get("status") == "connected"

        with st.expander(f"{plat_icon} {plat_label} — {'Bagli' if is_connected else 'Bagli Degil'}", expanded=False
        ):
            c1, c2 = st.columns([3, 1])
            with c1:
                # Durum gostergesi
                if is_connected:
                    token_exp = acc.get("token_expires", "")
                    if token_exp:
                        try:
                            exp_dt = datetime.strptime(token_exp, "%Y-%m-%d %H:%M:%S")
                            days_left = (exp_dt - datetime.now()).days
                            if days_left < 0:
                                st.error(f"Token suresi dolmus! ({token_exp})")
                            elif days_left < 7:
                                st.warning(f"Token suresi dolmak uzere: {days_left} gun kaldi")
                            else:
                                st.success(f"Token gecerli — {days_left} gun kaldi")
                        except Exception:
                            st.info(f"Token durumu: {token_exp}")
                    else:
                        st.success("Baglanti aktif")
                else:
                    st.info("Henuz baglanmadi")

            with c2:
                if is_connected:
                    st.markdown(f"""<div style="background:#22c55e20;color:#22c55e;
                    padding:8px 12px;border-radius:10px;text-align:center;
                    font-weight:700;font-size:0.85rem">Bagli</div>""",
                    unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div style="background:#ef444420;color:#ef4444;
                    padding:8px 12px;border-radius:10px;text-align:center;
                    font-weight:700;font-size:0.85rem">Bagli Degil</div>""",
                    unsafe_allow_html=True)

            # Platform bazli alan aciklamalari
            _FIELD_HELP = {
                "facebook": {"page_id": "Facebook Sayfa ID (Page ID)", "token": "Page Access Token (uzun sureli)"},
                "instagram": {"page_id": "Instagram Business Account ID (IG User ID)", "token": "Facebook Page Access Token"},
                "linkedin": {"page_id": "Organization ID (opsiyonel, kisisel için bos)", "token": "OAuth 2.0 Bearer Token"},
                "tiktok": {"page_id": "Kullanilmiyor (bos birakin)", "token": "OAuth 2.0 Access Token"},
                "youtube": {"page_id": "YouTube Kanal ID (opsiyonel)", "token": "OAuth 2.0 Access Token", "api_key": "Google API Key", "api_secret": "Google Client Secret"},
                "x_twitter": {"page_id": "Kullanilmiyor (bos birakin)", "token": "OAuth 2.0 Bearer Token", "api_key": "API Key (Consumer Key)", "api_secret": "API Secret (Consumer Secret)"},
                "whatsapp_business": {"page_id": "Phone Number ID", "token": "Permanent Access Token", "api_key": "WhatsApp Business Account ID", "api_secret": "Kullanilmiyor (bos birakin)"},
                "email": {"page_id": "E-posta Adresi (orn: okul@gmail.com)", "token": "SMTP Sifre (App Password)", "api_key": "SMTP Host (orn: smtp.gmail.com)", "api_secret": "SMTP Port (orn: 587)"},
            }
            helps = _FIELD_HELP.get(plat_key, {})

            # Platform bazli yardim metni
            _PLATFORM_GUIDE = {
                "facebook": (
                    "**Facebook API bilgilerini almak icin:**\n"
                    "1. [developers.facebook.com](https://developers.facebook.com) adresine gidin\n"
                    "2. 'Uygulamalarim' > 'Uygulama Oluştur' tiklayin\n"
                    "3. 'Isletme' turunu secin > Uygulama adini girin\n"
                    "4. Ayarlar > Temel bolumund en **App ID** ve **App Secret** gorunur\n"
                    "5. Facebook Login ekleyin > Sayfaniz için token alin\n"
                    "6. Sayfa ID: Facebook sayfaniz > Hakkinda > Sayfa ID"
                ),
                "instagram": (
                    "**Instagram API bilgilerini almak icin:**\n"
                    "1. Instagram hesabinizi **Profesyonel Hesap** yapin (Ayarlar > Hesap)\n"
                    "2. Hesabi bir **Facebook Sayfasina** baglayin\n"
                    "3. [developers.facebook.com](https://developers.facebook.com) > Graph API Explorer\n"
                    "4. `pages_show_list`, `instagram_basic`, `instagram_content_publish` izinlerini secin\n"
                    "5. Token olusturun > Sayfanizi secin > IG User ID otomatik gelir\n"
                    "6. Token'i uzun sureli yapmak için Token Debugger kullanin"
                ),
                "linkedin": (
                    "**LinkedIn API bilgilerini almak icin:**\n"
                    "1. [linkedin.com/developers](https://www.linkedin.com/developers/) adresine gidin\n"
                    "2. 'Uygulama Oluştur' tiklayin > Sirket sayfanizi secin\n"
                    "3. Auth sekmesinden **Client ID** ve **Client Secret** alin\n"
                    "4. OAuth 2.0 ile Bearer Token olusturun\n"
                    "5. Organization ID: Sirket sayfasi URL'sindeki numara (linkedin.com/company/12345)"
                ),
                "tiktok": (
                    "**TikTok API bilgilerini almak icin:**\n"
                    "1. [developers.tiktok.com](https://developers.tiktok.com) adresine gidin\n"
                    "2. 'Uygulama Yonet' > Yeni uygulama olusturun\n"
                    "3. 'Content Posting API' erisimi isteyin\n"
                    "4. Onay sonrasi **Client Key** ve **Client Secret** alin\n"
                    "5. OAuth akisiyla Access Token olusturun"
                ),
                "youtube": (
                    "**YouTube API bilgilerini almak icin:**\n"
                    "1. [console.cloud.google.com](https://console.cloud.google.com) adresine gidin\n"
                    "2. Yeni proje olusturun > API'ler ve Hizmetler > Kitaplik\n"
                    "3. 'YouTube Data API v3' etkinlestirin\n"
                    "4. Kimlik Bilgileri > OAuth 2.0 Istemci Kimligi olusturun\n"
                    "5. **Client ID** (API Key) ve **Client Secret** burada gorunur\n"
                    "6. OAuth Consent Screen'i yapilandirin > Access Token alin\n"
                    "7. Kanal ID: YouTube > Kanaliniz > Ayarlar > Gelismis Ayarlar"
                ),
                "x_twitter": (
                    "**X (Twitter) API bilgilerini almak icin:**\n"
                    "1. [developer.x.com](https://developer.x.com) adresine gidin\n"
                    "2. Developer Portal > Projeler ve Uygulamalar > Yeni Uygulama\n"
                    "3. 'Keys and Tokens' sekmesinden:\n"
                    "   - **API Key** (Consumer Key)\n"
                    "   - **API Secret** (Consumer Secret)\n"
                    "   - **Bearer Token** (Access Token olarak girin)\n"
                    "4. Free plan: Ayda 1.500 tweet okuma, 500 tweet yazma"
                ),
                "whatsapp_business": (
                    "**WhatsApp Business API bilgilerini almak icin:**\n"
                    "1. [business.facebook.com](https://business.facebook.com) > WhatsApp Manager\n"
                    "2. Meta Business Suite'te WhatsApp Business hesabi olusturun\n"
                    "3. [developers.facebook.com](https://developers.facebook.com) > WhatsApp eklentisi\n"
                    "4. API Kurulumu sayfasindan:\n"
                    "   - **Phone Number ID** (Sayfa/Hesap ID olarak girin)\n"
                    "   - **Permanent Access Token** (System User uzerinden)\n"
                    "   - **WhatsApp Business Account ID** (API Key olarak girin)\n"
                    "5. Not: Meta Business dogrulama sureci gereklidir"
                ),
                "email": (
                    "**E-posta (SMTP) bilgilerini almak icin:**\n\n"
                    "**Gmail:** smtp.gmail.com / Port: 587\n"
                    "- Google Hesap > Guvenlik > 2 Adimli Dogrulama acin\n"
                    "- Uygulama Sifreleri > Yeni sifre olusturun > SMTP Sifre olarak girin\n\n"
                    "**Outlook/Hotmail:** smtp-mail.outlook.com / Port: 587\n"
                    "- Normal hesap sifrenizi kullanin\n\n"
                    "**Yandex:** smtp.yandex.com / Port: 587\n"
                    "- Ayarlar > Guvenlik > Uygulama Sifresi olusturun\n\n"
                    "**Kurumsal:** IT biriminizden SMTP bilgilerini isteyin"
                ),
            }
            guide = _PLATFORM_GUIDE.get(plat_key)
            if guide:
                with st.expander("Bu bilgileri nereden alabilirim?", expanded=False):
                    st.markdown(guide)

            # API Key / Secret / Token alanlari
            api_key = st.text_input(
                helps.get("api_key", "API Key"),
                value=acc.get("api_key", "") if acc else "",
                type="password", key=f"smm_api_{plat_key}"
            )
            api_secret = st.text_input(
                helps.get("api_secret", "API Secret"),
                value=acc.get("api_secret", "") if acc else "",
                type="password", key=f"smm_secret_{plat_key}"
            )
            access_token = st.text_input(
                helps.get("token", "Access Token"),
                value=acc.get("access_token", "") if acc else "",
                type="password", key=f"smm_token_{plat_key}"
            )
            page_id = st.text_input(
                helps.get("page_id", "Sayfa/Hesap ID"),
                value=acc.get("page_id", "") if acc else "",
                key=f"smm_pageid_{plat_key}"
            )

            bc1, bc2, bc3 = st.columns(3)
            with bc1:
                if st.button("Kaydet", key=f"smm_save_{plat_key}", type="primary"):
                    new_acc = {
                        "id": acc["id"] if acc else _new_id("acc"),
                        "platform": plat_key,
                        "api_key": api_key,
                        "api_secret": api_secret,
                        "access_token": access_token,
                        "page_id": page_id,
                        "status": "connected" if access_token else "disconnected",
                        "token_expires": acc.get("token_expires", "") if acc else "",
                        "updated_at": _now(),
                    }
                    # Guncelle veya ekle
                    found = False
                    for i, a in enumerate(accounts):
                        if a.get("platform") == plat_key:
                            accounts[i] = new_acc
                            found = True
                            break
                    if not found:
                        accounts.append(new_acc)
                    _save_accounts(accounts)
                    st.success(f"{plat_label} bilgileri kaydedildi.")
                    st.rerun()

            with bc2:
                if st.button("Baglanti Testi", key=f"smm_test_{plat_key}"):
                    if access_token:
                        with st.spinner(f"{plat_label} API baglantisi test ediliyor..."):
                            creds = {
                                "api_key": api_key, "api_secret": api_secret,
                                "access_token": access_token,
                                "page_id": page_id,
                            }
                            result = SocialMediaAPI.test_connection(plat_key, creds)
                        if result["ok"]:
                            st.success(f"Başarılı! {result['message']}")
                        else:
                            st.error(f"Hata: {result['message']}")
                    else:
                        st.warning("Lutfen once Access Token giriniz.")

            with bc3:
                if is_connected:
                    if st.button("Baglantıyı Kes", key=f"smm_disconnect_{plat_key}"):
                        for i, a in enumerate(accounts):
                            if a.get("platform") == plat_key:
                                accounts[i]["status"] = "disconnected"
                                accounts[i]["access_token"] = ""
                                break
                        _save_accounts(accounts)
                        st.warning(f"{plat_label} baglantisi kesildi.")
                        st.rerun()

    # Yetki atama
    st.markdown("---")
    styled_section("Yetki Atamalari", "#8b5cf6")

    yetki_data = settings.get("yetkiler", {})

    with st.expander("Kullanıcı Yetkileri Düzenle"):
        st.caption("Kullanıcı adi girin ve yetkilerini secin.")
        yetki_user = st.text_input("Kullanıcı Adi", key="smm_yetki_user")
        if yetki_user:
            user_perms = yetki_data.get(yetki_user, [])
            new_perms = []
            cols = st.columns(4)
            for idx, (perm_key, perm_label) in enumerate(SMM_YETKILER):
                with cols[idx % 4]:
                    if st.checkbox(perm_label, value=perm_key in user_perms, key=f"smm_perm_{perm_key}"):
                        new_perms.append(perm_key)

            if st.button("Yetkileri Kaydet", key="smm_save_perms", type="primary"):
                yetki_data[yetki_user] = new_perms
                settings["yetkiler"] = yetki_data
                _save_settings(settings)
                st.success(f"{yetki_user} yetkileri güncellendi.")

    # Mevcut yetkiler tablosu
    if yetki_data:
        st.markdown("**Mevcut Yetki Atamalari:**")
        for user, perms in yetki_data.items():
            perm_labels = [dict(SMM_YETKILER).get(p, p) for p in perms]
            st.markdown(f"- **{user}**: {', '.join(perm_labels) if perm_labels else 'Yetki yok'}")


# ===================== 2. ICERIKLER (ASSET LIBRARY) =====================

def _render_icerikler():
    styled_section("İçerik Kutuphanesi", "#8b5cf6")

    assets = _assets()
    settings = _settings()

    sub_ic1, sub_ic2, sub_ic3, sub_ic4 = st.tabs([
        "🖼️ Medya Galeri", "📄 Metin Şablonları", "#️⃣ Hashtag Havuzu", "🏷️ Kampanya Etiketleri"
    ])

    # --- Medya Galeri ---
    with sub_ic1:
        st.markdown("##### Görsel ve Video Yükleme")
        uploaded = st.file_uploader(
            "Dosya Yukle", type=["png", "jpg", "jpeg", "gif", "mp4", "mov"],
            accept_multiple_files=True, key="smm_media_upload"
        )
        if uploaded:
            from utils.security import validate_upload
            _valid_media = []
            for uf in uploaded:
                _ok, _msg = validate_upload(uf, allowed_types=["png", "jpg", "jpeg", "gif", "mp4", "mov"], max_mb=50)
                if _ok:
                    _valid_media.append(uf)
                else:
                    st.warning(f"⚠️ {uf.name}: {_msg}")
            uploaded = _valid_media
        if uploaded:
            for uf in uploaded:
                media_dir = os.path.join(_smm_dir(), "smm_media")
                os.makedirs(media_dir, exist_ok=True)
                fname = f"{_new_id('med')}_{uf.name}"
                fpath = os.path.join(media_dir, fname)
                with open(fpath, "wb") as f:
                    f.write(uf.getvalue())
                asset_rec = {
                    "id": _new_id("asset"),
                    "tip": "image" if uf.type and uf.type.startswith("image") else "video",
                    "dosya": fpath,
                    "orijinal_ad": uf.name,
                    "boyut": uf.size,
                    "created_at": _now(),
                }
                assets.append(asset_rec)
            _save_assets(assets)
            st.success(f"{len(uploaded)} dosya yuklendi.")
            st.rerun()

        # Galeri gorunumu
        media_assets = [a for a in assets if a.get("tip") in ("image", "video")]
        if media_assets:
            st.markdown(f"**Toplam: {len(media_assets)} medya dosyasi**")
            cols = st.columns(4)
            for idx, asset in enumerate(media_assets[-20:]):  # son 20
                with cols[idx % 4]:
                    if asset.get("tip") == "image" and os.path.exists(asset.get("dosya", "")):
                        st.image(asset["dosya"], caption=asset.get("orijinal_ad", ""), use_container_width=True)
                    else:
                        st.markdown(f"""<div style="background:#1A2035;border-radius:10px;
                        padding:20px;text-align:center;margin-bottom:8px">
                        <span style="font-size:2rem">🎬</span><br>
                        <span style="font-size:0.75rem;color:#64748b">{asset.get('orijinal_ad', 'Video')}</span>
                        </div>""", unsafe_allow_html=True)
                    if st.button("Sil", key=f"smm_del_asset_{asset['id']}"):
                        assets = [a for a in assets if a["id"] != asset["id"]]
                        _save_assets(assets)
                        st.rerun()
        else:
            st.info("Henuz medya yuklenmedi.")

    # --- Metin Şablonları ---
    with sub_ic2:
        st.markdown("##### Metin Şablonları")
        sablonlar = settings.get("metin_sablonlari", [])

        with st.expander("Yeni Sablon Ekle"):
            s_ad = st.text_input("Sablon Adi", key="smm_sablon_ad")
            s_metin = st.text_area("Sablon Metni", key="smm_sablon_metin", height=100)
            s_platform = st.multiselect("Platform", [p[2] for p in PLATFORMLAR], key="smm_sablon_plat")
            if st.button("Sablon Kaydet", key="smm_save_sablon", type="primary"):
                if s_ad and s_metin:
                    sablonlar.append({
                        "id": _new_id("sab"),
                        "ad": s_ad,
                        "metin": s_metin,
                        "platformlar": s_platform,
                        "created_at": _now(),
                    })
                    settings["metin_sablonlari"] = sablonlar
                    _save_settings(settings)
                    st.success("Sablon kaydedildi.")
                    st.rerun()
                else:
                    st.warning("Ad ve metin zorunludur.")

        if sablonlar:
            for sab in sablonlar:
                col_s1, col_s2 = st.columns([4, 1])
                with col_s1:
                    st.markdown(f"**{sab.get('ad', '')}**")
                    st.caption(sab.get("metin", "")[:100] + ("..." if len(sab.get("metin", "")) > 100 else ""))
                with col_s2:
                    if st.button("Sil", key=f"smm_del_sab_{sab['id']}"):
                        sablonlar = [s for s in sablonlar if s["id"] != sab["id"]]
                        settings["metin_sablonlari"] = sablonlar
                        _save_settings(settings)
                        st.rerun()
        else:
            st.info("Henuz sablon eklenmedi.")

    # --- Hashtag Havuzu ---
    with sub_ic3:
        st.markdown("##### Hashtag Havuzu")
        hashtag_havuz = settings.get("hashtag_havuzu", [])

        col_h1, col_h2 = st.columns([3, 1])
        with col_h1:
            new_tag = st.text_input("Yeni Hashtag (#ile baslayabilir)", key="smm_new_tag")
        with col_h2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Ekle", key="smm_add_tag", type="primary"):
                if new_tag:
                    tag = new_tag if new_tag.startswith("#") else f"#{new_tag}"
                    if tag not in hashtag_havuz:
                        hashtag_havuz.append(tag)
                        settings["hashtag_havuzu"] = hashtag_havuz
                        _save_settings(settings)
                        st.success(f"{tag} eklendi.")
                        st.rerun()
                    else:
                        st.warning("Bu hashtag zaten mevcut.")

        if hashtag_havuz:
            badges = " ".join(
                f'<span style="background:#2563eb15;color:#2563eb;padding:4px 12px;'
                f'border-radius:20px;font-size:0.8rem;font-weight:600;margin:2px;'
                f'display:inline-block">{tag}</span>'
                for tag in hashtag_havuz
            )
            st.markdown(badges, unsafe_allow_html=True)
            st.markdown("")
            tag_to_del = st.selectbox("Silmek için sec", [""] + hashtag_havuz, key="smm_del_tag_sel")
            if tag_to_del and st.button("Hashtag Sil", key="smm_del_tag"):
                hashtag_havuz.remove(tag_to_del)
                settings["hashtag_havuzu"] = hashtag_havuz
                _save_settings(settings)
                st.rerun()
        else:
            st.info("Henuz hashtag eklenmedi.")

    # --- Kampanya Etiketleri ---
    with sub_ic4:
        st.markdown("##### Kampanya Etiketleri")
        kampanyalar = settings.get("kampanya_etiketleri", list(KAMPANYA_ETIKETLERI))

        col_k1, col_k2 = st.columns([3, 1])
        with col_k1:
            new_kamp = st.text_input("Yeni Kampanya Etiketi", key="smm_new_kamp")
        with col_k2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Ekle", key="smm_add_kamp", type="primary"):
                if new_kamp and new_kamp not in kampanyalar:
                    kampanyalar.append(new_kamp)
                    settings["kampanya_etiketleri"] = kampanyalar
                    _save_settings(settings)
                    st.success(f"{new_kamp} eklendi.")
                    st.rerun()

        badges_k = " ".join(
            f'<span style="background:#f59e0b20;color:#d97706;padding:4px 12px;'
            f'border-radius:20px;font-size:0.8rem;font-weight:600;margin:2px;'
            f'display:inline-block">{k}</span>'
            for k in kampanyalar
        )
        st.markdown(badges_k, unsafe_allow_html=True)


# ===================== 3. YENI PAYLASIM =====================

def _render_yeni_paylasim():
    styled_section("Yeni Paylasim Oluştur", "#10b981")

    settings = _settings()
    accounts = _accounts()
    connected = [a["platform"] for a in accounts if a.get("status") == "connected"]

    # Platform secimi
    platform_options = [p[2] for p in PLATFORMLAR if p[0] in connected]
    all_platform_options = [p[2] for p in PLATFORMLAR]
    if not platform_options:
        platform_options = all_platform_options
        st.info("Henuz bagli platform yok. Tüm platformlar listeleniyor.")

    selected_platforms = st.multiselect(
        "Platformlar", platform_options,
        default=platform_options[:1] if platform_options else [],
        key="smm_new_platforms"
    )
    platform_keys = []
    for sp in selected_platforms:
        for p in PLATFORMLAR:
            if p[2] == sp:
                platform_keys.append(p[0])

    # Medya ekleme
    st.markdown("##### Medya")
    media_source = st.radio("Medya Kaynagi", ["Dosya Yukle", "Kutuphaneden Sec"], horizontal=True, key="smm_media_src")

    selected_media = []
    if media_source == "Dosya Yukle":
        up_files = st.file_uploader(
            "Görsel/Video Yükle", type=["png", "jpg", "jpeg", "gif", "mp4", "mov"],
            accept_multiple_files=True, key="smm_post_media"
        )
        if up_files:
            from utils.security import validate_upload
            _valid_up = []
            for uf in up_files:
                _ok, _msg = validate_upload(uf, allowed_types=["png", "jpg", "jpeg", "gif", "mp4", "mov"], max_mb=50)
                if _ok:
                    _valid_up.append(uf)
                else:
                    st.warning(f"⚠️ {uf.name}: {_msg}")
            up_files = _valid_up
        if up_files:
            for uf in up_files:
                selected_media.append({
                    "dosya": uf.name,
                    "tip": "image" if uf.type and uf.type.startswith("image") else "video",
                    "_file": uf,
                })
    else:
        assets = _assets()
        media_assets = [a for a in assets if a.get("tip") in ("image", "video")]
        if media_assets:
            asset_names = [a.get("orijinal_ad", a["id"]) for a in media_assets]
            chosen = st.multiselect("Kutuphaneden Sec", asset_names, key="smm_lib_media")
            for c in chosen:
                asset = next((a for a in media_assets if a.get("orijinal_ad", a["id"]) == c), None)
                if asset:
                    selected_media.append({"dosya": asset["dosya"], "tip": asset["tip"]})
        else:
            st.info("Kutuphanede medya yok. Öncelikle İçerikler sekmesinden yukleyin.")

    # Metin
    st.markdown("##### Açıklama")
    # Sablon secimi
    sablonlar = settings.get("metin_sablonlari", [])
    sablon_choice = ""
    if sablonlar:
        sablon_names = ["-- Bos --"] + [s["ad"] for s in sablonlar]
        sablon_sel = st.selectbox("Sablondan Yukle", sablon_names, key="smm_sablon_sel")
        if sablon_sel != "-- Bos --":
            sab = next((s for s in sablonlar if s["ad"] == sablon_sel), None)
            sablon_choice = sab.get("metin", "") if sab else ""

    metin = st.text_area("Paylasim Metni", value=sablon_choice, height=120, key="smm_post_metin")

    # Hashtag secimi
    hashtag_havuz = settings.get("hashtag_havuzu", [])
    selected_tags = []
    if hashtag_havuz:
        selected_tags = st.multiselect("Hashtagler", hashtag_havuz, key="smm_post_tags")

    # Kampanya
    kampanyalar = settings.get("kampanya_etiketleri", list(KAMPANYA_ETIKETLERI))
    kampanya = st.selectbox("Kampanya Etiketi", [""] + kampanyalar, key="smm_post_kamp")

    # Platform ozel metin
    platform_metinleri = {}
    if len(platform_keys) > 1:
        with st.expander("Platform Özel Metin (Opsiyonel)"):
            for pk in platform_keys:
                info = PLATFORM_MAP[pk]
                pm = st.text_area(
                    f"{info['icon']} {info['label']} Özel Metin",
                    key=f"smm_pm_{pk}", height=80
                )
                if pm:
                    platform_metinleri[pk] = pm

    # Onizleme
    if selected_platforms and metin:
        st.markdown("##### Onizleme")
        cols = st.columns(min(len(platform_keys), 3))
        for idx, pk in enumerate(platform_keys):
            info = PLATFORM_MAP[pk]
            display_text = platform_metinleri.get(pk, metin)
            tag_str = " ".join(selected_tags) if selected_tags else ""
            with cols[idx % min(len(platform_keys), 3)]:
                st.markdown(f"""<div style="border:2px solid {info['color']};border-radius:14px;
                padding:16px;margin-bottom:8px">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px">
                <span style="font-size:1.3rem">{info['icon']}</span>
                <span style="font-weight:700;color:{info['color']}">{info['label']}</span></div>
                <div style="font-size:0.85rem;color:#94A3B8;line-height:1.6">{display_text}</div>
                <div style="font-size:0.78rem;color:#2563eb;margin-top:6px">{tag_str}</div>
                </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Calisma modu
    calisma_modu = settings.get("calisma_modu", "her_ikisi")

    # Butonlar
    bc1, bc2, bc3 = st.columns(3)

    with bc1:
        if st.button("Taslak Kaydet", key="smm_save_draft"):
            if metin or selected_media:
                _save_post(platform_keys, metin, platform_metinleri, selected_media,
                           selected_tags, kampanya, "DRAFT", "direkt")
                st.success("Taslak kaydedildi.")
                st.rerun()
            else:
                st.warning("Lutfen metin veya medya ekleyin.")

    with bc2:
        if calisma_modu in ("direkt", "her_ikisi"):
            if st.button("Direkt Paylas", key="smm_publish", type="primary"):
                if metin or selected_media:
                    # Planlama secimi
                    plan_mode = st.session_state.get("smm_plan_toggle", False)
                    status = "SCHEDULED" if plan_mode else "PUBLISHING"
                    post = _save_post(platform_keys, metin, platform_metinleri, selected_media,
                                      selected_tags, kampanya, status, "direkt")
                    if status == "PUBLISHING":
                        # Gercek API ile yayinla
                        _publish_to_platforms(post["id"])
                    else:
                        st.success("Paylasim planlandi!")
                    st.rerun()
                else:
                    st.warning("Lutfen metin veya medya ekleyin.")

    with bc3:
        if calisma_modu in ("onayli", "her_ikisi"):
            if st.button("Onaya Gonder", key="smm_submit"):
                if metin or selected_media:
                    _save_post(platform_keys, metin, platform_metinleri, selected_media,
                               selected_tags, kampanya, "SUBMITTED", "onayli")
                    st.success("Onaya gonderildi.")
                    st.rerun()
                else:
                    st.warning("Lutfen metin veya medya ekleyin.")

    # Planlama secenegi
    if calisma_modu in ("direkt", "her_ikisi"):
        plan_toggle = st.checkbox("Ileri tarihe planla", key="smm_plan_toggle")
        if plan_toggle:
            col_d, col_t = st.columns(2)
            with col_d:
                st.date_input("Tarih", key="smm_plan_date")
            with col_t:
                st.time_input("Saat", key="smm_plan_time")


def _save_post(platforms, metin, platform_metinleri, medya, hashtagler,
               kampanya, status, mod):
    posts = _posts()
    auth_user = st.session_state.get("auth_user", {})
    plan_date = ""
    if status == "SCHEDULED":
        d = st.session_state.get("smm_plan_date")
        t = st.session_state.get("smm_plan_time")
        if d and t:
            plan_date = f"{d} {t}"

    # Medya dosyalari kaydet
    saved_media = []
    for m in medya:
        if "_file" in m:
            media_dir = os.path.join(_smm_dir(), "smm_media")
            os.makedirs(media_dir, exist_ok=True)
            fname = f"{_new_id('med')}_{m['dosya']}"
            fpath = os.path.join(media_dir, fname)
            with open(fpath, "wb") as f:
                f.write(m["_file"].getvalue())
            saved_media.append({"dosya": fpath, "tip": m["tip"]})
        else:
            saved_media.append({"dosya": m["dosya"], "tip": m["tip"]})

    post = {
        "id": _new_id("smm"),
        "platformlar": platforms,
        "metin": metin,
        "platform_metinleri": platform_metinleri,
        "medya": saved_media,
        "hashtagler": hashtagler,
        "kampanya": kampanya,
        "status": status,
        "mod": mod,
        "olusturan": {
            "id": auth_user.get("username", ""),
            "ad": auth_user.get("name", ""),
        },
        "onay_gecmisi": [],
        "planlanan_tarih": plan_date,
        "yayin_tarihi": _now() if status == "PUBLISHED" else "",
        "yayin_sonuclari": {},
        "analytics": {"begeni": 0, "yorum": 0, "paylasim": 0, "goruntulenme": 0},
        "created_at": _now(),
        "updated_at": _now(),
    }
    posts.append(post)
    _save_posts(posts)
    return post


def _publish_to_platforms(post_id: str):
    """Postu gercek API'ler uzerinden platformlara yayinla."""
    posts = _posts()
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        return

    accounts = _accounts()
    platforms = post.get("platformlar", [])
    metin = post.get("metin", "")
    platform_metinleri = post.get("platform_metinleri", {})
    medya = post.get("medya", [])
    hashtagler = post.get("hashtagler", [])
    yayin_sonuclari = {}
    all_ok = True
    fail_messages = []

    for plat_key in platforms:
        acc = next((a for a in accounts if a.get("platform") == plat_key and a.get("status") == "connected"), None)
        if not acc:
            yayin_sonuclari[plat_key] = {"ok": False, "message": "Platform bagli degil"}
            all_ok = False
            fail_messages.append(f"{PLATFORM_MAP.get(plat_key, {}).get('label', plat_key)}: Bagli degil")
            continue

        plat_metin = platform_metinleri.get(plat_key, metin)
        creds = {
            "api_key": acc.get("api_key", ""),
            "api_secret": acc.get("api_secret", ""),
            "access_token": acc.get("access_token", ""),

            "page_id": acc.get("page_id", ""),
        }

        with st.spinner(f"{PLATFORM_MAP.get(plat_key, {}).get('icon', '')} {PLATFORM_MAP.get(plat_key, {}).get('label', plat_key)} yayinlaniyor..."):
            result = SocialMediaAPI.publish(plat_key, creds, plat_metin, medya, hashtagler)

        yayin_sonuclari[plat_key] = result
        if result["ok"]:
            plat_label = PLATFORM_MAP.get(plat_key, {}).get("label", plat_key)
            st.success(f"{plat_label}: {result['message']}")
        else:
            all_ok = False
            plat_label = PLATFORM_MAP.get(plat_key, {}).get("label", plat_key)
            fail_messages.append(f"{plat_label}: {result['message']}")
            st.error(f"{plat_label}: {result['message']}")

    # Post durumunu guncelle
    for p in posts:
        if p["id"] == post_id:
            p["yayin_sonuclari"] = yayin_sonuclari
            p["updated_at"] = _now()
            if all_ok:
                p["status"] = "PUBLISHED"
                p["yayin_tarihi"] = _now()
                st.success("Tüm platformlarda basariyla yayinlandi!")
            elif any(r.get("ok") for r in yayin_sonuclari.values()):
                # Kismen basarili
                p["status"] = "PUBLISHED"
                p["yayin_tarihi"] = _now()
                st.warning("Bazi platformlarda hata olustu:\n" + "\n".join(fail_messages))
            else:
                p["status"] = "PUBLISH_FAILED"
                st.error("Yayin basarisiz:\n" + "\n".join(fail_messages))
            break
    _save_posts(posts)


# ===================== 4. ONAY KUYRUGU =====================

def _render_onay_kuyrugu():
    styled_section("Onay Kuyrugu", "#f59e0b")

    posts = _posts()
    onay_statuses = ["SUBMITTED", "IN_REVIEW", "CHANGES_REQUESTED"]
    onay_posts = [p for p in posts if p.get("status") in onay_statuses]

    if not onay_posts:
        st.info("Onay bekleyen paylasim yok.")
        return

    # Ozet kartlar
    submitted = len([p for p in onay_posts if p["status"] == "SUBMITTED"])
    in_review = len([p for p in onay_posts if p["status"] == "IN_REVIEW"])
    changes_req = len([p for p in onay_posts if p["status"] == "CHANGES_REQUESTED"])

    styled_stat_row([
        ("Onay Bekliyor", str(submitted), "#f59e0b", "📨"),
        ("Incelemede", str(in_review), "#8b5cf6", "🔍"),
        ("Revizyon", str(changes_req), "#ef4444", "✏️"),
    ])
    st.markdown("")

    # Filtre
    filter_status = st.selectbox(
        "Durum Filtresi", ["Tümü"] + onay_statuses,
        format_func=lambda x: STATUS_MAP.get(x, {}).get("label", x) if x != "Tümü" else "Tümü",
        key="smm_onay_filter"
    )
    filtered = onay_posts if filter_status == "Tümü" else [p for p in onay_posts if p["status"] == filter_status]

    for post in sorted(filtered, key=lambda x: x.get("created_at", ""), reverse=True):
        plat_badges = " ".join(_platform_badge(pk) for pk in post.get("platformlar", []))
        with st.expander(f"{post.get('metin', '')[:50]}... — {STATUS_MAP.get(post['status'], {}).get('label', post['status'])}",
            expanded=False
        ):
            st.markdown(f"**Oluşturan:** {post.get('olusturan', {}).get('ad', '-')}", unsafe_allow_html=True)
            st.markdown(f"**Platformlar:** {plat_badges}", unsafe_allow_html=True)
            st.markdown(f"**Tarih:** {post.get('created_at', '-')}")
            st.markdown(f"**Metin:** {post.get('metin', '')}")
            if post.get("hashtagler"):
                st.markdown(f"**Hashtagler:** {' '.join(post['hashtagler'])}")

            # Onay gecmisi
            if post.get("onay_gecmisi"):
                st.markdown("**Onay Geçmişi:**")
                for og in post["onay_gecmisi"]:
                    icon = {"onaylandi": "✅", "iade": "🔄", "reddedildi": "❌"}.get(og.get("islem", ""), "📝")
                    st.markdown(
                        f"- {icon} {og.get('tarih', '')} — {og.get('kisi', '')} — "
                        f"*{og.get('islem', '')}* — {og.get('yorum', '')}"
                    )

            st.markdown("---")

            # Aksiyonlar
            yorum = st.text_input("Yorum", key=f"smm_onay_yorum_{post['id']}")
            auth_user = st.session_state.get("auth_user", {})
            reviewer = auth_user.get("name", "Yetkili")

            ac1, ac2, ac3 = st.columns(3)
            with ac1:
                if st.button("Onayla", key=f"smm_approve_{post['id']}", type="primary"):
                    _update_post_status(post["id"], "APPROVED", reviewer, yorum, "onaylandi")
                    st.success("Paylasim onaylandi!")
                    st.rerun()
            with ac2:
                if st.button("Revizyon Iste", key=f"smm_revise_{post['id']}"):
                    _update_post_status(post["id"], "CHANGES_REQUESTED", reviewer, yorum, "iade")
                    st.warning("Revizyon istendi.")
                    st.rerun()
            with ac3:
                if st.button("Reddet", key=f"smm_reject_{post['id']}"):
                    _update_post_status(post["id"], "CANCELED", reviewer, yorum, "reddedildi")
                    st.error("Paylasim reddedildi.")
                    st.rerun()


def _update_post_status(post_id: str, new_status: str, reviewer: str, yorum: str, islem: str):
    posts = _posts()
    for p in posts:
        if p["id"] == post_id:
            p["status"] = new_status
            p["updated_at"] = _now()
            if "onay_gecmisi" not in p:
                p["onay_gecmisi"] = []
            p["onay_gecmisi"].append({
                "tarih": _now(),
                "islem": islem,
                "kisi": reviewer,
                "yorum": yorum,
            })
            if new_status == "PUBLISHED":
                p["yayin_tarihi"] = _now()
            break
    _save_posts(posts)


# ===================== 5. TAKVIM =====================

def _render_takvim():
    styled_section("İçerik Takvimi", "#0d9488")

    posts = _posts()
    today = datetime.now()

    # Ay secimi
    col_m1, col_m2 = st.columns([1, 1])
    with col_m1:
        sel_month = st.selectbox(
            "Ay", list(range(1, 13)),
            index=today.month - 1,
            format_func=lambda m: ["Ocak", "Subat", "Mart", "Nisan", "Mayis", "Haziran",
                                    "Temmuz", "Agustos", "Eylul", "Ekim", "Kasim", "Aralik"][m - 1],
            key="smm_cal_month"
        )
    with col_m2:
        sel_year = st.number_input("Yil", min_value=2024, max_value=2030,
                                   value=today.year, key="smm_cal_year")

    # Takvim grid
    cal = calendar.Calendar(firstweekday=0)  # Pazartesi
    month_days = cal.monthdayscalendar(sel_year, sel_month)

    # Gun isimleri
    day_names = ["Pzt", "Sal", "Car", "Per", "Cum", "Cmt", "Paz"]
    header_html = "".join(
        f'<div style="text-align:center;font-weight:700;color:#64748b;font-size:0.8rem;padding:8px">{d}</div>'
        for d in day_names
    )

    # Icerik takvime esleme
    def _posts_for_day(day: int) -> list:
        if day == 0:
            return []
        date_str = f"{sel_year}-{sel_month:02d}-{day:02d}"
        result = []
        for p in posts:
            p_date = p.get("yayin_tarihi", "") or p.get("planlanan_tarih", "") or p.get("created_at", "")
            if p_date[:10] == date_str:
                result.append(p)
        return result

    # Grid olustur
    grid_html = f'<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:2px;margin-top:10px">'
    grid_html += header_html

    for week in month_days:
        for day in week:
            if day == 0:
                grid_html += '<div style="padding:8px;background:#111827;border-radius:6px;min-height:60px"></div>'
            else:
                day_posts = _posts_for_day(day)
                is_today = (day == today.day and sel_month == today.month and sel_year == today.year)
                bg = "#eff6ff" if is_today else "#ffffff"
                border = "2px solid #2563eb" if is_today else "1px solid #e2e8f0"

                dots = ""
                for dp in day_posts[:3]:
                    s_info = STATUS_MAP.get(dp.get("status", ""), {"color": "#94a3b8"})
                    dots += f'<div style="width:8px;height:8px;border-radius:50%;background:{s_info["color"]};display:inline-block;margin:1px"></div>'

                grid_html += (
                    f'<div style="padding:6px 8px;background:{bg};border:{border};border-radius:8px;min-height:60px">'
                    f'<div style="font-weight:600;font-size:0.85rem;color:#0B0F19">{day}</div>'
                    f'<div style="margin-top:4px">{dots}</div>'
                    f'{"<div style=font-size:0.65rem;color:#64748b;margin-top:2px>" + str(len(day_posts)) + " icerik</div>" if day_posts else ""}'
                    f'</div>'
                )

    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

    # Secili gun detay
    st.markdown("---")
    sel_day = st.number_input("Gün Detayi", min_value=1,
                              max_value=calendar.monthrange(sel_year, sel_month)[1],
                              value=min(today.day, calendar.monthrange(sel_year, sel_month)[1]),
                              key="smm_cal_day")

    day_posts = _posts_for_day(sel_day)
    if day_posts:
        st.markdown(f"**{sel_day}/{sel_month}/{sel_year} — {len(day_posts)} icerik:**")
        for dp in day_posts:
            plat_badges = " ".join(_platform_badge(pk) for pk in dp.get("platformlar", []))
            st.markdown(
                f'{_status_badge(dp.get("status", "DRAFT"))} {plat_badges} '
                f'— {dp.get("metin", "")[:60]}...',
                unsafe_allow_html=True
            )
    else:
        st.info(f"{sel_day}/{sel_month}/{sel_year} tarihinde icerik yok.")


# ===================== 6. DASHBOARD (ANALYTICS) =====================

def _render_dashboard():
    styled_section("Sosyal Medya Analytics", "#6366f1")

    posts = _posts()
    published = [p for p in posts if p.get("status") == "PUBLISHED"]

    if not published:
        st.info("Henuz yayinlanmis paylasim yok. Analiz için veri bulunmuyor.")
        return

    # API'den gercek analiz cekme butonu
    if st.button("Analiz Verilerini Güncelle (API)", key="smm_refresh_analytics", type="primary"):
        _sync_analytics(published)
        st.rerun()

    # Toplam metrikler
    total_begeni = sum(p.get("analytics", {}).get("begeni", 0) for p in published)
    total_yorum = sum(p.get("analytics", {}).get("yorum", 0) for p in published)
    total_paylasim = sum(p.get("analytics", {}).get("paylasim", 0) for p in published)
    total_goruntulenme = sum(p.get("analytics", {}).get("goruntulenme", 0) for p in published)

    styled_stat_row([
        ("Begeni", str(total_begeni), "#ef4444", "❤️"),
        ("Yorum", str(total_yorum), "#2563eb", "💬"),
        ("Paylasim", str(total_paylasim), "#10b981", "🔄"),
        ("Görüntülenme", str(total_goruntulenme), "#8b5cf6", "👁️"),
    ])
    st.markdown("")

    # Platform bazli KPI
    styled_section("Platform Bazli Performans", "#2563eb")
    plat_data = {}
    for p in published:
        for pk in p.get("platformlar", []):
            if pk not in plat_data:
                plat_data[pk] = {"paylasim_sayisi": 0, "begeni": 0, "yorum": 0, "goruntulenme": 0}
            plat_data[pk]["paylasim_sayisi"] += 1
            plat_data[pk]["begeni"] += p.get("analytics", {}).get("begeni", 0)
            plat_data[pk]["yorum"] += p.get("analytics", {}).get("yorum", 0)
            plat_data[pk]["goruntulenme"] += p.get("analytics", {}).get("goruntulenme", 0)

    if plat_data:
        cols = st.columns(min(len(plat_data), 5))
        for idx, (pk, pd_val) in enumerate(plat_data.items()):
            info = PLATFORM_MAP.get(pk, {"icon": "🌐", "label": pk, "color": "#64748b"})
            with cols[idx % min(len(plat_data), 5)]:
                st.markdown(f"""<div style="background:white;border:2px solid {info['color']};
                border-radius:14px;padding:16px;text-align:center">
                <div style="font-size:2rem">{info['icon']}</div>
                <div style="font-weight:700;color:{info['color']};margin:4px 0">{info['label']}</div>
                <div style="font-size:0.8rem;color:#64748b">{pd_val['paylasim_sayisi']} paylasim</div>
                <div style="font-size:0.8rem;color:#64748b">❤️ {pd_val['begeni']} | 💬 {pd_val['yorum']}</div>
                </div>""", unsafe_allow_html=True)

    st.markdown("")

    # Top 5 icerik
    styled_section("En Iyi 5 İçerik", "#10b981")
    sorted_posts = sorted(published,
                          key=lambda x: sum(x.get("analytics", {}).values()),
                          reverse=True)[:5]
    for idx, sp in enumerate(sorted_posts, 1):
        total = sum(sp.get("analytics", {}).values())
        plat_badges = " ".join(_platform_badge(pk) for pk in sp.get("platformlar", []))
        st.markdown(
            f"**{idx}.** {plat_badges} — {sp.get('metin', '')[:50]}... "
            f"(**{total}** toplam etkilesim)",
            unsafe_allow_html=True
        )

    st.markdown("")

    # Kampanya bazli performans (bar chart)
    styled_section("Kampanya Performansi", "#f59e0b")
    kamp_data = {}
    for p in published:
        k = p.get("kampanya", "Diger") or "Diger"
        if k not in kamp_data:
            kamp_data[k] = {"begeni": 0, "yorum": 0, "paylasim": 0, "goruntulenme": 0}
        for metric in ["begeni", "yorum", "paylasim", "goruntulenme"]:
            kamp_data[k][metric] += p.get("analytics", {}).get(metric, 0)

    if kamp_data:
        import pandas as pd
        df_kamp = pd.DataFrame([
            {"Kampanya": k, "Begeni": v["begeni"], "Yorum": v["yorum"],
             "Paylasim": v["paylasim"], "Görüntülenme": v["goruntulenme"]}
            for k, v in kamp_data.items()
        ])
        _metrics = ["Begeni", "Yorum", "Paylasim", "Görüntülenme"]
        fig_kamp = go.Figure()
        for i, m in enumerate(_metrics):
            fig_kamp.add_trace(go.Bar(
                x=df_kamp["Kampanya"], y=df_kamp[m], name=m,
                marker_color=SC_COLORS[i % len(SC_COLORS)],
                text=df_kamp[m], textposition="outside",
            ))
        fig_kamp.update_layout(barmode="group", legend_title="Metrik")
        sc_bar(fig_kamp, height=350)
        st.plotly_chart(fig_kamp, use_container_width=True, config=SC_CHART_CFG)

    # Platform dagilimi (donut chart)
    col_ch1, col_ch2 = st.columns(2)
    with col_ch1:
        styled_section("Platform Dagilimi", "#E4405F")
        if plat_data:
            plat_names = [PLATFORM_MAP.get(k, {}).get("label", k) for k in plat_data]
            plat_counts = [v["paylasim_sayisi"] for v in plat_data.values()]
            _n = len(plat_names)
            fig_donut = go.Figure(data=[go.Pie(
                labels=plat_names, values=plat_counts, hole=0.55,
                marker=dict(colors=SC_COLORS[:_n], line=dict(color="#fff", width=2)),
                textinfo="label+percent",
            )])
            sc_pie(fig_donut, height=300)
            st.plotly_chart(fig_donut, use_container_width=True, config=SC_CHART_CFG)

    with col_ch2:
        styled_section("Zaman Bazli Trend", "#2563eb")
        # Son 30 gun trend
        date_data = {}
        for p in published:
            p_date = (p.get("yayin_tarihi") or p.get("created_at", ""))[:10]
            if p_date:
                if p_date not in date_data:
                    date_data[p_date] = 0
                date_data[p_date] += sum(p.get("analytics", {}).values())

        if date_data:
            import pandas as pd
            df_trend = pd.DataFrame([
                {"Tarih": k, "Etkilesim": v}
                for k, v in sorted(date_data.items())
            ])
            fig_trend = px.line(
                df_trend, x="Tarih", y="Etkilesim",
                color_discrete_sequence=[SC_COLORS[0]],
                markers=True, title=""
            )
            fig_trend.update_layout(
                height=300,
                margin=dict(t=10, b=30, l=30, r=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(tickfont_size=9),
                yaxis=dict(tickfont_size=9, showgrid=True, gridcolor="#1A2035"),
            )
            st.plotly_chart(fig_trend, use_container_width=True, config=SC_CHART_CFG)
        else:
            st.info("Trend için yeterli veri yok.")


def _sync_analytics(published: list):
    """Yayinlanan postlarin analizlerini API'den cek ve guncelle."""
    accounts = _accounts()
    posts = _posts()
    updated = 0

    progress = st.progress(0, text="Analiz verileri cekiliyor...")
    total = sum(len(p.get("platformlar", [])) for p in published)
    done = 0

    for pub in published:
        post_results = pub.get("yayin_sonuclari", {})
        merged_analytics = {"begeni": 0, "yorum": 0, "paylasim": 0, "goruntulenme": 0}

        for plat_key in pub.get("platformlar", []):
            plat_result = post_results.get(plat_key, {})
            plat_post_id = plat_result.get("post_id", "")
            acc = next((a for a in accounts if a.get("platform") == plat_key and a.get("status") == "connected"), None)
            if acc and plat_post_id:
                creds = {
                    "api_key": acc.get("api_key", ""),
                    "api_secret": acc.get("api_secret", ""),
                    "access_token": acc.get("access_token", ""),
        
                    "page_id": acc.get("page_id", ""),
                }
                analytics = SocialMediaAPI.get_analytics(plat_key, creds, plat_post_id)
                for k in merged_analytics:
                    merged_analytics[k] += analytics.get(k, 0)
            done += 1
            progress.progress(min(done / max(total, 1), 1.0), text=f"Analiz cekiliyor... ({done}/{total})")

        # Post'u guncelle
        for p in posts:
            if p["id"] == pub["id"]:
                if any(v > 0 for v in merged_analytics.values()):
                    p["analytics"] = merged_analytics
                    p["updated_at"] = _now()
                    updated += 1
                break

    _save_posts(posts)
    progress.empty()
    st.success(f"{updated} paylasimin analiz verileri güncellendi.")


# ===================== 7. GELEN KUTUSU =====================

def _render_gelen_kutusu():
    styled_section("Gelen Kutusu", "#1877F2")

    inbox = _inbox()

    # API'den gercek yorum/mention cekme
    if st.button("Yorumlari ve Etiketlemeleri Cek (API)", key="smm_fetch_inbox", type="primary"):
        _fetch_real_inbox()
        inbox = _inbox()  # Yeniden yukle

    # Ozet
    okunmamis = len([m for m in inbox if not m.get("okundu")])
    toplam = len(inbox)

    col_g1, col_g2, col_g3 = st.columns(3)
    with col_g1:
        st.metric("Toplam", toplam)
    with col_g2:
        st.metric("Okunmamis", okunmamis)
    with col_g3:
        st.metric("Bugün", len([m for m in inbox if m.get("tarih", "")[:10] == _today()]))

    # Filtre
    filter_plat = st.selectbox(
        "Platform Filtresi", ["Tümü"] + [p[2] for p in PLATFORMLAR],
        key="smm_inbox_filter"
    )

    filtered = inbox
    if filter_plat != "Tümü":
        plat_key = next((p[0] for p in PLATFORMLAR if p[2] == filter_plat), "")
        filtered = [m for m in inbox if m.get("platform") == plat_key]

    if not filtered:
        st.info("Gelen kutusu bos.")
        return

    # Yeni mesaj ekleme (simule)
    with st.expander("Test Mesaji Ekle (Simulasyon)"):
        sim_plat = st.selectbox("Platform", [p[2] for p in PLATFORMLAR], key="smm_sim_plat")
        sim_tip = st.selectbox("Tip", ["yorum", "mention", "dm"], key="smm_sim_tip")
        sim_user = st.text_input("Kullanıcı", key="smm_sim_user")
        sim_metin = st.text_area("Mesaj", key="smm_sim_metin")
        if st.button("Ekle", key="smm_sim_add", type="primary"):
            if sim_user and sim_metin:
                plat_key = next((p[0] for p in PLATFORMLAR if p[2] == sim_plat), "instagram")
                inbox.append({
                    "id": _new_id("inb"),
                    "platform": plat_key,
                    "tip": sim_tip,
                    "kullanici": sim_user,
                    "metin": sim_metin,
                    "tarih": _now(),
                    "okundu": False,
                    "yanitlandi": False,
                    "gorev_atandi": False,
                    "gorev_kisi": "",
                })
                _save_inbox(inbox)
                st.success("Test mesaji eklendi.")
                st.rerun()

    # Mesaj listesi
    for msg in sorted(filtered, key=lambda x: x.get("tarih", ""), reverse=True):
        p_info = PLATFORM_MAP.get(msg.get("platform", ""), {"icon": "🌐", "label": "?", "color": "#64748b"})
        okundu_icon = "📩" if not msg.get("okundu") else "📧"
        tip_label = {"yorum": "Yorum", "mention": "Etiketleme", "dm": "Mesaj"}.get(msg.get("tip", ""), msg.get("tip", ""))

        bg_color = "#eff6ff" if not msg.get("okundu") else "#ffffff"
        with st.container():
            st.markdown(f"""<div style="background:{bg_color};border:1px solid #e2e8f0;
            border-radius:12px;padding:14px;margin-bottom:8px;border-left:4px solid {p_info['color']}">
            <div style="display:flex;justify-content:space-between;align-items:center">
            <div>
            <span style="font-size:1rem">{okundu_icon}</span>
            <span style="font-weight:700;color:#0B0F19;margin:0 8px">@{msg.get('kullanici', '')}</span>
            {_platform_badge(msg.get('platform', ''))}
            <span style="background:#1A203520;color:#64748b;padding:2px 8px;border-radius:10px;
            font-size:0.75rem;margin-left:4px">{tip_label}</span>
            </div>
            <span style="font-size:0.75rem;color:#94a3b8">{msg.get('tarih', '')}</span>
            </div>
            <div style="margin-top:8px;color:#94A3B8;font-size:0.9rem">{msg.get('metin', '')}</div>
            </div>""", unsafe_allow_html=True)

            # Aksiyonlar
            mc1, mc2, mc3, mc4 = st.columns(4)
            with mc1:
                if not msg.get("okundu"):
                    if st.button("Okundu", key=f"smm_read_{msg['id']}"):
                        for m in inbox:
                            if m["id"] == msg["id"]:
                                m["okundu"] = True
                                break
                        _save_inbox(inbox)
                        st.rerun()
            with mc2:
                if not msg.get("yanitlandi"):
                    yanit = st.text_input("Yanit", key=f"smm_reply_text_{msg['id']}", label_visibility="collapsed",
                                          placeholder="Yanit yaz...")
                    if yanit:
                        if st.button("Gonder", key=f"smm_reply_{msg['id']}"):
                            for m in inbox:
                                if m["id"] == msg["id"]:
                                    m["yanitlandi"] = True
                                    m["yanit"] = yanit
                                    m["yanit_tarih"] = _now()
                                    break
                            _save_inbox(inbox)
                            st.success("Yanit gonderildi.")
                            st.rerun()
            with mc3:
                if not msg.get("gorev_atandi"):
                    gorev_kisi = st.text_input("Görev Ata", key=f"smm_assign_text_{msg['id']}",
                                               label_visibility="collapsed", placeholder="Kisi adi...")
                    if gorev_kisi:
                        if st.button("Ata", key=f"smm_assign_{msg['id']}"):
                            for m in inbox:
                                if m["id"] == msg["id"]:
                                    m["gorev_atandi"] = True
                                    m["gorev_kisi"] = gorev_kisi
                                    break
                            _save_inbox(inbox)
                            st.success(f"{gorev_kisi} kisisine atandi.")
                            st.rerun()
            with mc4:
                if st.button("Sil", key=f"smm_del_msg_{msg['id']}"):
                    inbox = [m for m in inbox if m["id"] != msg["id"]]
                    _save_inbox(inbox)
                    st.rerun()


def _fetch_real_inbox():
    """Bagli platformlardan gercek yorum ve mention'lari cek."""
    accounts = _accounts()
    inbox = _inbox()
    existing_ids = {m.get("external_id") for m in inbox if m.get("external_id")}
    new_count = 0

    for acc in accounts:
        if acc.get("status") != "connected":
            continue
        plat_key = acc.get("platform", "")
        creds = {
            "api_key": acc.get("api_key", ""),
            "api_secret": acc.get("api_secret", ""),
            "access_token": acc.get("access_token", ""),

            "page_id": acc.get("page_id", ""),
        }

        with st.spinner(f"{PLATFORM_MAP.get(plat_key, {}).get('icon', '')} {PLATFORM_MAP.get(plat_key, {}).get('label', plat_key)} yorumlari cekiliyor..."):
            comments = SocialMediaAPI.get_comments(plat_key, creds)

        for c in comments:
            ext_id = c.get("id", "")
            if ext_id and ext_id in existing_ids:
                continue  # Zaten mevcut
            inbox.append({
                "id": _new_id("inb"),
                "external_id": ext_id,
                "platform": c.get("platform", plat_key),
                "tip": c.get("tip", "yorum"),
                "kullanici": c.get("kullanici", ""),
                "metin": c.get("metin", ""),
                "tarih": c.get("tarih", _now()),
                "okundu": False,
                "yanitlandi": False,
                "gorev_atandi": False,
                "gorev_kisi": "",
            })
            new_count += 1

    _save_inbox(inbox)
    if new_count > 0:
        st.success(f"{new_count} yeni yorum/etiketleme cekildi.")
    else:
        st.info("Yeni yorum veya etiketleme bulunamadı.")


# ===================== 8. UYARILAR =====================

def _render_uyarilar():
    styled_section("Uyari Merkezi", "#ef4444")

    alerts = _alerts()
    posts = _posts()
    accounts = _accounts()

    # Otomatik uyari kontrolleri
    new_alerts = []

    # 1. 48 saat paylasim yok uyarisi
    published = [p for p in posts if p.get("status") == "PUBLISHED"]
    if published:
        son_yayin = max(p.get("yayin_tarihi", "") or p.get("created_at", "") for p in published)
        if son_yayin:
            try:
                son_dt = datetime.strptime(son_yayin[:19], "%Y-%m-%d %H:%M:%S")
                hours_diff = (datetime.now() - son_dt).total_seconds() / 3600
                if hours_diff > 48:
                    existing = any(a.get("tip") == "paylasim_yok" and a.get("tarih", "")[:10] == _today() for a in alerts)
                    if not existing:
                        new_alerts.append({
                            "id": _new_id("alert"),
                            "tip": "paylasim_yok",
                            "baslik": "48 Saat Paylasim Yok",
                            "mesaj": f"Son paylasim {son_yayin[:10]} tarihinde yapildi. {int(hours_diff)} saat gecti.",
                            "seviye": "warning",
                            "tarih": _now(),
                            "okundu": False,
                        })
            except Exception:
                pass
    else:
        existing = any(a.get("tip") == "paylasim_yok" and a.get("tarih", "")[:10] == _today() for a in alerts)
        if not existing:
            new_alerts.append({
                "id": _new_id("alert"),
                "tip": "paylasim_yok",
                "baslik": "Henuz Paylasim Yok",
                "mesaj": "Hic paylasim yapilmadi. İlk paylasiminizi olusturun!",
                "seviye": "info",
                "tarih": _now(),
                "okundu": False,
            })

    # 2. Token suresi dolmak uzere
    for acc in accounts:
        if acc.get("status") == "connected" and acc.get("token_expires"):
            try:
                exp_dt = datetime.strptime(acc["token_expires"], "%Y-%m-%d %H:%M:%S")
                days_left = (exp_dt - datetime.now()).days
                if 0 < days_left < 7:
                    plat_label = PLATFORM_MAP.get(acc["platform"], {}).get("label", acc["platform"])
                    existing = any(a.get("tip") == "token_exp" and a.get("platform") == acc["platform"]
                                   and a.get("tarih", "")[:10] == _today() for a in alerts)
                    if not existing:
                        new_alerts.append({
                            "id": _new_id("alert"),
                            "tip": "token_exp",
                            "platform": acc["platform"],
                            "baslik": f"{plat_label} Token Suresi Azaliyor",
                            "mesaj": f"{plat_label} token suresi {days_left} gun icinde dolacak.",
                            "seviye": "warning",
                            "tarih": _now(),
                            "okundu": False,
                        })
                elif days_left <= 0:
                    plat_label = PLATFORM_MAP.get(acc["platform"], {}).get("label", acc["platform"])
                    existing = any(a.get("tip") == "token_exp" and a.get("platform") == acc["platform"]
                                   and a.get("tarih", "")[:10] == _today() for a in alerts)
                    if not existing:
                        new_alerts.append({
                            "id": _new_id("alert"),
                            "tip": "token_exp",
                            "platform": acc["platform"],
                            "baslik": f"{plat_label} Token Suresi Doldu!",
                            "mesaj": f"{plat_label} token suresi doldu. Lutfen yenileyin.",
                            "seviye": "error",
                            "tarih": _now(),
                            "okundu": False,
                        })
            except Exception:
                pass

    # 3. Yayin hatasi
    failed = [p for p in posts if p.get("status") == "PUBLISH_FAILED"]
    for fp in failed:
        existing = any(a.get("tip") == "yayin_hata" and a.get("post_id") == fp["id"] for a in alerts)
        if not existing:
            new_alerts.append({
                "id": _new_id("alert"),
                "tip": "yayin_hata",
                "post_id": fp["id"],
                "baslik": "Yayin Hatasi",
                "mesaj": f"Paylasim '{fp.get('metin', '')[:30]}...' yayinlanamadi.",
                "seviye": "error",
                "tarih": _now(),
                "okundu": False,
            })

    # Yeni uyarilari kaydet
    if new_alerts:
        alerts.extend(new_alerts)
        _save_alerts(alerts)

    # Ozet
    okunmamis = len([a for a in alerts if not a.get("okundu")])
    errors = len([a for a in alerts if a.get("seviye") == "error"])
    warnings = len([a for a in alerts if a.get("seviye") == "warning"])

    styled_stat_row([
        ("Toplam Uyari", str(len(alerts)), "#64748b", "🔔"),
        ("Okunmamis", str(okunmamis), "#f59e0b", "📬"),
        ("Hata", str(errors), "#ef4444", "❌"),
        ("Uyari", str(warnings), "#f59e0b", "⚠️"),
    ])
    st.markdown("")

    # Tumu okundu butonu
    if okunmamis > 0:
        if st.button("Tümünu Okundu Isaretle", key="smm_read_all_alerts"):
            for a in alerts:
                a["okundu"] = True
            _save_alerts(alerts)
            st.success("Tüm uyarilar okundu olarak isaretlendi.")
            st.rerun()

    if not alerts:
        st.success("Aktif uyari yok. Her sey yolunda!")
        return

    # Uyari listesi
    seviye_icons = {"error": "🔴", "warning": "🟡", "info": "🔵", "success": "🟢"}
    seviye_colors = {"error": "#dc2626", "warning": "#f59e0b", "info": "#2563eb", "success": "#22c55e"}

    for alert in sorted(alerts, key=lambda x: x.get("tarih", ""), reverse=True):
        seviye = alert.get("seviye", "info")
        icon = seviye_icons.get(seviye, "🔵")
        color = seviye_colors.get(seviye, "#2563eb")
        okundu = alert.get("okundu", False)
        bg = "#ffffff" if okundu else f"{color}08"

        st.markdown(f"""<div style="background:{bg};border:1px solid #e2e8f0;
        border-radius:12px;padding:14px;margin-bottom:8px;border-left:4px solid {color}">
        <div style="display:flex;justify-content:space-between;align-items:center">
        <div>
        <span style="font-size:1rem">{icon}</span>
        <span style="font-weight:700;color:#0B0F19;margin-left:8px">{alert.get('baslik', '')}</span>
        </div>
        <span style="font-size:0.75rem;color:#94a3b8">{alert.get('tarih', '')}</span>
        </div>
        <div style="margin-top:6px;color:#475569;font-size:0.85rem">{alert.get('mesaj', '')}</div>
        </div>""", unsafe_allow_html=True)

        if not okundu:
            if st.button("Okundu", key=f"smm_alert_read_{alert['id']}"):
                for a in alerts:
                    if a["id"] == alert["id"]:
                        a["okundu"] = True
                        break
                _save_alerts(alerts)
                st.rerun()

    # Gecmisi temizle
    st.markdown("---")
    if st.button("Okunmus Uyarilari Temizle", key="smm_clear_read_alerts"):
        alerts = [a for a in alerts if not a.get("okundu")]
        _save_alerts(alerts)
        st.success("Okunmus uyarilar temizlendi.")
        st.rerun()


# ===================== 9. TAKVIM V2 (iyilestirilmis — #8) =====================

def _render_takvim_v2():
    """Gelistirilmis takvim — gunluk/haftalik/aylik gorunum + en iyi saat onerisi (#6, #8)."""
    styled_section("Icerik Takvimi", "#0d9488")

    posts = _posts()
    sstore = get_smm_store()

    gorunum = st.radio("Gorunum", ["Aylik", "Haftalik", "Gunluk"], horizontal=True, key="smm_takvim_gorunum")

    today = datetime.now()

    if gorunum == "Aylik":
        # Mevcut _render_takvim mantigi
        tc1, tc2 = st.columns([1, 1])
        with tc1:
            sec_yil = st.selectbox("Yil", list(range(today.year - 1, today.year + 2)),
                                    index=1, key="smm_takvim_yil_v2")
        with tc2:
            sec_ay = st.selectbox("Ay", list(range(1, 13)), index=today.month - 1, key="smm_takvim_ay_v2",
                                   format_func=lambda x: ["", "Ocak", "Subat", "Mart", "Nisan", "Mayis",
                                                           "Haziran", "Temmuz", "Agustos", "Eylul", "Ekim",
                                                           "Kasim", "Aralik"][x])

        cal_obj = calendar.Calendar(firstweekday=0)
        month_days = cal_obj.monthdayscalendar(sec_yil, sec_ay)

        # Gune gore paylasim haritasi
        day_map = {}
        for p in posts:
            tarih = p.get("planlanan_tarih", "") or p.get("yayin_tarihi", "") or p.get("created_at", "")
            if not tarih:
                continue
            try:
                dt = datetime.strptime(tarih[:10], "%Y-%m-%d")
                if dt.year == sec_yil and dt.month == sec_ay:
                    day_map.setdefault(dt.day, []).append(p)
            except ValueError:
                continue

        # Baslik satiri
        gun_baslik = st.columns(7)
        for i, g in enumerate(["Pzt", "Sal", "Car", "Per", "Cum", "Cmt", "Paz"]):
            with gun_baslik[i]:
                st.markdown(f"<div style='text-align:center;font-weight:700;color:#64748b;font-size:0.8rem'>{g}</div>",
                            unsafe_allow_html=True)

        for week in month_days:
            cols = st.columns(7)
            for i, day in enumerate(week):
                with cols[i]:
                    if day == 0:
                        st.write("")
                    else:
                        day_posts = day_map.get(day, [])
                        is_today = (day == today.day and sec_ay == today.month and sec_yil == today.year)
                        bg = "#dbeafe" if is_today else ("#f0fdf4" if day_posts else "#f8fafc")
                        border = "2px solid #3b82f6" if is_today else "1px solid #e2e8f0"
                        cnt = len(day_posts)
                        badge = f"<span style='background:#10b981;color:#fff;border-radius:50%;padding:1px 6px;font-size:0.7rem;margin-left:4px'>{cnt}</span>" if cnt > 0 else ""
                        st.markdown(f"""<div style="background:{bg};border:{border};border-radius:8px;
                            padding:6px;min-height:50px;text-align:center">
                            <div style="font-weight:{'800' if is_today else '600'};font-size:0.9rem;
                            color:{'#2563eb' if is_today else '#334155'}">{day}{badge}</div>
                        </div>""", unsafe_allow_html=True)

    elif gorunum == "Haftalik":
        # Haftalik gorunum
        hafta_baslangic = today - timedelta(days=today.weekday())
        st.caption(f"Hafta: {hafta_baslangic.strftime('%d/%m')} - {(hafta_baslangic + timedelta(days=6)).strftime('%d/%m/%Y')}")

        cols = st.columns(7)
        for i in range(7):
            gun_dt = hafta_baslangic + timedelta(days=i)
            gun_str = gun_dt.strftime("%Y-%m-%d")
            gun_posts = [p for p in posts if (p.get("planlanan_tarih", "") or p.get("yayin_tarihi", ""))[:10] == gun_str]
            gun_adlari = ["Pzt", "Sal", "Car", "Per", "Cum", "Cmt", "Paz"]

            with cols[i]:
                is_today = gun_dt.date() == today.date()
                bg = "#dbeafe" if is_today else "#f8fafc"
                st.markdown(f"""<div style="background:{bg};border-radius:10px;padding:10px;
                    min-height:120px;border:{'2px solid #3b82f6' if is_today else '1px solid #e2e8f0'}">
                    <div style="font-weight:700;text-align:center;color:#334155">{gun_adlari[i]}</div>
                    <div style="text-align:center;font-size:0.8rem;color:#64748b">{gun_dt.strftime('%d/%m')}</div>
                </div>""", unsafe_allow_html=True)
                for gp in gun_posts[:3]:
                    status_info = STATUS_MAP.get(gp.get("status", ""), {"label": "?", "color": "#94a3b8"})
                    plat_icons = " ".join(PLATFORM_MAP.get(pk, {}).get("icon", "") for pk in gp.get("platformlar", []))
                    st.markdown(f"""<div style="background:{status_info['color']}15;border-left:3px solid {status_info['color']};
                        border-radius:0 6px 6px 0;padding:4px 8px;margin:4px 0;font-size:0.75rem">
                        {plat_icons} {gp.get('metin', '')[:25]}...
                    </div>""", unsafe_allow_html=True)

    else:
        # Gunluk gorunum
        sec_gun = st.date_input("Gun Sec", value=today.date(), key="smm_takvim_gun")
        gun_str = sec_gun.strftime("%Y-%m-%d")
        gun_posts = [p for p in posts if (p.get("planlanan_tarih", "") or p.get("yayin_tarihi", ""))[:10] == gun_str]

        if not gun_posts:
            st.info(f"{sec_gun.strftime('%d/%m/%Y')} tarihinde planlanmis icerik yok.")
        else:
            for gp in gun_posts:
                status_info = STATUS_MAP.get(gp.get("status", ""), {"label": "?", "color": "#94a3b8"})
                plat_badges = " ".join(_platform_badge(pk) for pk in gp.get("platformlar", []))
                saat = ""
                tarih_raw = gp.get("planlanan_tarih", "") or gp.get("yayin_tarihi", "")
                if len(tarih_raw) > 10:
                    saat = tarih_raw[11:16]
                st.markdown(f"""<div style="background:white;border:1px solid #e2e8f0;border-radius:12px;
                    padding:14px;margin-bottom:8px;border-left:4px solid {status_info['color']}">
                    <div style="display:flex;justify-content:space-between">
                    <div>{plat_badges} <span style="font-weight:700">{saat}</span></div>
                    <div style="background:{status_info['color']};color:#fff;padding:2px 10px;
                    border-radius:12px;font-size:0.75rem">{status_info['label']}</div>
                    </div>
                    <div style="margin-top:6px;color:#334155">{gp.get('metin', '')[:100]}</div>
                </div>""", unsafe_allow_html=True)

    # En iyi saat onerisi (#6)
    st.markdown("---")
    styled_section("En Iyi Paylasim Saatleri", "#f59e0b")
    st.caption("Engagement verilerinize dayali otomatik oneri. Veri yoksa sektordeki en iyi saatler gosterilir.")

    oneri_plat = st.selectbox("Platform", [p[2] for p in PLATFORMLAR], key="smm_oneri_plat")
    plat_key = next((p[0] for p in PLATFORMLAR if p[2] == oneri_plat), "instagram")

    oneriler = EngelliSaatOnerici.hesapla(posts, plat_key)
    if oneriler:
        cols = st.columns(min(len(oneriler), 5))
        for idx, oneri in enumerate(oneriler[:5]):
            with cols[idx]:
                kaynak = "📊 Veri" if oneri.get("kaynak") == "veri" else "📌 Varsayilan"
                eng = oneri.get("ort_engagement", "")
                eng_str = f"<br><span style='font-size:0.7rem;color:#64748b'>Ort: {eng}</span>" if eng else ""
                st.markdown(f"""<div style="background:#fef3c7;border:1px solid #f59e0b40;
                    border-radius:10px;padding:12px;text-align:center">
                    <div style="font-weight:800;color:#92400e">{oneri['gun']}</div>
                    <div style="font-size:1.2rem;font-weight:700;color:#d97706">{oneri['saat']}</div>
                    <div style="font-size:0.7rem;color:#94a3b8">{kaynak}</div>{eng_str}
                </div>""", unsafe_allow_html=True)


# ===================== 10. GELEN KUTUSU V2 (sentiment — #13) =====================

def _render_gelen_kutusu_v2():
    """Gelen kutusu — sentiment analizi entegreli (#13)."""
    styled_section("Gelen Kutusu", "#1877F2")

    inbox = _inbox()
    sstore = get_smm_store()

    # API'den cekme
    if st.button("Yorumlari ve Etiketlemeleri Cek (API)", key="smm_fetch_inbox_v2", type="primary"):
        _fetch_real_inbox()
        inbox = _inbox()

    # Toplu sentiment analizi
    has_unanalyzed = any(not m.get("sentiment") or m.get("sentiment") == "" for m in inbox if m.get("metin"))
    if has_unanalyzed:
        if st.button("Sentiment Analizi Calistir", key="smm_run_sentiment"):
            for msg in inbox:
                if msg.get("metin") and (not msg.get("sentiment") or msg.get("sentiment") == ""):
                    result = SentimentAnalyzer.analyze(msg["metin"])
                    msg["sentiment"] = result["label"]
                    msg["sentiment_skor"] = result["skor"]
            _save_inbox(inbox)
            st.success("Sentiment analizi tamamlandi!")
            st.rerun()

    # Ozet
    okunmamis = len([m for m in inbox if not m.get("okundu")])
    pozitif_c = len([m for m in inbox if m.get("sentiment") == "pozitif"])
    negatif_c = len([m for m in inbox if m.get("sentiment") == "negatif"])

    styled_stat_row([
        ("Toplam", str(len(inbox)), "#64748b", "📬"),
        ("Okunmamis", str(okunmamis), "#f59e0b", "📩"),
        ("Pozitif", str(pozitif_c), "#10b981", "😊"),
        ("Negatif", str(negatif_c), "#ef4444", "😞"),
    ])
    st.markdown("")

    # Filtre
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        filter_plat = st.selectbox("Platform", ["Tumu"] + [p[2] for p in PLATFORMLAR], key="smm_inbox_filter_v2")
    with fc2:
        filter_sentiment = st.selectbox("Sentiment", ["Tumu", "pozitif", "notr", "negatif"], key="smm_inbox_sent_filter")
    with fc3:
        filter_tip = st.selectbox("Tip", ["Tumu", "yorum", "mention", "dm"], key="smm_inbox_tip_filter")

    filtered = inbox
    if filter_plat != "Tumu":
        plat_key = next((p[0] for p in PLATFORMLAR if p[2] == filter_plat), "")
        filtered = [m for m in filtered if m.get("platform") == plat_key]
    if filter_sentiment != "Tumu":
        filtered = [m for m in filtered if m.get("sentiment") == filter_sentiment]
    if filter_tip != "Tumu":
        filtered = [m for m in filtered if m.get("tip") == filter_tip]

    if not filtered:
        st.info("Gelen kutusu bos.")
        return

    # Test mesaji ekleme
    with st.expander("Test Mesaji Ekle (Simulasyon)"):
        sim_plat = st.selectbox("Platform", [p[2] for p in PLATFORMLAR], key="smm_sim_plat_v2")
        sim_tip = st.selectbox("Tip", ["yorum", "mention", "dm"], key="smm_sim_tip_v2")
        sim_user = st.text_input("Kullanici", key="smm_sim_user_v2")
        sim_metin = st.text_area("Mesaj", key="smm_sim_metin_v2")
        if st.button("Ekle", key="smm_sim_add_v2", type="primary"):
            if sim_user and sim_metin:
                plat_key = next((p[0] for p in PLATFORMLAR if p[2] == sim_plat), "instagram")
                sentiment = SentimentAnalyzer.analyze(sim_metin)
                inbox.append({
                    "id": _new_id("inb"),
                    "platform": plat_key,
                    "tip": sim_tip,
                    "kullanici": sim_user,
                    "metin": sim_metin,
                    "tarih": _now(),
                    "okundu": False,
                    "yanitlandi": False,
                    "sentiment": sentiment["label"],
                    "sentiment_skor": sentiment["skor"],
                })
                _save_inbox(inbox)
                st.success("Mesaj eklendi.")
                st.rerun()

    # Mesaj listesi
    sentiment_emoji = {"pozitif": "😊", "notr": "😐", "negatif": "😞"}
    sentiment_color = {"pozitif": "#10b981", "notr": "#94a3b8", "negatif": "#ef4444"}

    for msg in sorted(filtered, key=lambda x: x.get("tarih", ""), reverse=True):
        p_info = PLATFORM_MAP.get(msg.get("platform", ""), {"icon": "🌐", "label": "?", "color": "#64748b"})
        okundu_icon = "📩" if not msg.get("okundu") else "📧"
        tip_label = {"yorum": "Yorum", "mention": "Etiketleme", "dm": "Mesaj"}.get(msg.get("tip", ""), msg.get("tip", ""))
        sent = msg.get("sentiment", "notr")
        sent_icon = sentiment_emoji.get(sent, "😐")
        sent_clr = sentiment_color.get(sent, "#94a3b8")

        bg_color = "#eff6ff" if not msg.get("okundu") else "#ffffff"

        with st.expander(f"{okundu_icon} @{msg.get('kullanici', '')} | {p_info['label']} | {tip_label} | {sent_icon} {sent}"):
            st.markdown(f"**Mesaj:** {msg.get('metin', '')}")
            st.markdown(f"**Tarih:** {msg.get('tarih', '')} | **Sentiment:** "
                        f"<span style='color:{sent_clr};font-weight:700'>{sent_icon} {sent}</span> "
                        f"(skor: {msg.get('sentiment_skor', 0):.2f})", unsafe_allow_html=True)

            mc1, mc2, mc3 = st.columns(3)
            with mc1:
                if not msg.get("okundu"):
                    if st.button("Okundu", key=f"smm_read_v2_{msg['id']}"):
                        for m in inbox:
                            if m["id"] == msg["id"]:
                                m["okundu"] = True
                                break
                        _save_inbox(inbox)
                        st.rerun()
            with mc2:
                yanit = st.text_input("Yanit", key=f"smm_reply_v2_{msg['id']}", label_visibility="collapsed",
                                       placeholder="Yanit yaz...")
                if yanit and st.button("Gonder", key=f"smm_send_reply_v2_{msg['id']}"):
                    for m in inbox:
                        if m["id"] == msg["id"]:
                            m["yanitlandi"] = True
                            m["yanit_metin"] = yanit
                            break
                    _save_inbox(inbox)
                    st.success("Yanit gonderildi.")
                    st.rerun()


# ===================== 11. AI ICERIK ASISTANI (#4) =====================

def _render_ai_asistan():
    """AI destekli icerik olusturma, caption/hashtag onerisi, A/B test, coklu dil (#4, #12)."""
    if not check_smm_yetki("ai_asistan"):
        st.warning("Bu ozellik icin AI Asistan yetkisi gereklidir.")
        return

    styled_section("AI Icerik Asistani", "#8b5cf6")

    ai_t1, ai_t2, ai_t3, ai_t4 = st.tabs([
        "  📝 Caption Uretici  ", "  #️⃣ Hashtag Onerici  ",
        "  🔄 A/B Test  ", "  🌐 Ceviri (#12)  ",
    ])

    # --- Caption Uretici ---
    with ai_t1:
        st.markdown("##### AI ile Caption Olustur")
        konu = st.text_input("Konu/Etkinlik *", placeholder="Orn: Bilim fuari, 23 Nisan kutlamasi...", key="smm_ai_konu")
        ai_c1, ai_c2 = st.columns(2)
        with ai_c1:
            ton = st.selectbox("Ton", ["Resmi", "Samimi", "Enerjik", "Bilgilendirici", "Ilham Verici"],
                               key="smm_ai_ton")
            platform = st.selectbox("Platform", [p[2] for p in PLATFORMLAR], key="smm_ai_plat")
        with ai_c2:
            uzunluk = st.selectbox("Uzunluk", ["Kisa (1-2 cumle)", "Orta (3-4 cumle)", "Uzun (5+ cumle)"],
                                    key="smm_ai_uzunluk")
            emoji_kullan = st.checkbox("Emoji kullan", value=True, key="smm_ai_emoji")

        if st.button("Caption Uret", type="primary", key="smm_ai_gen_caption"):
            if not konu:
                st.error("Konu giriniz.")
            else:
                with st.spinner("AI caption uretiyor..."):
                    try:
                        from openai import OpenAI
                        client = OpenAI()
                        plat_key = next((p[0] for p in PLATFORMLAR if p[2] == platform), "instagram")
                        karakter_limit = PLATFORM_KARAKTER_LIMITI.get(plat_key, 2200)

                        prompt = (
                            f"Bir egitim kurumunun sosyal medya yoneticisisin. "
                            f"{platform} platformu icin, '{konu}' konusunda bir paylasim metni yaz.\n"
                            f"Ton: {ton}\nUzunluk: {uzunluk}\n"
                            f"Karakter limiti: {karakter_limit}\n"
                            f"{'Emoji kullan.' if emoji_kullan else 'Emoji kullanma.'}\n"
                            f"Sadece paylasim metnini yaz, baska aciklama ekleme."
                        )

                        resp = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{"role": "user", "content": prompt}],
                            max_tokens=500,
                            temperature=0.8,
                        )
                        caption = resp.choices[0].message.content.strip()
                        st.text_area("Uretilen Caption", value=caption, height=150, key="smm_ai_result")
                        st.caption(f"{len(caption)} karakter | Limit: {karakter_limit}")

                        if st.button("Yeni Paylasim Olarak Kullan", key="smm_ai_use"):
                            posts = _posts()
                            posts.append({
                                "id": _new_id("post"),
                                "metin": caption,
                                "platformlar": [plat_key],
                                "hashtagler": [],
                                "status": "DRAFT",
                                "ai_oneriler": {"kaynak": "caption_uretici", "konu": konu, "ton": ton},
                                "created_at": _now(),
                                "updated_at": _now(),
                            })
                            _save_posts(posts)
                            st.success("Taslak olarak kaydedildi!")
                    except ImportError:
                        st.error("OpenAI kutuphanesi yuklu degil. `pip install openai` calistirin.")
                    except Exception as e:
                        st.error(f"AI hatasi: {e}")

    # --- Hashtag Onerici ---
    with ai_t2:
        st.markdown("##### AI ile Hashtag Onerisi")
        ht_metin = st.text_area("Paylasim Metni", height=100, key="smm_ai_ht_metin",
                                 placeholder="Paylasim metninizi yapisitirin...")
        ht_adet = st.slider("Hashtag Sayisi", 3, 15, 8, key="smm_ai_ht_adet")

        if st.button("Hashtag Oner", type="primary", key="smm_ai_gen_ht"):
            if not ht_metin:
                st.error("Metin giriniz.")
            else:
                with st.spinner("Hashtagler oneriliyor..."):
                    try:
                        from openai import OpenAI
                        client = OpenAI()
                        resp = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{
                                "role": "user",
                                "content": (
                                    f"Asagidaki sosyal medya paylasimi icin {ht_adet} adet Turkce "
                                    f"hashtag oner. Sadece hashtag'leri yaz (# ile baslayan), "
                                    f"birer satira:\n\n{ht_metin}"
                                ),
                            }],
                            max_tokens=200,
                            temperature=0.7,
                        )
                        hashtagler = resp.choices[0].message.content.strip()
                        st.code(hashtagler, language=None)
                    except ImportError:
                        st.error("OpenAI kutuphanesi yuklu degil.")
                    except Exception as e:
                        st.error(f"Hata: {e}")

    # --- A/B Test ---
    with ai_t3:
        st.markdown("##### A/B Test Caption Uretici")
        st.caption("Ayni konu icin 2 farkli caption uretir — hangisinin daha iyi performans gosterecegini test edin.")
        ab_konu = st.text_input("Konu", key="smm_ai_ab_konu", placeholder="Kayit donemi basladi...")
        if st.button("A/B Ciftini Uret", type="primary", key="smm_ai_gen_ab"):
            if not ab_konu:
                st.error("Konu giriniz.")
            else:
                with st.spinner("A/B test captionlari uretiliyor..."):
                    try:
                        from openai import OpenAI
                        client = OpenAI()
                        resp = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{
                                "role": "user",
                                "content": (
                                    f"Bir okul sosyal medya paylasimi icin '{ab_konu}' konusunda "
                                    f"2 farkli versiyon yaz. Birincisi resmi ve bilgilendirici, "
                                    f"ikincisi samimi ve enerjik olsun. "
                                    f"Her birini 'VERSIYON A:' ve 'VERSIYON B:' basliklariyla ayir."
                                ),
                            }],
                            max_tokens=600,
                            temperature=0.9,
                        )
                        st.markdown(resp.choices[0].message.content.strip())
                    except ImportError:
                        st.error("OpenAI kutuphanesi yuklu degil.")
                    except Exception as e:
                        st.error(f"Hata: {e}")

    # --- Coklu Dil Cevirisi (#12) ---
    with ai_t4:
        st.markdown("##### Coklu Dil Cevirisi")
        st.caption("Paylasim metninizi birden fazla dile cevirin.")
        cev_metin = st.text_area("Turkce Metin", height=100, key="smm_ai_cev_metin")
        cev_diller = st.multiselect("Hedef Diller", ["English", "Deutsch", "Francais", "Espanol", "Arabca"],
                                     default=["English"], key="smm_ai_cev_dil")
        if st.button("Cevir", type="primary", key="smm_ai_cev_btn"):
            if not cev_metin:
                st.error("Metin giriniz.")
            else:
                with st.spinner("Cevriliyor..."):
                    try:
                        from openai import OpenAI
                        client = OpenAI()
                        resp = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{
                                "role": "user",
                                "content": (
                                    f"Asagidaki sosyal medya metnini su dillere cevir: {', '.join(cev_diller)}. "
                                    f"Her cevitiyi dil basligi ile ayir.\n\n{cev_metin}"
                                ),
                            }],
                            max_tokens=800,
                            temperature=0.3,
                        )
                        st.markdown(resp.choices[0].message.content.strip())
                    except ImportError:
                        st.error("OpenAI kutuphanesi yuklu degil.")
                    except Exception as e:
                        st.error(f"Hata: {e}")


# ===================== 12. RAKIP ANALIZI (#5) =====================

def _render_rakip_analizi():
    """Rakip okullarin sosyal medya takibi (#5)."""
    if not check_smm_yetki("rakip_analiz"):
        st.warning("Rakip Analizi yetkisi gereklidir.")
        return

    styled_section("Rakip Analizi", "#ef4444")
    sstore = get_smm_store()
    rakipler = sstore.get_rakipler()

    rm1, rm2 = st.columns(2)
    with rm1:
        st.metric("Takip Edilen Rakip", str(len(rakipler)))
    with rm2:
        st.metric("Toplam Metrik Kaydi", str(sum(len(r.metrikler) for r in rakipler)))

    # Yeni rakip ekleme
    with st.expander("➕ Yeni Rakip Ekle", expanded=False):
        with st.form("smm_rakip_form", clear_on_submit=True):
            rf1, rf2 = st.columns(2)
            with rf1:
                r_kurum = st.text_input("Kurum Adi *", key="smm_rak_kurum")
                r_plat = st.selectbox("Platform", [p[2] for p in PLATFORMLAR], key="smm_rak_plat")
            with rf2:
                r_url = st.text_input("Hesap URL", key="smm_rak_url")
                r_hesap = st.text_input("Hesap Adi (@)", key="smm_rak_hesap")
            r_notlar = st.text_area("Notlar", key="smm_rak_notlar", height=68)
            if st.form_submit_button("Kaydet", type="primary"):
                if not r_kurum:
                    st.error("Kurum adi zorunludur.")
                else:
                    plat_key = next((p[0] for p in PLATFORMLAR if p[2] == r_plat), "instagram")
                    yeni_rak = Rakip(kurum_adi=r_kurum, platform=plat_key,
                                     hesap_url=r_url, hesap_adi=r_hesap, notlar=r_notlar)
                    sstore.add_object("rakipler", yeni_rak)
                    st.success(f"Rakip '{r_kurum}' eklendi!")
                    st.rerun()

    if not rakipler:
        styled_info_banner("Henuz rakip eklenmemis.", "info")
        return

    # Rakip listesi + metrik girisi
    for rak in rakipler:
        p_info = PLATFORM_MAP.get(rak.platform, {"icon": "🌐", "label": "?", "color": "#64748b"})
        son = rak.son_metrik

        with st.expander(f"{p_info['icon']} {rak.kurum_adi} | @{rak.hesap_adi} | "
                         f"Takipci: {son.get('takipci', '-')}"):
            st.markdown(f"**Platform:** {p_info['label']} | **URL:** {rak.hesap_url or '-'} | **Notlar:** {rak.notlar or '-'}")

            # Metrik gecmisi
            if rak.metrikler:
                import pandas as _pd
                df_met = _pd.DataFrame(rak.metrikler)
                st.dataframe(df_met, use_container_width=True, hide_index=True)

                # Takipci trendi
                if "takipci" in df_met.columns and len(df_met) > 1:
                    try:
                        fig = px.line(df_met, x="tarih", y="takipci", title=f"{rak.kurum_adi} Takipci Trendi")
                        fig.update_layout(height=250, margin=dict(t=30, b=20))
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception:
                        pass

            # Yeni metrik girisi
            with st.form(f"smm_rak_metrik_{rak.id}"):
                st.markdown("**Yeni Metrik Girisi**")
                mfc1, mfc2, mfc3 = st.columns(3)
                with mfc1:
                    m_takipci = st.number_input("Takipci", min_value=0, key=f"smm_rak_m_tak_{rak.id}")
                    m_paylasim = st.number_input("Paylasim Sayisi", min_value=0, key=f"smm_rak_m_pay_{rak.id}")
                with mfc2:
                    m_begeni = st.number_input("Ort. Begeni", min_value=0, key=f"smm_rak_m_beg_{rak.id}")
                    m_yorum = st.number_input("Ort. Yorum", min_value=0, key=f"smm_rak_m_yor_{rak.id}")
                with mfc3:
                    m_eng = st.number_input("Engagement Rate (%)", min_value=0.0, step=0.1,
                                             key=f"smm_rak_m_eng_{rak.id}")
                if st.form_submit_button("Metrik Kaydet"):
                    yeni_metrik = {
                        "tarih": _today(),
                        "takipci": m_takipci,
                        "paylasim_sayisi": m_paylasim,
                        "begeni_ort": m_begeni,
                        "yorum_ort": m_yorum,
                        "engagement_rate": m_eng,
                    }
                    tum = sstore.load_list("rakipler")
                    for r in tum:
                        if r.get("id") == rak.id:
                            r.setdefault("metrikler", []).append(yeni_metrik)
                    sstore.save_list("rakipler", tum)
                    st.success("Metrik kaydedildi!")
                    st.rerun()

            # Sil
            if st.button("🗑️ Rakibi Sil", key=f"smm_rak_sil_{rak.id}"):
                sstore.delete_object("rakipler", rak.id)
                st.success("Rakip silindi!")
                st.rerun()


# ===================== 13. HASHTAG PERFORMANS TAKIBI (#14) =====================

def _render_hashtag_takibi():
    """Hashtag performans analizi (#14)."""
    styled_section("Hashtag Performans Takibi", "#6366f1")

    posts = _posts()
    hashtag_list = HashtagTracker.guncelle(posts)

    if not hashtag_list:
        styled_info_banner("Yayinlanmis paylasim veya hashtag verisi bulunamadi.", "info")
        return

    hm1, hm2, hm3 = st.columns(3)
    with hm1:
        st.metric("Toplam Hashtag", str(len(hashtag_list)))
    with hm2:
        en_iyi = hashtag_list[0] if hashtag_list else None
        st.metric("En Iyi Hashtag", en_iyi.hashtag if en_iyi else "-")
    with hm3:
        st.metric("Ort. Etkilesim", f"{sum(h.ort_etkilesim for h in hashtag_list) / len(hashtag_list):.1f}" if hashtag_list else "0")

    # Tablo
    import pandas as _pd
    rows = []
    for h in hashtag_list:
        rows.append({
            "Hashtag": h.hashtag,
            "Kullanim": h.kullanim_sayisi,
            "Begeni": h.toplam_begeni,
            "Yorum": h.toplam_yorum,
            "Goruntulenme": h.toplam_goruntulenme,
            "Ort. Etkilesim": round(h.ort_etkilesim, 1),
            "Platformlar": ", ".join(h.platformlar),
        })
    df_ht = _pd.DataFrame(rows)
    st.dataframe(df_ht, use_container_width=True, hide_index=True)

    # Grafik
    if len(hashtag_list) > 1:
        try:
            top10 = df_ht.head(10)
            fig = px.bar(top10, x="Hashtag", y="Ort. Etkilesim",
                         color="Ort. Etkilesim",
                         color_continuous_scale=["#94a3b8", "#6366f1"],
                         title="Top 10 Hashtag (Ort. Etkilesim)")
            fig.update_layout(height=300, margin=dict(t=30, b=20))
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            pass


# ===================== 14. MARKA AYARLARI (#11) =====================

def _render_marka_ayarlari():
    """Kurum marka tutarliligi ayarlari ve kontrol (#11)."""
    if not check_smm_yetki("marka_ayar"):
        st.warning("Marka Ayarlari yetkisi gereklidir.")
        return

    styled_section("Marka Tutarliligi Ayarlari", "#d97706")
    sstore = get_smm_store()
    marka = sstore.get_marka_ayar()

    # Ayar formu
    with st.form("smm_marka_form"):
        mf1, mf2 = st.columns(2)
        with mf1:
            m_kurum = st.text_input("Kurum Adi", value=marka.kurum_adi, key="smm_mrk_kurum")
            m_renk1 = st.color_picker("Birincil Renk", value=marka.renk_birincil, key="smm_mrk_renk1")
            m_renk2 = st.color_picker("Ikincil Renk", value=marka.renk_ikincil, key="smm_mrk_renk2")
        with mf2:
            m_slogan = st.text_input("Slogan", value=marka.slogan, key="smm_mrk_slogan")
            m_min = st.number_input("Min. Karakter Sayisi", min_value=0, value=marka.min_karakter, key="smm_mrk_min")
            m_logo = st.text_input("Logo Dosya Yolu", value=marka.logo_path, key="smm_mrk_logo")

        m_zorunlu_ht = st.text_input("Zorunlu Hashtagler (virgul ile)",
                                      value=", ".join(marka.zorunlu_hashtagler),
                                      key="smm_mrk_ht")
        m_yasak = st.text_input("Yasak Kelimeler (virgul ile)",
                                 value=", ".join(marka.yasak_kelimeler),
                                 key="smm_mrk_yasak")

        if st.form_submit_button("Kaydet", type="primary"):
            marka.kurum_adi = m_kurum
            marka.renk_birincil = m_renk1
            marka.renk_ikincil = m_renk2
            marka.slogan = m_slogan
            marka.min_karakter = m_min
            marka.logo_path = m_logo
            marka.zorunlu_hashtagler = [h.strip() for h in m_zorunlu_ht.split(",") if h.strip()]
            marka.yasak_kelimeler = [k.strip() for k in m_yasak.split(",") if k.strip()]
            sstore.save_marka_ayar(marka)
            st.success("Marka ayarlari kaydedildi!")
            st.rerun()

    # Test
    st.markdown("---")
    styled_section("Marka Kontrol Testi", "#f59e0b")
    test_metin = st.text_area("Test Metni", key="smm_mrk_test_metin", height=80)
    test_ht = st.text_input("Hashtagler (virgul ile)", key="smm_mrk_test_ht")
    test_plat = st.multiselect("Platformlar", [p[0] for p in PLATFORMLAR],
                                format_func=lambda x: PLATFORM_MAP.get(x, {}).get("label", x),
                                key="smm_mrk_test_plat")

    if st.button("Kontrol Et", type="primary", key="smm_mrk_test_btn"):
        if not test_metin:
            st.error("Test metni giriniz.")
        else:
            hashtagler = [h.strip() for h in test_ht.split(",") if h.strip()]
            kontrolcu = MarkaKontrolcu(marka)
            sonuc = kontrolcu.kontrol_et(test_metin, hashtagler, test_plat)

            skor = sonuc["skor"]
            skor_renk = "#10b981" if skor >= 80 else ("#f59e0b" if skor >= 50 else "#ef4444")
            st.markdown(f"""<div style="text-align:center;padding:16px;background:{skor_renk}15;
                border:2px solid {skor_renk};border-radius:14px;margin-bottom:12px">
                <div style="font-size:2.5rem;font-weight:800;color:{skor_renk}">{skor}/100</div>
                <div style="color:{skor_renk};font-weight:600">
                {'Marka Uyumlu' if sonuc['basarili'] else 'Uyumsuzluk Tespit Edildi'}</div>
            </div>""", unsafe_allow_html=True)

            for s in sonuc["sonuclar"]:
                icon = {"basarili": "✅", "basarisiz": "❌", "uyari": "⚠️"}.get(s["durum"], "ℹ️")
                st.markdown(f"{icon} **{s['kural']}:** {s['mesaj']}")


# ===================== 15. RAPORLAR (#7) =====================

def _render_raporlar():
    """Rapor olusturma ve export — PDF/Excel (#7)."""
    if not check_smm_yetki("rapor"):
        st.warning("Rapor yetkisi gereklidir.")
        return

    styled_section("Sosyal Medya Raporlari", "#0d9488")

    posts = _posts()
    sstore = get_smm_store()
    published = [p for p in posts if p.get("status") == "PUBLISHED"]

    rap_t1, rap_t2, rap_t3 = st.tabs([
        "  📊 Genel Ozet  ", "  📅 Donemsel Rapor  ", "  📥 Export  "
    ])

    with rap_t1:
        if not published:
            styled_info_banner("Yayinlanmis paylasim yok.", "info")
            return

        # Genel istatistikler
        total_begeni = sum(p.get("analytics", {}).get("begeni", 0) for p in published)
        total_yorum = sum(p.get("analytics", {}).get("yorum", 0) for p in published)
        total_paylasim = sum(p.get("analytics", {}).get("paylasim", 0) for p in published)
        total_goruntulenme = sum(p.get("analytics", {}).get("goruntulenme", 0) for p in published)

        styled_stat_row([
            ("Paylasim", str(len(published)), "#6366f1", "📝"),
            ("Begeni", str(total_begeni), "#ef4444", "❤️"),
            ("Yorum", str(total_yorum), "#2563eb", "💬"),
            ("Goruntulenme", str(total_goruntulenme), "#8b5cf6", "👁️"),
        ])

        # Platform dagilimi
        plat_dag = {}
        for p in published:
            for pk in p.get("platformlar", []):
                plat_dag[pk] = plat_dag.get(pk, 0) + 1
        if plat_dag:
            import pandas as _pd
            try:
                labels = [PLATFORM_MAP.get(k, {}).get("label", k) for k in plat_dag.keys()]
                fig = px.pie(names=labels, values=list(plat_dag.values()),
                             title="Platform Dagilimi")
                fig.update_layout(height=300, margin=dict(t=40, b=20))
                st.plotly_chart(fig, use_container_width=True)
            except Exception:
                pass

        # Status dagilimi
        status_dag = {}
        for p in posts:
            s = p.get("status", "DRAFT")
            status_dag[s] = status_dag.get(s, 0) + 1
        if status_dag:
            import pandas as _pd
            try:
                labels = [STATUS_MAP.get(k, {}).get("label", k) for k in status_dag.keys()]
                fig = px.bar(x=labels, y=list(status_dag.values()), title="Icerik Durum Dagilimi")
                fig.update_layout(height=300, margin=dict(t=30, b=20))
                st.plotly_chart(fig, use_container_width=True)
            except Exception:
                pass

    with rap_t2:
        rc1, rc2 = st.columns(2)
        with rc1:
            baslangic = st.date_input("Baslangic", value=datetime.now().date() - timedelta(days=30),
                                       key="smm_rap_baslangic")
        with rc2:
            bitis = st.date_input("Bitis", value=datetime.now().date(), key="smm_rap_bitis")

        donemsel = [p for p in published
                    if baslangic.isoformat() <= (p.get("yayin_tarihi", "") or p.get("created_at", ""))[:10] <= bitis.isoformat()]

        if not donemsel:
            st.info("Bu donemde yayinlanmis icerik yok.")
        else:
            d_begeni = sum(p.get("analytics", {}).get("begeni", 0) for p in donemsel)
            d_yorum = sum(p.get("analytics", {}).get("yorum", 0) for p in donemsel)

            styled_stat_row([
                ("Paylasim", str(len(donemsel)), "#6366f1", "📝"),
                ("Begeni", str(d_begeni), "#ef4444", "❤️"),
                ("Yorum", str(d_yorum), "#2563eb", "💬"),
            ])

            # Gunluk paylasim grafigi
            import pandas as _pd
            gun_map = {}
            for p in donemsel:
                tarih = (p.get("yayin_tarihi", "") or p.get("created_at", ""))[:10]
                gun_map[tarih] = gun_map.get(tarih, 0) + 1
            if gun_map:
                try:
                    df_gun = _pd.DataFrame(sorted(gun_map.items()), columns=["Tarih", "Paylasim"])
                    fig = px.line(df_gun, x="Tarih", y="Paylasim", title="Gunluk Paylasim Sayisi")
                    fig.update_layout(height=250, margin=dict(t=30, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                except Exception:
                    pass

    with rap_t3:
        st.markdown("##### Rapor Export")

        export_format = st.selectbox("Format", ["Excel (.xlsx)", "CSV"], key="smm_rap_format")

        if st.button("Rapor Olustur ve Indir", type="primary", key="smm_rap_export"):
            import pandas as _pd
            rows = []
            for p in published:
                a = p.get("analytics", {})
                rows.append({
                    "Tarih": (p.get("yayin_tarihi", "") or p.get("created_at", ""))[:10],
                    "Metin": p.get("metin", "")[:80],
                    "Platformlar": ", ".join(p.get("platformlar", [])),
                    "Begeni": a.get("begeni", 0),
                    "Yorum": a.get("yorum", 0),
                    "Paylasim": a.get("paylasim", 0),
                    "Goruntulenme": a.get("goruntulenme", 0),
                    "Hashtagler": " ".join(p.get("hashtagler", [])),
                    "Kampanya": p.get("kampanya", ""),
                })
            df_export = _pd.DataFrame(rows)

            if "Excel" in export_format:
                try:
                    import io
                    buffer = io.BytesIO()
                    with _pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                        df_export.to_excel(writer, index=False, sheet_name="Sosyal Medya Raporu")
                    st.download_button(
                        "📥 Excel Indir", data=buffer.getvalue(),
                        file_name=f"SMM_Rapor_{_today()}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="smm_dl_xlsx",
                    )
                except ImportError:
                    st.error("openpyxl yuklu degil. `pip install openpyxl` calistirin.")
            else:
                csv_data = df_export.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📥 CSV Indir", data=csv_data,
                    file_name=f"SMM_Rapor_{_today()}.csv",
                    mime="text/csv",
                    key="smm_dl_csv",
                )

        # PDF rapor
        st.markdown("---")
        if st.button("PDF Rapor Olustur", key="smm_rap_pdf"):
            try:
                from utils.report_utils import ReportPDFGenerator
                from utils.shared_data import load_kurum_profili
                kp = load_kurum_profili()
                k_adi = kp.get("kurum_adi", "") or kp.get("name", "Kurum")

                pdf = ReportPDFGenerator("Sosyal Medya Raporu", k_adi)
                pdf.add_header(k_adi)
                pdf.add_section("Genel Ozet")

                import pandas as _pd
                ozet_rows = [{
                    "Paylasim Sayisi": len(published),
                    "Begeni": sum(p.get("analytics", {}).get("begeni", 0) for p in published),
                    "Yorum": sum(p.get("analytics", {}).get("yorum", 0) for p in published),
                    "Goruntulenme": sum(p.get("analytics", {}).get("goruntulenme", 0) for p in published),
                }]
                pdf.add_table(_pd.DataFrame(ozet_rows))

                pdf_bytes = pdf.generate()
                if pdf_bytes:
                    st.download_button(
                        "📄 PDF Indir", data=pdf_bytes,
                        file_name=f"SMM_Rapor_{_today()}.pdf",
                        mime="application/pdf", key="smm_dl_pdf",
                    )
            except Exception as e:
                st.error(f"PDF olusturulamadi: {e}")


# ===================== 16. ENTEGRASYONLAR (#9, #10) =====================

def _render_entegrasyonlar():
    """Halkla Iliskiler ve Etkinlik/Duyuru entegrasyonlari (#9, #10)."""
    styled_section("Modul Entegrasyonlari", "#6366f1")

    ent_t1, ent_t2, ent_t3 = st.tabs([
        "  📢 Etkinlik → Paylasim  ", "  🏢 Halkla Iliskiler  ", "  ⚙️ Yetki Yonetimi  "
    ])

    # --- Etkinlik/Duyuru -> Sosyal Medya (#10) ---
    with ent_t1:
        styled_section("Etkinlik & Duyuru Entegrasyonu", "#10b981")
        st.caption("Kurum Hizmetleri modulundeki etkinlik ve duyurulari otomatik sosyal medya paylasimlarina donusturun.")

        try:
            from views.kurum_hizmetleri import _load_hizmet_json, ETKINLIK_DOSYA
            etkinlikler = _load_hizmet_json(ETKINLIK_DOSYA)
        except ImportError:
            etkinlikler = []

        if not etkinlikler:
            styled_info_banner("Kurum Hizmetleri modulunde etkinlik bulunamadi.", "info")
        else:
            # Son 10 etkinlik
            son_etkinlikler = sorted(etkinlikler, key=lambda x: x.get("tarih", ""), reverse=True)[:10]

            for etk in son_etkinlikler:
                etk_tip = etk.get("tip", "duyuru")
                etk_baslik = etk.get("baslik", "-")
                etk_aciklama = etk.get("aciklama", "")
                etk_tarih = etk.get("tarih", "")

                with st.expander(f"📢 {etk_baslik} | {etk_tip} | {etk_tarih}"):
                    st.markdown(f"**Aciklama:** {etk_aciklama[:200]}")

                    sec_plat = st.multiselect(
                        "Platformlar", [p[2] for p in PLATFORMLAR],
                        default=["Instagram", "Facebook"],
                        key=f"smm_etk_plat_{etk.get('id', '')}",
                    )

                    if st.button("Taslak Olustur", type="primary", key=f"smm_etk_btn_{etk.get('id', '')}"):
                        plat_keys = []
                        for sp in sec_plat:
                            for p in PLATFORMLAR:
                                if p[2] == sp:
                                    plat_keys.append(p[0])

                        metin = f"{etk_baslik}\n\n{etk_aciklama}"
                        if etk_tarih:
                            metin += f"\n\nTarih: {etk_tarih}"

                        posts = _posts()
                        posts.append({
                            "id": _new_id("post"),
                            "metin": metin,
                            "platformlar": plat_keys,
                            "hashtagler": [],
                            "kampanya": etk_tip.title(),
                            "status": "DRAFT",
                            "olusturan": {"ad": "Etkinlik Entegrasyonu", "kaynak": "kurum_hizmetleri"},
                            "created_at": _now(),
                            "updated_at": _now(),
                        })
                        _save_posts(posts)
                        st.success(f"'{etk_baslik}' taslak olarak olusturuldu!")
                        st.rerun()

    # --- Halkla Iliskiler Entegrasyonu (#9) ---
    with ent_t2:
        styled_section("Halkla Iliskiler Entegrasyonu", "#8b5cf6")
        st.caption("PR modulundeki medya icerikleri ve basin bultenleri ile entegrasyon.")

        st.info(
            "Halkla Iliskiler modulunden gelen icerikler burada listelenir. "
            "PR modulunde bir basin bulteni veya medya icerigi olusturuldugunda, "
            "otomatik olarak sosyal medya taslagi olusturulabilir."
        )

        # PR modulunden veri cekme
        try:
            from utils.tenant import get_data_path
            pr_path = os.path.join(get_data_path(""), "pr_icerikler.json")
            if os.path.exists(pr_path):
                with open(pr_path, "r", encoding="utf-8") as f:
                    pr_icerikler = json.load(f)
                if pr_icerikler:
                    for pr in pr_icerikler[-5:]:
                        with st.expander(f"📰 {pr.get('baslik', '-')}"):
                            st.markdown(pr.get("ozet", pr.get("icerik", ""))[:300])
                            if st.button("SM Taslagi Olustur", key=f"smm_pr_{pr.get('id', '')}"):
                                posts = _posts()
                                posts.append({
                                    "id": _new_id("post"),
                                    "metin": pr.get("ozet", pr.get("icerik", "")),
                                    "platformlar": ["linkedin", "facebook"],
                                    "status": "DRAFT",
                                    "kampanya": "Basin Bulteni",
                                    "olusturan": {"ad": "PR Entegrasyonu", "kaynak": "halkla_iliskiler"},
                                    "created_at": _now(),
                                    "updated_at": _now(),
                                })
                                _save_posts(posts)
                                st.success("PR icerigi taslak olarak eklendi!")
                                st.rerun()
                else:
                    styled_info_banner("PR modulunde icerik bulunamadi.", "info")
            else:
                styled_info_banner("PR veri dosyasi bulunamadi.", "info")
        except Exception:
            styled_info_banner("PR modulu ile baglanti kurulamadi.", "info")

    # --- Yetki Yonetimi (#3) ---
    with ent_t3:
        styled_section("SMM Yetki Yonetimi", "#f59e0b")
        st.caption("Kullanici rollerine gore sosyal medya yetkilerini yonetin.")

        auth_user = st.session_state.get("auth_user", {})
        current_role = auth_user.get("role", "bilinmiyor")
        st.info(f"Mevcut kullanici rolu: **{current_role}**")

        st.markdown("##### Yetki Matrisi")
        yetki_data = []
        for key, label in SMM_YETKILER_MODEL:
            has_it = check_smm_yetki(key)
            yetki_data.append({
                "Yetki": label,
                "Kod": key,
                "Durum": "✅ Var" if has_it else "❌ Yok",
            })
        import pandas as _pd
        st.dataframe(_pd.DataFrame(yetki_data), use_container_width=True, hide_index=True)

        st.markdown("""
        **Not:** Yetki atamalari `auth_user` session state uzerinden yonetilir.
        `admin` ve `yonetici` rolleri tum yetkilere otomatik sahiptir.
        Diger roller icin kullanicinin `smm_yetkiler` listesine ilgili yetki kodu eklenmelidir.
        """)


# ===================== 17. KULLANIM KILAVUZU SEKMESI =====================

def _render_kullanim_kilavuzu():
    """A'dan Z'ye tam kullanim kilavuzu — sekme icinde."""
    styled_section("Sosyal Medya Yonetimi — Kullanim Kilavuzu", "#0c4a6e")

    # PDF indirme butonu
    kilavuz_bytes = _generate_kullanim_kilavuzu_pdf()
    if kilavuz_bytes:
        st.download_button(
            "📄 Kilavuzu PDF Olarak Indir",
            data=kilavuz_bytes,
            file_name=f"SMM_Kullanim_Kilavuzu_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            key="smm_kilavuz_tab_pdf",
            use_container_width=True,
        )
    st.markdown("---")

    # ══════════════════════════════════════════════════════
    # ADIM 1
    # ══════════════════════════════════════════════════════
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0c4a6e 0%,#1e3a5f 100%);
    border-radius:14px;padding:20px 24px;margin-bottom:18px">
    <h3 style="color:#f0f9ff;margin:0">Adim 1: Ayarlar (Ilk Kurulum)</h3>
    <p style="color:#93c5fd;margin:6px 0 0 0;font-size:0.9rem">Tek seferlik yapilandirilir — tum platformlar icin temel.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("1.1 Sistem API Ayarlari (Yonetici)", expanded=False):
        st.markdown("""
**Bu bolum tek seferlik ayarlanir.** Her platform icin Developer App kimlik bilgilerini girin.

| Platform | Gerekli Bilgi | Nereden Alinir |
|----------|--------------|----------------|
| Facebook / Instagram | App ID + App Secret | developers.facebook.com → Uygulama Olustur → Business |
| LinkedIn | Client ID + Client Secret | linkedin.com/developers/apps |
| TikTok | Client Key + Client Secret | developers.tiktok.com → Manage Apps |
| YouTube | API Key | console.cloud.google.com → YouTube Data API v3 |
| X (Twitter) | API Key + Secret + Bearer Token | developer.x.com → Projects & Apps |

> **Redirect URI:** Tum platformlar icin `https://localhost/callback` kullanilir.
        """)

    with st.expander("1.2 Calisma Modu Secimi", expanded=False):
        st.markdown("""
3 farkli calisma modu vardir:

| Mod | Aciklama | Kimler Icin |
|-----|----------|-------------|
| **Direkt Yayin** | Icerikler onay sureci olmadan dogrudan yayinlanir | Tek kisilik ekipler |
| **Onayli Yayin** | Her icerik onay kuyuguna duser, yetkili onaylar | Buyuk kurumlar |
| **Her Ikisi** | Yetkiye gore direkt veya onayli yayin | Esnek yapiya ihtiyac duyanlar |
        """)

    with st.expander("1.3 Platform Hesabi Baglama (Kolay Kurulum)", expanded=False):
        st.markdown("""
Her platform icin adimlar:

1. **Ayarlar** sekmesinde ilgili platformun bolumunu acin
2. **"Bagla"** butonuna tiklayin
3. Acilan sayfada platformdaki hesabinizla giris yapin ve yetkilendirin
4. Sayfa sizi geri yonlendirecek — **donen kodu** kopyalayin
5. Kodu ilgili alana yapiistirin ve **"Onayla"** tiklayin
6. **"Baglanti Testi"** ile dogrulayin — yesil tik gorunmeli

**Token Suresi:**
- Facebook/Instagram: ~60 gun
- LinkedIn: ~1 yil
- Token suresi dolmadan 7 gun once sistem otomatik uyari uretir
        """)

    # ══════════════════════════════════════════════════════
    # ADIM 2
    # ══════════════════════════════════════════════════════
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1e40af 0%,#3730a3 100%);
    border-radius:14px;padding:20px 24px;margin-bottom:18px">
    <h3 style="color:#f0f9ff;margin:0">Adim 2: Icerik Kutuphanesi Hazirligi</h3>
    <p style="color:#a5b4fc;margin:6px 0 0 0;font-size:0.9rem">Paylasim oncesi gorsel, sablon ve hashtag hazirligi.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("2.1 Medya Galeri", expanded=False):
        st.markdown("""
Sik kullanacaginiz gorselleri/videolari yukleyin.

- **Desteklenen formatlar:** PNG, JPG, JPEG, GIF, MP4, MOV
- **Max dosya boyutu:** 50 MB
- Yuklenen dosyalar **4 sutunlu galeri** gorunumunde listelenir
- Paylasim olustururken **"Kutuphaneden Sec"** ile mevcut medyalarinizi kullanabilirsiniz
- Her dosya guvenlik kontrolunden (`validate_upload`) gecer
        """)

    with st.expander("2.2 Metin Sablonlari", expanded=False):
        st.markdown("""
Sik kullanilan paylasim metinlerini sablon olarak kaydedin.

**Ornek sablonlar:**
- "Etkinlik Duyurusu" → `Degerli velilerimiz, [ETKINLIK] tarihinde [TARIH] gerceklesecektir...`
- "Kayit Cagrisi" → `2026-2027 egitim yili on kayitlarimiz baslamistir...`
- "Basari Paylasimi" → `Ogrencimiz [AD] [YARISMADA] [BASARI] elde etmistir...`

Yeni paylasim olustururken **"Sablondan Yukle"** dropdown'undan secim yaparsaniz metin otomatik dolar.
        """)

    with st.expander("2.3 Hashtag Havuzu & Kampanya Etiketleri", expanded=False):
        st.markdown("""
**Hashtag Havuzu:**
- Kurum hashtag'lerinizi merkezi olarak yonetin
- `#` isareti otomatik eklenir
- Ornek: `#SmartCampus`, `#egitim2026`, `#basarihikayeleri`

**Kampanya Etiketleri:**
- Paylasimlarinizi kategorize edin
- Varsayilan etiketler: Bursluluk, Gezi, Kayit, Duyuru, Basari, Etkinlik, Mezuniyet, Spor, Kultur
- Kampanya bazli performans raporlari olusturabilirsiniz
        """)

    # ══════════════════════════════════════════════════════
    # ADIM 3
    # ══════════════════════════════════════════════════════
    st.markdown("""
    <div style="background:linear-gradient(135deg,#065f46 0%,#064e3b 100%);
    border-radius:14px;padding:20px 24px;margin-bottom:18px">
    <h3 style="color:#ecfdf5;margin:0">Adim 3: Marka Ayarlarini Tanimlayin</h3>
    <p style="color:#6ee7b7;margin:6px 0 0 0;font-size:0.9rem">Tutarli ve profesyonel paylasimlar icin kurallar belirleyin.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Marka Tutarliligi Ayarlari", expanded=False):
        st.markdown("""
**Marka Ayarlari** sekmesinde su bilgileri girin:

| Alan | Aciklama | Ornek |
|------|----------|-------|
| Kurum Adi | Resmi kurum adi | UZ Koleji |
| Slogan | Kurum slogani | Gelecegi Insa Ediyoruz |
| Birincil Renk | Ana kurumsal renk | #1a365d (lacivert) |
| Ikincil Renk | Vurgu rengi | #c6a84b (altin) |
| Zorunlu Hashtagler | Her paylasimda olmali | #UZKoleji, #egitim |
| Yasak Kelimeler | Kesinlikle olmamali | kotu, berbat, ucuz |
| Min. Karakter | Alt limit | 50 |

**Marka Kontrol Puanlama (100 uzerinden):**
- Zorunlu hashtag eksik: **-20 puan**
- Yasak kelime tespit: **-30 puan**
- Karakter limiti asimi: **-15 puan**
- Minimum karakter altinda: **-10 puan**
- **70+ puan = Marka Uyumlu** (yesil onay)
        """)

    # ══════════════════════════════════════════════════════
    # ADIM 4
    # ══════════════════════════════════════════════════════
    st.markdown("""
    <div style="background:linear-gradient(135deg,#9333ea 0%,#7e22ce 100%);
    border-radius:14px;padding:20px 24px;margin-bottom:18px">
    <h3 style="color:#faf5ff;margin:0">Adim 4: Ilk Paylasiminizi Olusturun</h3>
    <p style="color:#d8b4fe;margin:6px 0 0 0;font-size:0.9rem">6 adimda profesyonel icerik olusturun.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Paylasim Olusturma Adimlari", expanded=True):
        st.markdown("""
**Yeni Paylasim** sekmesinde 6 adim:

| Adim | Ne Yapilir | Detay |
|------|-----------|-------|
| 1. Platform Secimi | Hedef platformlari secin | Birden fazla secilebilir (Instagram + Facebook + LinkedIn) |
| 2. Medya Ekleme | Gorsel/video ekleyin | "Dosya Yukle" veya "Kutuphaneden Sec" |
| 3. Metin Yazma | Caption yazin | Sablondan yukleyebilir, karakter limiti otomatik kontrol edilir |
| 4. Hashtag & Kampanya | Etiketleyin | Havuzdan secin veya yeni ekleyin |
| 5. Onizleme | Kontrol edin | Her platform icin ayri onizleme karti goruntulenir |
| 6. Kaydet/Paylas | Aksiyonu secin | Taslak / Direkt Paylas / Onaya Gonder |

**Platform Ozel Metin:**
Birden fazla platform sectiyseniz, her birine farkli metin yazabilirsiniz:
- Instagram: Kisa + emoji + hashtag agirlikli
- LinkedIn: Uzun + resmi + bilgilendirici
- X (Twitter): Max 280 karakter, oze odakli
        """)

    col_plat = st.columns(4)
    platform_limits = [
        ("Instagram", "2.200", "#E4405F"), ("Facebook", "63.206", "#1877F2"),
        ("LinkedIn", "3.000", "#0A66C2"), ("X (Twitter)", "280", "#000000"),
    ]
    for i, (name, limit, color) in enumerate(platform_limits):
        with col_plat[i]:
            st.markdown(f"""<div style="text-align:center;padding:12px;background:{color}12;
                border:1px solid {color}30;border-radius:10px">
                <div style="font-weight:700;color:{color}">{name}</div>
                <div style="font-size:1.4rem;font-weight:800;color:{color}">{limit}</div>
                <div style="font-size:0.7rem;color:#64748b">karakter limiti</div>
            </div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # ADIM 5
    # ══════════════════════════════════════════════════════
    st.markdown("""
    <div style="background:linear-gradient(135deg,#b45309 0%,#92400e 100%);
    border-radius:14px;padding:20px 24px;margin:18px 0">
    <h3 style="color:#fefce8;margin:0">Adim 5: Onay Sureci</h3>
    <p style="color:#fde68a;margin:6px 0 0 0;font-size:0.9rem">Onayli yayin modunda icerik kontrol akisi.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Onay Kuyrugu Nasil Calisir", expanded=False):
        st.markdown("""
**Onay Kuyrugu** sekmesinde yetkili kisiler bekleyen icerikleri gorur.

**Durum Akisi:**
```
TASLAK → ONAYA GONDERILDI → INCELEMEDE → ONAYLANDI → YAYINLANDI
                                    ↓
                           REVIZYON ISTENDI → (duzelt) → ONAYA GONDERILDI
                                    ↓
                               REDDEDILDI (IPTAL)
```

**Yetkili 3 aksiyon alabilir:**

| Aksiyon | Sonuc | Ne Zaman |
|---------|-------|----------|
| **Onayla** | Icerik yayina hazir (APPROVED) | Icerik uygun |
| **Revizyon Iste** | Icerik olusturana geri doner | Duzeltme gerekiyor |
| **Reddet** | Icerik iptal (CANCELED) | Icerik uygun degil |

Her islem **onay gecmisinde** kayit altina alinir (tarih + kisi + islem + yorum).
        """)

    # ══════════════════════════════════════════════════════
    # ADIM 6
    # ══════════════════════════════════════════════════════
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0d9488 0%,#0f766e 100%);
    border-radius:14px;padding:20px 24px;margin-bottom:18px">
    <h3 style="color:#f0fdfa;margin:0">Adim 6: Takvim ve Planlama</h3>
    <p style="color:#99f6e4;margin:6px 0 0 0;font-size:0.9rem">3 farkli gorunum + AI destekli en iyi saat onerisi.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Takvim Gorunumleri", expanded=False):
        st.markdown("""
| Gorunum | Aciklama | Kullanim |
|---------|----------|----------|
| **Aylik** | Tum ayin takvim grid'i, gun basi paylasim sayisi badge | Genel plan kontrolu |
| **Haftalik** | 7 kolonlu haftalik gorunum, icerik kartlari | Bu haftanin plani |
| **Gunluk** | Secilen gune ait detayli icerik listesi | Belirli gun kontrolu |

**En Iyi Paylasim Saatleri (Otomatik Oneri):**
- Sistem yayinlanmis paylasimlarinizin engagement verilerini analiz eder
- Her platform icin en verimli gun ve saat onerisi sunar
- Yeterli veri yoksa sektordeki en iyi pratikler gosterilir
- Ornek: Instagram → Sali 11:00, Persembe 14:00
        """)

    # ══════════════════════════════════════════════════════
    # ADIM 7-8
    # ══════════════════════════════════════════════════════
    st.markdown("""
    <div style="background:linear-gradient(135deg,#4338ca 0%,#3730a3 100%);
    border-radius:14px;padding:20px 24px;margin-bottom:18px">
    <h3 style="color:#eef2ff;margin:0">Adim 7: Dashboard & Performans Takibi</h3>
    <p style="color:#a5b4fc;margin:6px 0 0 0;font-size:0.9rem">Analitik verileri gorsellestirin ve optimize edin.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Dashboard Ozellikleri", expanded=False):
        st.markdown("""
**Dashboard** sekmesi sunlari gosterir:

- **Genel Metrikler:** Toplam begeni, yorum, paylasim, goruntulenme
- **Platform Bazli KPI:** Her platform icin ayri performans kartlari
- **En Iyi 5 Icerik:** En yuksek etkilesim alan paylasimlar
- **Kampanya Performansi:** Bar grafik ile kampanya bazli karsilastirma
- **Platform Dagilimi:** Pasta grafik ile paylasim orani
- **Zaman Bazli Trend:** Gunluk etkilesim cizgi grafigi

**"Analiz Verilerini Guncelle (API)"** butonu ile platformlardan gercek zamanli veri cekilir.
        """)

    with st.expander("Gelen Kutusu & Sentiment Analizi", expanded=False):
        st.markdown("""
**Gelen Kutusu** ile tum sosyal medya mesajlarinizi yonetin:

- **"Yorumlari Cek (API)"** → Platformlardan yorum/mention/DM cekin
- **"Sentiment Analizi Calistir"** → Tum mesajlari otomatik siniflandirin

| Sentiment | Emoji | Anlam |
|-----------|-------|-------|
| Pozitif | 😊 | Olumlu yorum (tesekkur, harika, basarili...) |
| Notr | 😐 | Tarafsiz mesaj |
| Negatif | 😞 | Olumsuz yorum (kotu, sikayet, yetersiz...) |

**Aksiyonlar:** Okundu isaretle, yanit gonder, gorev ata, sil

Sistem **54 Turkce anahtar kelime** ile kural tabanli analiz yapar.
OpenAI aktifse GPT-4o-mini ile daha hassas sonuclar alinir.
        """)

    # ══════════════════════════════════════════════════════
    # ADIM 9
    # ══════════════════════════════════════════════════════
    st.markdown("""
    <div style="background:linear-gradient(135deg,#7c3aed 0%,#6d28d9 100%);
    border-radius:14px;padding:20px 24px;margin-bottom:18px">
    <h3 style="color:#f5f3ff;margin:0">Adim 8: AI Asistani Kullanin</h3>
    <p style="color:#c4b5fd;margin:6px 0 0 0;font-size:0.9rem">Yapay zeka ile icerik olusturma, hashtag onerisi, A/B test ve ceviri.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("AI Asistan Ozellikleri", expanded=False):
        st.markdown("""
**AI Asistan** sekmesinde 4 arac vardir (OpenAI GPT-4o-mini):

**1. Caption Uretici:**
- Konu girin (orn: "Bilim fuari")
- Ton secin (Resmi / Samimi / Enerjik / Bilgilendirici / Ilham Verici)
- Platform ve uzunluk secin
- "Caption Uret" tiklayin
- Uretilen metni "Yeni Paylasim Olarak Kullan" ile taslak yapin

**2. Hashtag Onerici:**
- Paylasim metninizi yapiistirin
- Istediginiz hashtag sayisini secin (3-15)
- AI iceriginize uygun Turkce hashtag'ler onerir

**3. A/B Test Uretici:**
- Ayni konu icin 2 farkli versiyon uretir
- Versiyon A: Resmi ve bilgilendirici
- Versiyon B: Samimi ve enerjik
- Hangisinin daha iyi performans gosterecegini test edin

**4. Coklu Dil Cevirisi:**
- Turkce metninizi su dillere cevirin: English, Deutsch, Francais, Espanol, Arabca
- Uluslararasi ogrenci/veli kitlesine ulasmak icin ideal
        """)

    # ══════════════════════════════════════════════════════
    # ADIM 10-12
    # ══════════════════════════════════════════════════════
    st.markdown("""
    <div style="background:linear-gradient(135deg,#dc2626 0%,#b91c1c 100%);
    border-radius:14px;padding:20px 24px;margin-bottom:18px">
    <h3 style="color:#fef2f2;margin:0">Adim 9: Rakip Analizi & Hashtag Takibi</h3>
    <p style="color:#fca5a5;margin:6px 0 0 0;font-size:0.9rem">Rakipleri izleyin, hashtag performansinizi olcun.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Rakip Analizi Nasil Kullanilir", expanded=False):
        st.markdown("""
1. **"Yeni Rakip Ekle"** ile rakip okulu ekleyin (kurum adi, platform, hesap URL, @kullanici)
2. Periyodik olarak **metrik girisi** yapin:

| Metrik | Aciklama | Onerilen Siklik |
|--------|----------|-----------------|
| Takipci | Toplam takipci sayisi | Haftalik |
| Paylasim Sayisi | Toplam post sayisi | Aylik |
| Ort. Begeni | Son 10 postun ortalamasi | 2 haftada bir |
| Ort. Yorum | Son 10 postun ortalamasi | 2 haftada bir |
| Engagement Rate (%) | (Begeni+Yorum) / Takipci * 100 | Aylik |

3. **Takipci trendi grafigi** ile buyumeyi karsilastirin
        """)

    with st.expander("Hashtag Performans Takibi", expanded=False):
        st.markdown("""
Sistem yayinlanmis paylasimlarinizdaki hashtag'lerin performansini otomatik hesaplar:

| Metrik | Aciklama |
|--------|----------|
| Kullanim Sayisi | Hashtag kac paylasimda kullanildi |
| Toplam Begeni | Bu hashtag'li paylasimlardan gelen toplam begeni |
| Toplam Yorum | Bu hashtag'li paylasimlardan gelen toplam yorum |
| Ort. Etkilesim | (Begeni + Yorum) / Kullanim Sayisi |

**Top 10 Hashtag** grafigiyle en etkili hashtag'lerinizi goruntuleyin.
Dusuk performansli hashtag'leri eleyerek stratejinizi optimize edin.
        """)

    # ══════════════════════════════════════════════════════
    # ADIM 13-14
    # ══════════════════════════════════════════════════════
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0369a1 0%,#075985 100%);
    border-radius:14px;padding:20px 24px;margin-bottom:18px">
    <h3 style="color:#f0f9ff;margin:0">Adim 10: Raporlayin & Entegre Edin</h3>
    <p style="color:#7dd3fc;margin:6px 0 0 0;font-size:0.9rem">Performansi raporlayin, diger modullerle entegre calisin.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Raporlar ve Export", expanded=False):
        st.markdown("""
**Raporlar** sekmesinde 3 bolum:

| Bolum | Aciklama |
|-------|----------|
| **Genel Ozet** | Tum zamanlarin metrik ozeti + platform dagilimi grafigi + status bar chart |
| **Donemsel Rapor** | Tarih araligi secerek belirli donemin analizi + gunluk trend grafigi |
| **Export** | Verilerinizi 3 formatta disari aktarin |

**Export Formatlari:**
- **Excel (.xlsx):** Detayli tablo — Tarih, Metin, Platformlar, Begeni, Yorum, Paylasim, Goruntulenme, Hashtagler, Kampanya
- **CSV:** Hafif format, tum veri programlariyla uyumlu
- **PDF:** Kurumsal baslikli profesyonel rapor
        """)

    with st.expander("Modul Entegrasyonlari", expanded=False):
        st.markdown("""
**Entegrasyonlar** sekmesinde 3 baglanti:

**1. Etkinlik → Paylasim:**
- Kurum Hizmetleri modulundeki etkinlikleri gorursunuz
- Etkinlik secip "Taslak Olustur" tiklayin
- Baslik + aciklama otomatik metin olur, platform secin

**2. Halkla Iliskiler → Paylasim:**
- PR modulundeki basin bultenlerini gorursunuz
- "SM Taslagi Olustur" ile LinkedIn + Facebook taslagi olusur

**3. Yetki Yonetimi:**
10 farkli yetki atanabilir:

| Yetki | Aciklama |
|-------|----------|
| Hesap Baglama | Platform hesaplarini baglama/ayirma |
| Icerik Olusturma | Paylasim taslagi olusturma |
| Direkt Yayin | Onay olmadan yayinlama |
| Planlama | Icerik zamanlama |
| Onay | Icerik onaylama/reddetme |
| Rapor | Analitik ve rapor erisimi |
| Gelen Kutusu | Yorum/mesaj yonetimi |
| AI Asistan | AI araclarini kullanma |
| Rakip Analizi | Rakip verilerini yonetme |
| Marka Ayarlari | Marka kurallarini duzenleme |

> **Admin** ve **Yonetici** rolleri tum yetkilere otomatik sahiptir.
        """)

    # ══════════════════════════════════════════════════════
    # IS AKISI + GUNLUK RUTIN
    # ══════════════════════════════════════════════════════
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1e293b 0%,#0f172a 100%);
    border-radius:14px;padding:20px 24px;margin:18px 0">
    <h3 style="color:#f8fafc;margin:0">Icerik Is Akisi (Workflow)</h3>
    <p style="color:#94a3b8;margin:6px 0 0 0;font-size:0.9rem">Bir icerigin yasam dongusu — 12 asamali.</p>
    </div>
    """, unsafe_allow_html=True)

    # Workflow gorsel
    workflow_steps = [
        ("TASLAK", "#94a3b8"), ("YAYINA HAZIR", "#3b82f6"), ("ONAYA GONDERILDI", "#f59e0b"),
        ("INCELEMEDE", "#8b5cf6"), ("ONAYLANDI", "#10b981"), ("PLANLANDI", "#0d9488"),
        ("YAYINLANIYOR", "#6366f1"), ("YAYINLANDI", "#22c55e"),
    ]
    wf_cols = st.columns(len(workflow_steps))
    for i, (label, color) in enumerate(workflow_steps):
        with wf_cols[i]:
            st.markdown(f"""<div style="text-align:center;padding:8px 4px;background:{color}15;
                border:1px solid {color}40;border-radius:8px;min-height:60px;
                display:flex;align-items:center;justify-content:center">
                <span style="font-size:0.65rem;font-weight:700;color:{color}">{label}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("")

    # Gunluk rutin
    st.markdown("""
    <div style="background:linear-gradient(135deg,#fef3c7 0%,#fde68a 100%);
    border-radius:14px;padding:20px 24px;margin:18px 0;border:1px solid #f59e0b40">
    <h3 style="color:#92400e;margin:0">Onerilen Gunluk Rutin</h3>
    </div>
    """, unsafe_allow_html=True)

    rutin_cols = st.columns(3)
    with rutin_cols[0]:
        st.markdown("""
**🌅 Sabah**
- Gelen kutusunu kontrol et
- Uyarilari oku
- Onay kuyugunu temizle
        """)
    with rutin_cols[1]:
        st.markdown("""
**☀️ Ogle**
- Planlanmis icerikleri gozden gecir
- AI ile yeni caption uret
- Paylasimi yayinla/zamanla
        """)
    with rutin_cols[2]:
        st.markdown("""
**🌙 Aksam**
- Dashboard'dan performansi oku
- Rakip metriklerini guncelle
- Haftalik rapor olustur
        """)

    # SSS
    st.markdown("---")
    styled_section("Sikca Sorulan Sorular", "#64748b")

    sss_listesi = [
        ("Platform hesabimi nasil baglarim?",
         "Ayarlar > Kolay Kurulum sihirbazini kullanin. Ilgili platformun sekmesine gidin, "
         "'Bagla' butonuna tiklayin ve acilan sayfada hesabinizi yetkilendirin."),
        ("Token suresi doldu uyarisi aliyorum, ne yapmaliyim?",
         "Ayarlar sekmesinden ilgili platformun baglantisini kesin ve yeniden baglanin. "
         "Token otomatik yenilenir."),
        ("AI ozellikleri neden calismiyor?",
         "AI ozellikleri OpenAI API anahtari gerektirir. Sistem yoneticinizden "
         "OPENAI_API_KEY ortam degiskeninin tanimlandigini kontrol etmesini isteyin."),
        ("Paylasimim neden 'Yayin Hatasi' aldi?",
         "Platform API'si paylasimi reddetti. Olasi nedenler: token suresi dolmus, "
         "dosya formati uyumsuz, karakter limiti asilmis veya platform politikasi ihlali."),
        ("Birden fazla platforma ayni anda nasil paylasirim?",
         "Yeni Paylasim sekmesinde birden fazla platform secin. Her birine ozel metin "
         "yazabilir veya ayni metni tum platformlara gonderebilirsiniz."),
        ("Rakip verileri otomatik cekilebiliyor mu?",
         "Hayir, rakip metrikleri su an manuel girilir. Ilgili platformlarin herkese acik "
         "verilerini kullanarak duzenli giris yapabilirsiniz."),
        ("Sentiment analizi ne kadar dogru?",
         "Kural tabanli sistem 54 Turkce anahtar kelime kullanir (~%75 dogruluk). "
         "OpenAI entegrasyonu aktifse GPT-4o-mini ile ~%95 dogruluk elde edilir."),
        ("Raporlari kimlerle paylasabilirim?",
         "Excel, CSV veya PDF formatinda indirip e-posta ile paylasabilir, "
         "yonetim toplantilarina sunabilirsiniz."),
    ]

    for soru, cevap in sss_listesi:
        with st.expander(f"❓ {soru}"):
            st.markdown(cevap)
