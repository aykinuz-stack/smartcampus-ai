"""
Authentication Module
=====================
SmartCampus AI icin kimlik dogrulama ve kullanici yonetim sistemi.
bcrypt hash tabanli sifre dogrulama + Streamlit session yonetimi.
Rol Bazli Erisim Kontrolu (RBAC) destegi.
"""

import hashlib
import json
import os
import re
import secrets
import string
from datetime import datetime
from typing import Any

import bcrypt
import streamlit as st

USERS_FILE = os.path.join("data", "users.json")

# =====================================================================
# GUVENLIK UYARISI (PRODUCTION)
# =====================================================================
# Bu dosyadaki varsayilan sifreler YALNIZCA gelistirme/demo amacidir.
# URETIM ortaminda asagidaki ortam degiskenlerini MUTLAKA ayarlayin:
#   SA_DEFAULT_PW, ADMIN_DEFAULT_PW, OGR_DEFAULT_PW,
#   STU_DEFAULT_PW, VELI_DEFAULT_PW
# Ortam degiskenleri bos birakildiysa varsayilan sifre atanmaz ve
# kullanicinin ilk giriste sifre olusturmasi zorunlu olur.
# =====================================================================

# ===================== SUPER ADMIN =====================

SUPER_ADMIN_ROLE = "SuperAdmin"

# ===================== SIFRE HASH =====================


def _hash_password(password: str) -> str:
    """Sifreyi bcrypt ile hash'le (salt dahil)."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")


def _verify_password(password: str, stored_hash: str) -> bool:
    """Sifreyi dogrula — bcrypt ve legacy SHA-256 destegi."""
    # bcrypt hash ($2b$ ile baslar)
    if stored_hash.startswith("$2b$") or stored_hash.startswith("$2a$"):
        try:
            return bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))
        except Exception:
            return False
    # Legacy SHA-256 fallback (eski hashler icin)
    legacy = hashlib.sha256(password.encode()).hexdigest()
    if legacy == stored_hash:
        return True
    return False


def _needs_rehash(stored_hash: str) -> bool:
    """Hash'in bcrypt'e guncellenmesi gerekiyor mu?"""
    return not (stored_hash.startswith("$2b$") or stored_hash.startswith("$2a$"))


# ===================== ROL TANIMLARI =====================

ROLES = ["SuperAdmin", "Yonetici", "Ogretmen", "Calisan", "Ogrenci", "Veli"]

STAFF_CATEGORY_TO_ROLE: dict[str, str] = {
    "yonetim_kurulu": "Yonetici",
    "ust_yonetim": "Yonetici",
    "okul_yoneticileri": "Yonetici",
    "akademik": "Ogretmen",
    "ogretim": "Ogretmen",
    "idari": "Calisan",
    "destek": "Calisan",
    "diger": "Calisan",
}

# Varsayilan kullanicilar (ilk calistirmada olusturulur)
# ONEMLI: Sifreler ortam degiskenlerinden alinir. Ortam degiskeni ayarlanmamissa
# rastgele sifre uretilir ve must_change_password=True zorlanir.
# Uretim ortaminda mutlaka SA_DEFAULT_PW, ADMIN_DEFAULT_PW vb. ayarlayin.

def _default_pw(env_key: str) -> tuple[str, bool]:
    """Ortam degiskeninden sifre al. Yoksa rastgele uret + zorunlu degisim."""
    pw = os.environ.get(env_key, "")
    if pw:
        return _hash_password(pw), True  # env'den geldi ama yine de degistirmeli
    # Env bos: rastgele 16 karakter uret (kullanici ilk giriste degistirmeli)
    alphabet = string.ascii_letters + string.digits
    pw = "".join(secrets.choice(alphabet) for _ in range(16))
    return _hash_password(pw), True  # must_change_password = True


_sa_hash, _sa_mcp = _default_pw("SA_DEFAULT_PW")
_admin_hash, _admin_mcp = _default_pw("ADMIN_DEFAULT_PW")
_ogr_hash, _ogr_mcp = _default_pw("OGR_DEFAULT_PW")
_stu_hash, _stu_mcp = _default_pw("STU_DEFAULT_PW")
_veli_hash, _veli_mcp = _default_pw("VELI_DEFAULT_PW")

DEFAULT_USERS = [
    {
        "username": "superadmin",
        "password_hash": _sa_hash,
        "name": "Super Admin",
        "role": "SuperAdmin",
        "tenant_id": "__global__",
        "must_change_password": _sa_mcp,
    },
    {
        "username": "admin",
        "password_hash": _admin_hash,
        "name": "Yonetici",
        "role": "Yonetici",
        "tenant_id": "uz_koleji",
        "must_change_password": _admin_mcp,
    },
    {
        "username": "ogretmen",
        "password_hash": _ogr_hash,
        "name": "Ogretmen",
        "role": "Ogretmen",
        "tenant_id": "uz_koleji",
        "must_change_password": _ogr_mcp,
    },
    {
        "username": "ogrenci",
        "password_hash": _stu_hash,
        "name": "Ogrenci",
        "role": "Ogrenci",
        "tenant_id": "uz_koleji",
        "must_change_password": _stu_mcp,
    },
    {
        "username": "veli",
        "password_hash": _veli_hash,
        "name": "Veli",
        "role": "Veli",
        "tenant_id": "uz_koleji",
        "must_change_password": _veli_mcp,
    },
]


# ===================== DOSYA ISLEMLERI =====================

def _ensure_users_file() -> None:
    """Kullanici dosyasi yoksa varsayilan kullanicilarla olustur."""
    if not os.path.exists(USERS_FILE):
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_USERS, f, ensure_ascii=False, indent=2)


def _load_users() -> list[dict[str, Any]]:
    """Kullanici listesini yukle."""
    _ensure_users_file()
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return list(DEFAULT_USERS)


def _save_users(users: list[dict[str, Any]]) -> None:
    """Kullanici listesini dosyaya kaydet."""
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


# ===================== SIFRE & KULLANICI ADI URETIMI =====================

def generate_password(length: int = 8) -> str:
    """Rastgele alfanumerik sifre uret (SMS uyumlu, ozel karakter yok)."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def _normalize_tr(text: str) -> str:
    """Turkce karakterleri ASCII karsiliklarına cevir."""
    tr_map = {
        "ç": "c", "Ç": "c", "ğ": "g", "Ğ": "g",
        "ı": "i", "İ": "i", "ö": "o", "Ö": "o",
        "ş": "s", "Ş": "s", "ü": "u", "Ü": "u",
    }
    for tr_char, ascii_char in tr_map.items():
        text = text.replace(tr_char, ascii_char)
    return text.lower().strip()


def generate_username(ad: str, soyad: str, existing: set[str]) -> str:
    """ad.soyad formatinda benzersiz kullanici adi uret."""
    base_ad = re.sub(r"[^a-z0-9]", "", _normalize_tr(ad))
    base_soyad = re.sub(r"[^a-z0-9]", "", _normalize_tr(soyad))
    if not base_ad:
        base_ad = "user"
    if not base_soyad:
        base_soyad = "x"
    base = f"{base_ad}.{base_soyad}"
    if base not in existing:
        return base
    counter = 2
    while f"{base}{counter}" in existing:
        counter += 1
    return f"{base}{counter}"


# ===================== KULLANICI CRUD =====================

def get_all_users(tenant_scoped: bool = True) -> list[dict[str, Any]]:
    """Kullanicilari dondur.

    tenant_scoped=True ise sadece mevcut tenant'in kullanicilarini dondurur.
    SuperAdmin ise tum kullanicilari dondurur.
    """
    users = _load_users()
    if not tenant_scoped:
        return users
    # SuperAdmin tum kullanicilari gorur
    auth_user = st.session_state.get("auth_user", {})
    if auth_user.get("role") == SUPER_ADMIN_ROLE:
        return users
    tid = st.session_state.get("tenant_id", "")
    if not tid:
        return users
    return [u for u in users if u.get("tenant_id", "") == tid or u.get("tenant_id", "") == ""]


def user_exists(source_type: str, source_id: str) -> bool:
    """Belirli bir kaynak kaydina ait hesap var mi kontrol et."""
    users = _load_users()
    for u in users:
        if u.get("source_type") == source_type and u.get("source_id") == source_id:
            return True
    return False


def find_user_by_source(source_type: str, source_id: str) -> dict[str, Any] | None:
    """Kaynak kaydina gore kullanici bul."""
    users = _load_users()
    for u in users:
        if u.get("source_type") == source_type and u.get("source_id") == source_id:
            return u
    return None


def add_user(user_dict: dict[str, Any]) -> None:
    """Tek kullanici ekle. Tenant_id yoksa session'dan al."""
    if "tenant_id" not in user_dict:
        user_dict["tenant_id"] = st.session_state.get("tenant_id", "")
    users = _load_users()
    users.append(user_dict)
    _save_users(users)
    try:
        from utils.activity_log import log_activity
        log_activity("kullanici_ekle", detail=f"username={user_dict.get('username', '')}, role={user_dict.get('role', '')}", module="auth")
    except Exception:
        pass


def add_users_batch(user_list: list[dict[str, Any]]) -> None:
    """Toplu kullanici ekle. Tenant_id yoksa session'dan al."""
    tid = st.session_state.get("tenant_id", "")
    for u in user_list:
        if "tenant_id" not in u:
            u["tenant_id"] = tid
    users = _load_users()
    users.extend(user_list)
    _save_users(users)


def delete_user(username: str) -> bool:
    """Kullaniciyi sil. Basarili ise True dondurur."""
    users = _load_users()
    new_users = [u for u in users if u["username"] != username]
    if len(new_users) == len(users):
        return False
    _save_users(new_users)
    try:
        from utils.activity_log import log_activity
        log_activity("kullanici_sil", detail=f"username={username}", module="auth")
    except Exception:
        pass
    return True


def toggle_user_active(username: str) -> bool | None:
    """Kullanicinin aktif/pasif durumunu degistir. Yeni durumu dondurur."""
    users = _load_users()
    for u in users:
        if u["username"] == username:
            current = u.get("is_active", True)
            u["is_active"] = not current
            _save_users(users)
            return u["is_active"]
    return None


def reset_password(username: str) -> str | None:
    """Kullanicinin sifresini sifirla. Yeni plaintext sifreyi dondurur."""
    users = _load_users()
    for u in users:
        if u["username"] == username:
            new_pw = generate_password(12)
            u["password_hash"] = _hash_password(new_pw)
            u["must_change_password"] = True
            _save_users(users)
            try:
                from utils.activity_log import log_activity
                log_activity("sifre_sifirla", detail=f"username={username}", module="auth")
            except Exception:
                pass
            return new_pw
    return None


def update_user_field(username: str, field_name: str, value: Any) -> bool:
    """Kullanicinin belirli bir alanini guncelle."""
    users = _load_users()
    for u in users:
        if u["username"] == username:
            u[field_name] = value
            _save_users(users)
            return True
    return False


def update_user_modules(username: str, moduller: list[str]) -> bool:
    """Kullanicinin erisebilecegi modulleri guncelle."""
    return update_user_field(username, "izinli_moduller", moduller)


def get_user_modules(username: str) -> list[str]:
    """Kullanicinin erisebilecegi modul listesini dondur. Bos = tumu."""
    users = _load_users()
    for u in users:
        if u["username"] == username:
            return u.get("izinli_moduller", [])
    return []


# ===================== MODUL & GRUP YETKILERI =====================

# Tum sistem modulleri — GRUPLU (app.py _MODUL_GRUPLARI ile senkron)
MODUL_GRUPLARI = {
    "GENEL": [
        "Ana Sayfa",
        "Yonetim Tek Ekran",
    ],
    "KURUM": [
        "Kurumsal Organizasyon ve Iletisim",
        "Halkla Iliskiler ve Tanitim",
        "Insan Kaynaklari Yonetimi",
        "Butce Gelir Gider",
        "Randevu ve Ziyaretci",
        "Toplanti ve Kurullar",
        "Kurum Hizmetleri",
    ],
    "AKADEMİK": [
        "Ogrenci Zeka Merkezi",
        "Okul Oncesi - Ilkokul",
        "Akademik Takip",
        "Olcme ve Degerlendirme",
        "Rehberlik",
        "Okul Sagligi Takip",
        "Sosyal Etkinlik ve Kulupler",
        "Kutuphane",
        "AI Ogrenme Platformu",
        "Yabanci Dil",
        "Kisisel Dil Gelisimi",
        "Egitim Koclugu",
        "AI Treni",
    ],
    "OPERASYON": [
        "Tesis ve Varlik Yonetimi",
        "Sivil Savunma ve IS Guvenligi",
        "Mezunlar ve Kariyer Yonetimi",
    ],
    "SİSTEM": [
        "AI Destek",
        "Kullanici Yonetimi",
    ],
    "PANEL": [
        "Veli Paneli",
        "Ogrenci Paneli",
    ],
}

# Düz liste (geriye uyumluluk)
TUM_MODULLER = []
for _grp_mods in MODUL_GRUPLARI.values():
    TUM_MODULLER.extend(_grp_mods)

# Rol bazlı varsayılan modül şablonları
ROL_VARSAYILAN_MODULLER: dict[str, list[str]] = {
    "SuperAdmin": [],  # Boş = tümüne erişim
    "Yonetici": [],    # Boş = tümüne erişim
    "Ogretmen": [
        "Ana Sayfa",
        "Ogrenci Zeka Merkezi",
        "Akademik Takip",
        "Olcme ve Degerlendirme", "Rehberlik",
        "Okul Oncesi - Ilkokul",
        "Sosyal Etkinlik ve Kulupler",
        "Kutuphane", "AI Ogrenme Platformu",
        "Yabanci Dil", "Kisisel Dil Gelisimi",
        "Egitim Koclugu", "AI Treni",
        "AI Destek",
    ],
    "Calisan": [
        "Ana Sayfa",
        "Randevu ve Ziyaretci",
        "Kurum Hizmetleri",
        "AI Destek",
    ],
    "Ogrenci": [
        "Ogrenci Paneli",
        "AI Ogrenme Platformu",
        "Yabanci Dil",
        "Kisisel Dil Gelisimi",
        "AI Treni",
        "STEAM Merkezi",
    ],
    "Veli": [
        "Veli Paneli",
        "AI Ogrenme Platformu",
        "AI Treni",
        "Kisisel Dil Gelisimi",
        "Yabanci Dil",
        "STEAM Merkezi",
    ],
}


def update_role_modules(role: str, moduller: list[str]) -> None:
    """Rol bazlı varsayılan modülleri güncelle (runtime — kalıcı değil)."""
    ROL_VARSAYILAN_MODULLER[role] = moduller


def get_role_default_modules(role: str) -> list[str]:
    """Rol için varsayılan modül listesini döndür."""
    return ROL_VARSAYILAN_MODULLER.get(role, [])


# ===================== AUTH MANAGER =====================

def _veli_has_child_in_kademe(user_record: dict, kademe: str) -> bool:
    """Bir veli kullanicisinin verilen kademede aktif kayitli cocugu var mi kontrol eder.

    kademe: "okul_oncesi" | "ilkokul" | "ortaokul" | "lise"
    Donen: True = var, False = yok
    Hata olursa True doner (girisi engellememe yoluna git, panel icindeki ikinci
    filtre yine "Kayitli ogrenci bulunamadi" gosterir).
    """
    if not kademe:
        return True
    try:
        from models.akademik_takip import AkademikDataStore
        from utils.shared_data import normalize_sinif
    except Exception:
        return True

    _kademe_sinif_map = {
        "okul_oncesi": {"ana4", "ana5", "anahaz"},
        "ilkokul":     {"1", "2", "3", "4"},
        "ortaokul":    {"5", "6", "7", "8", "haz"},
        "lise":        {"9", "10", "11", "12"},
        # Geriye uyumluluk
        "okul_oncesi_ilkokul": {"ana4", "ana5", "anahaz", "1", "2", "3", "4"},
        "ortaokul_lise":       {"5", "6", "7", "8", "haz", "9", "10", "11", "12"},
    }
    izinli = _kademe_sinif_map.get(kademe)
    if not izinli:
        return True

    try:
        store = AkademikDataStore()
        all_students = store.get_students()
    except Exception:
        return True

    name = (user_record.get("name") or "").strip().lower()
    username = (user_record.get("username") or "").strip()

    # 1) Veli adi eslesmesi
    children = [s for s in all_students
                if s.veli_adi and name and name in s.veli_adi.lower()]
    # 2) Veli telefon
    if not children and username:
        children = [s for s in all_students
                    if s.veli_telefon and username in str(s.veli_telefon)]
    # 3) Veli email
    if not children and username:
        children = [s for s in all_students
                    if s.veli_email and username in str(s.veli_email)]

    if not children:
        return False

    # En az bir cocuk verilen kademede mi?
    for c in children:
        try:
            norm = normalize_sinif(str(c.sinif))
        except Exception:
            norm = str(c.sinif)
        if norm in izinli:
            return True
    return False


class AuthManager:
    """Streamlit tabanli kimlik dogrulama yoneticisi."""

    @staticmethod
    def authenticate(username: str, password: str, tenant_id: str = "",
                     kademe: str = "") -> dict | None:
        """Kullanici adi ve sifre ile dogrulama yap (tenant-aware).

        SuperAdmin kullanicilari tenant_id filtresine tabi degildir.
        Diger kullanicilar sadece kendi tenant'larina giris yapabilir.

        kademe parametresi verilirse (veli portalindan giris) ve kullanici
        Veli rolundeyse o kademede aktif cocugu yoksa giris reddedilir.
        """
        users = _load_users()
        for user in users:
            if user["username"] == username and _verify_password(password, user.get("password_hash", "")):
                # Legacy SHA-256 hash'i otomatik bcrypt'e yükselt
                if _needs_rehash(user.get("password_hash", "")):
                    user["password_hash"] = _hash_password(password)
                    _save_users(users)
                if not user.get("is_active", True):
                    return None
                user_tenant = user.get("tenant_id", "")
                # SuperAdmin her yerden giris yapabilir (kademe kontrolu yok)
                if user.get("role") == SUPER_ADMIN_ROLE:
                    result = {
                        "username": user["username"],
                        "name": user["name"],
                        "role": user["role"],
                        "cinsiyet": user.get("cinsiyet", ""),
                        "tenant_id": "__global__",
                    }
                    try:
                        from utils.activity_log import log_activity
                        log_activity("login", detail=f"user={username}, role={user['role']}", module="auth")
                    except Exception:
                        pass
                    return result
                # Tenant eslesmesi kontrolu
                if tenant_id and user_tenant and user_tenant != tenant_id:
                    return None  # Yanlis kurum

                # NOT: Veli kademe kontrolu artik tek portal yapisinda gerek yok.
                # Veli login sonrasi tum cocuklari kart olarak gorur (kademe-bagimsiz).

                result = {
                    "username": user["username"],
                    "name": user["name"],
                    "role": user["role"],
                    "cinsiyet": user.get("cinsiyet", ""),
                    "tenant_id": user_tenant or tenant_id,
                }
                try:
                    from utils.activity_log import log_activity
                    log_activity("login", detail=f"user={username}, role={user['role']}", module="auth")
                except Exception:
                    pass
                return result
        return None

    @staticmethod
    def is_authenticated() -> bool:
        """Kullanicinin oturum acip acmadigini kontrol et."""
        return st.session_state.get("authenticated", False)

    @staticmethod
    def get_current_user() -> dict:
        """Mevcut oturumdaki kullanici bilgilerini dondur."""
        return st.session_state.get("auth_user", {
            "username": "misafir",
            "name": "Misafir",
            "role": "Misafir",
        })

    @staticmethod
    def is_super_admin() -> bool:
        """Mevcut kullanicinin SuperAdmin olup olmadigini kontrol et."""
        user = st.session_state.get("auth_user", {})
        return user.get("role") == SUPER_ADMIN_ROLE

    @staticmethod
    def logout() -> None:
        """Oturumu kapat."""
        try:
            from utils.activity_log import log_activity
            log_activity("logout", module="auth")
        except Exception:
            pass
        st.session_state["authenticated"] = False
        st.session_state.pop("auth_user", None)
        st.session_state.pop("veli_kademe", None)
        st.session_state.pop("veli_secili_cocuk_id", None)
        st.session_state.pop("tenant_id", None)
        st.session_state.pop("tenant_name", None)
        st.session_state.pop("login_tenant", None)

    # Portal tanimlari
    _PORTALS = {
        "superadmin": {
            "baslik": "Süper Yönetici",
            "aciklama": "Tüm kurumları yöneten merkezi admin",
            "ikon": "🛡️",
            "renk": "#dc2626",
            "gradient": "linear-gradient(135deg,#991b1b,#dc2626)",
            "roller": ("SuperAdmin",),
            "ipucu": "Yöneticinizden kullanıcı bilgilerinizi alın",
        },
        "yonetici": {
            "baslik": "Yönetici Girişi",
            "aciklama": "Okul yönetimi ve idari personel",
            "ikon": "\U0001f3db\ufe0f",
            "renk": "#1e40af",
            "gradient": "linear-gradient(135deg,#1e3a8a,#2563eb)",
            "roller": ("Yonetici", "Calisan", "SuperAdmin"),
            "ipucu": "Yönetici hesabınızla giriş yapın",
        },
        "ogretmen": {
            "baslik": "Öğretmen Girişi",
            "aciklama": "Akademik kadro ve öğretmenler",
            "ikon": "\U0001f4da",
            "renk": "#7c3aed",
            "gradient": "linear-gradient(135deg,#5b21b6,#7c3aed)",
            "roller": ("Ogretmen",),
            "ipucu": "Öğretmen hesabınızla giriş yapın",
        },
        "veli": {
            "baslik": "Veli Girişi",
            "aciklama": "Tüm kademeler — Anaokulu, İlkokul, Ortaokul, Lise",
            "ikon": "\U0001f46a",
            "renk": "#2563eb",
            "gradient": "linear-gradient(135deg,#1e3a8a,#3b82f6)",
            "roller": ("Veli",),
            "ipucu": "Kullanıcı adı + şifre ile giriş yapın. Çocuğunuzun kademesi otomatik açılır.",
        },
        "ogrenci": {
            "baslik": "Öğrenci Girişi",
            "aciklama": "Tüm sınıflar için öğrenci girişi",
            "ikon": "\U0001f393",
            "renk": "#7c3aed",
            "gradient": "linear-gradient(135deg,#5b21b6,#7c3aed)",
            "roller": ("Ogrenci",),
            "ipucu": "Kendi kullanıcı adınız + şifrenizle giriş yapın",
        },
    }

    @staticmethod
    def render_login_screen() -> None:
        """Premium tek-tik giris ekrani — kurum se → portal kart tikla → otomatik giris."""

        # ════════════════════════════════════════════════════════════
        # PREMIUM CSS — Glassmorphism + Aurora Animasyonlari
        # ════════════════════════════════════════════════════════════
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        @keyframes auroraShift {
            0%, 100% { transform: translate(0, 0) scale(1); }
            33% { transform: translate(30px, -50px) scale(1.1); }
            66% { transform: translate(-20px, 20px) scale(0.95); }
        }
        @keyframes shimmerText {
            0% { background-position: -200% center; }
            100% { background-position: 200% center; }
        }
        @keyframes floatUp {
            0% { transform: translateY(20px); opacity: 0; }
            100% { transform: translateY(0); opacity: 1; }
        }
        @keyframes glowPulse {
            0%, 100% { box-shadow: 0 0 30px rgba(99, 102, 241, .15), 0 8px 32px rgba(0,0,0,.4); }
            50% { box-shadow: 0 0 50px rgba(99, 102, 241, .3), 0 12px 48px rgba(0,0,0,.5); }
        }

        /* Tum ana container koyu siyah-mor */
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > .main,
        [data-testid="stAppViewContainer"] > .main > .block-container {
            background: radial-gradient(ellipse at top left, #1a1f3a 0%, #0a0e1f 50%, #050818 100%) !important;
            min-height: 100vh !important;
            padding-top: 1rem !important;
            max-width: 100% !important;
        }
        [data-testid="stHeader"] { background: transparent !important; }
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="stToolbar"] { display: none !important; }
        footer { display: none !important; }

        /* Aurora arka plan gradientleri */
        .stApp::before {
            content: '';
            position: fixed;
            top: -200px;
            left: -200px;
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, rgba(99, 102, 241, .25) 0%, transparent 70%);
            border-radius: 50%;
            filter: blur(80px);
            pointer-events: none;
            animation: auroraShift 18s ease-in-out infinite;
            z-index: 0;
        }
        .stApp::after {
            content: '';
            position: fixed;
            bottom: -300px;
            right: -200px;
            width: 700px;
            height: 700px;
            background: radial-gradient(circle, rgba(168, 85, 247, .2) 0%, transparent 70%);
            border-radius: 50%;
            filter: blur(100px);
            pointer-events: none;
            animation: auroraShift 22s ease-in-out infinite reverse;
            z-index: 0;
        }

        /* Tum icerik aurorann ustunde */
        [data-testid="stAppViewContainer"] > .main > .block-container > * {
            position: relative;
            z-index: 1;
        }

        /* HERO BAS */
        .login-hero {
            text-align: center;
            margin-top: 30px;
            margin-bottom: 24px;
            animation: floatUp .8s ease-out;
            font-family: 'Inter', sans-serif;
        }
        .login-hero-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 92px;
            height: 92px;
            border-radius: 28px;
            background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
            box-shadow: 0 12px 48px rgba(99, 102, 241, .4),
                        0 0 0 1px rgba(255, 255, 255, .1) inset;
            margin-bottom: 18px;
            font-size: 46px;
            position: relative;
        }
        .login-hero-icon::before {
            content: '';
            position: absolute;
            inset: -2px;
            border-radius: 30px;
            background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899, #6366f1);
            background-size: 300% 300%;
            z-index: -1;
            animation: shimmerText 4s linear infinite;
            opacity: .6;
            filter: blur(8px);
        }
        .login-hero-title {
            font-size: 52px;
            font-weight: 900;
            background: linear-gradient(90deg, #818cf8 0%, #c4b5fd 25%, #f0abfc 50%, #c4b5fd 75%, #818cf8 100%);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: shimmerText 6s linear infinite;
            margin-bottom: 8px;
            letter-spacing: -1.5px;
            line-height: 1;
        }
        .login-hero-subtitle {
            color: #94a3b8;
            font-size: 14px;
            font-weight: 500;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-top: 6px;
        }

        /* Adim gostergesi (breadcrumb) */
        .login-breadcrumb {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 14px;
            margin: 18px 0 26px;
            font-family: 'Inter', sans-serif;
        }
        .login-step {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 7px 16px;
            border-radius: 30px;
            background: rgba(255, 255, 255, .04);
            border: 1px solid rgba(99, 102, 241, .2);
            color: #64748b;
            font-size: 12px;
            font-weight: 600;
        }
        .login-step.active {
            background: linear-gradient(135deg, rgba(99, 102, 241, .2), rgba(168, 85, 247, .15));
            border-color: rgba(168, 85, 247, .5);
            color: #c4b5fd;
            box-shadow: 0 4px 16px rgba(99, 102, 241, .25);
        }
        .login-step-num {
            width: 22px;
            height: 22px;
            border-radius: 50%;
            background: rgba(99, 102, 241, .15);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 10px;
        }
        .login-step.active .login-step-num {
            background: linear-gradient(135deg, #6366f1, #a855f7);
            color: white;
        }
        .login-step-arrow {
            color: #475569;
            font-size: 14px;
        }

        /* Section labels */
        .login-section-label {
            text-align: center;
            margin: 22px 0 14px;
            font-family: 'Inter', sans-serif;
        }
        .login-section-label-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(99, 102, 241, .08);
            border: 1px solid rgba(99, 102, 241, .25);
            border-radius: 30px;
            padding: 7px 20px;
            color: #a5b4fc;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 1.2px;
            text-transform: uppercase;
        }

        /* TUM butonlari premium yap */
        [data-testid="stAppViewContainer"] [data-testid="stButton"] > button,
        [data-testid="stAppViewContainer"] button[kind="secondary"],
        [data-testid="stAppViewContainer"] button[kind="primary"] {
            background: linear-gradient(135deg, rgba(99, 102, 241, .15), rgba(168, 85, 247, .1)) !important;
            border: 1px solid rgba(168, 85, 247, .35) !important;
            color: #e9d5ff !important;
            border-radius: 16px !important;
            font-weight: 700 !important;
            letter-spacing: .3px !important;
            font-family: 'Inter', sans-serif !important;
            padding: 14px 20px !important;
            transition: all .25s cubic-bezier(.4, 0, .2, 1) !important;
            backdrop-filter: blur(10px) !important;
        }
        [data-testid="stAppViewContainer"] [data-testid="stButton"] > button:hover,
        [data-testid="stAppViewContainer"] button[kind="secondary"]:hover,
        [data-testid="stAppViewContainer"] button[kind="primary"]:hover {
            background: linear-gradient(135deg, rgba(99, 102, 241, .35), rgba(168, 85, 247, .25)) !important;
            border-color: rgba(168, 85, 247, .7) !important;
            color: #fff !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px rgba(168, 85, 247, .3) !important;
        }
        [data-testid="stAppViewContainer"] button p {
            color: inherit !important;
            font-weight: 700 !important;
            font-family: 'Inter', sans-serif !important;
        }

        /* Footer */
        .login-footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px 0;
            color: #475569;
            font-size: 11px;
            font-weight: 500;
            letter-spacing: 1px;
            font-family: 'Inter', sans-serif;
        }
        .login-footer-divider {
            display: inline-block;
            width: 30px;
            height: 1px;
            background: linear-gradient(90deg, transparent, #475569, transparent);
            vertical-align: middle;
            margin: 0 12px;
        }
        </style>
        """, unsafe_allow_html=True)

        # ════════════════════════════════════════════════════════════
        # HERO HEADER
        # ════════════════════════════════════════════════════════════
        st.markdown("""
        <div class="login-hero">
            <div class="login-hero-icon">🎓</div>
            <div class="login-hero-title">SmartCampus AI</div>
            <div class="login-hero-subtitle">Akademik Yonetim Platformu</div>
        </div>
        """, unsafe_allow_html=True)

        # ════════════════════════════════════════════════════════════
        # AKIS DURUMU
        # ════════════════════════════════════════════════════════════
        login_tenant = st.session_state.get("login_tenant", None)

        # Breadcrumb
        adim1_class = "active" if login_tenant is None else ""
        adim2_class = "active" if login_tenant is not None else ""
        st.markdown(f"""
        <div class="login-breadcrumb">
            <div class="login-step {adim1_class}">
                <span class="login-step-num">1</span>
                <span>Kurum Sec</span>
            </div>
            <span class="login-step-arrow">→</span>
            <div class="login-step {adim2_class}">
                <span class="login-step-num">2</span>
                <span>Panel Sec ve Gir</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if login_tenant is None:
            # ════════════════════════════════════════════════════════════
            # AAMA 1: KURUM SECIMI
            # ════════════════════════════════════════════════════════════
            st.markdown("""
            <div class="login-section-label">
                <span class="login-section-label-pill">🏫 KURUMUNUZU SECIN</span>
            </div>
            """, unsafe_allow_html=True)

            from utils.tenant import list_tenant_configs, create_tenant
            configs = list_tenant_configs()
            if not configs:
                create_tenant("UZ Koleji")
                configs = list_tenant_configs()

            # SuperAdmin (her zaman ust)
            sa = AuthManager._PORTALS["superadmin"]
            _s1, _sc, _s2 = st.columns([1, 2, 1])
            with _sc:
                if st.button(f"{sa['ikon']}  Super Yonetici Girisi (Tum Kurumlar)",
                              key="portal_superadmin",
                              use_container_width=True):
                    success = AuthManager._auto_login_for_portal(
                        "superadmin", "__global__")
                    if success:
                        st.rerun()
                    else:
                        st.session_state["login_tenant"] = "__global__"
                        st.session_state["login_portal"] = "superadmin"
                        st.rerun()

            st.markdown("""
            <div class="login-section-label">
                <span class="login-section-label-pill">veya - OKUL SECIN</span>
            </div>
            """, unsafe_allow_html=True)

            # Kurum kartlari
            aktif_configs = [c for c in configs if c.get("aktif", True)]
            cols_per_row = min(len(aktif_configs), 3) or 1
            cols = st.columns(cols_per_row, gap="medium")
            for i, cfg in enumerate(aktif_configs):
                col = cols[i % cols_per_row]
                t_key = cfg.get("key", "")
                t_name = cfg.get("name", t_key.replace("_", " ").title())
                with col:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,rgba(99,102,241,.15),rgba(168,85,247,.1));
                                border:1px solid rgba(168,85,247,.3);
                                border-radius:20px;padding:24px 16px;text-align:center;
                                margin-bottom:8px;backdrop-filter:blur(20px);
                                box-shadow:0 8px 32px rgba(99,102,241,.15);
                                font-family:'Inter',sans-serif;">
                        <div style="font-size:36px;margin-bottom:10px;">🏫</div>
                        <div style="font-size:15px;font-weight:800;color:#fff;
                                    margin-bottom:4px;letter-spacing:-.3px;">{t_name}</div>
                        <div style="font-size:10px;color:#94a3b8;
                                    text-transform:uppercase;letter-spacing:1px;">EGITIM KURUMU</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"➜ {t_name}'ne Gir", key=f"tenant_{t_key}",
                                  use_container_width=True):
                        st.session_state["login_tenant"] = t_key
                        st.session_state["tenant_id"] = t_key
                        st.session_state["tenant_name"] = t_name
                        st.rerun()

        else:
            # ════════════════════════════════════════════════════════════
            # AAMA 2: PORTAL SECIMI + OTOMATIK GIRIS
            # ════════════════════════════════════════════════════════════
            tenant_name = st.session_state.get("tenant_name",
                            login_tenant.replace("_", " ").title()
                            if login_tenant != "__global__" else "Tum Kurumlar")

            # Secilen kurum bilgi ust banner
            st.markdown(f"""
            <div style="text-align:center;margin:8px auto 18px;max-width:480px;
                        background:linear-gradient(135deg,rgba(99,102,241,.12),rgba(168,85,247,.08));
                        border:1px solid rgba(168,85,247,.3);border-radius:16px;
                        padding:14px 24px;backdrop-filter:blur(20px);
                        font-family:'Inter',sans-serif;">
                <div style="font-size:10px;color:#a5b4fc;font-weight:700;
                            letter-spacing:1.5px;text-transform:uppercase;">SECILI KURUM</div>
                <div style="font-size:18px;font-weight:800;color:#fff;
                            margin-top:2px;letter-spacing:-.3px;">🏫 {tenant_name}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="login-section-label">
                <span class="login-section-label-pill">⚡ TEK TIKLA GIRIS</span>
            </div>
            """, unsafe_allow_html=True)

            # ── YONETICI + OGRETMEN (UST SATIR) ──
            col1, col2 = st.columns(2, gap="medium")
            for col, key in zip([col1, col2], ["yonetici", "ogretmen"]):
                p = AuthManager._PORTALS[key]
                with col:
                    st.markdown(f"""
                    <div style="background:{p['gradient']};
                                border-radius:20px;padding:30px 20px;text-align:center;
                                box-shadow:0 12px 40px {p['renk']}40;
                                border:1px solid rgba(255,255,255,.12);
                                margin-bottom:8px;backdrop-filter:blur(20px);
                                font-family:'Inter',sans-serif;
                                position:relative;overflow:hidden;">
                        <div style="font-size:42px;margin-bottom:12px;
                                    filter:drop-shadow(0 4px 12px rgba(0,0,0,.3));">{p['ikon']}</div>
                        <div style="font-size:18px;font-weight:800;color:#fff;
                                    margin-bottom:4px;letter-spacing:-.3px;
                                    text-shadow:0 2px 4px rgba(0,0,0,.3);">{p['baslik']}</div>
                        <div style="font-size:11px;color:rgba(255,255,255,.85);
                                    margin-top:4px;">{p['aciklama']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"⚡ {p['baslik']} (otomatik)",
                                  key=f"portal_{key}",
                                  use_container_width=True):
                        success = AuthManager._auto_login_for_portal(key, login_tenant)
                        if success:
                            st.success(f"✓ {p['baslik']}'na hosgeldiniz!")
                            st.rerun()
                        else:
                            st.error(f"❌ Bu kurumda {p['baslik']} icin uygun kullanici bulunamadi.")

            # ── VELI / OGRENCI BASLI ──
            st.markdown("""
            <div class="login-section-label">
                <span class="login-section-label-pill">👨‍👩‍👧 VELI / OGRENCI GIRISI</span>
            </div>
            """, unsafe_allow_html=True)

            # 2 PORTAL: Veli (tum kademeler) + Ogrenci
            # NOT: Veli artik kademe secmiyor — login sonrasi cocugun
            # kademesi otomatik bulunur ve dogru ekran acilir.
            vc1, vc2 = st.columns(2, gap="small")
            for col, key in zip([vc1, vc2], ["veli", "ogrenci"]):
                p = AuthManager._PORTALS.get(key)
                if not p:
                    continue
                with col:
                    st.markdown(f"""
                    <div style="background:{p['gradient']};
                                border-radius:18px;padding:18px 16px;text-align:center;
                                box-shadow:0 10px 32px {p['renk']}40;
                                border:1px solid rgba(255,255,255,.15);
                                margin-bottom:8px;backdrop-filter:blur(20px);
                                font-family:'Inter',sans-serif;min-height:120px;
                                display:flex;flex-direction:column;
                                justify-content:center;align-items:center;">
                        <div style="font-size:38px;margin-bottom:8px;
                                    filter:drop-shadow(0 4px 12px rgba(0,0,0,.35));">{p['ikon']}</div>
                        <div style="font-size:17px;font-weight:800;color:#fff;
                                    margin-bottom:2px;letter-spacing:-.3px;
                                    text-shadow:0 2px 4px rgba(0,0,0,.3);">{p['baslik']}</div>
                        <div style="font-size:11px;color:rgba(255,255,255,.85);
                                    margin-top:2px;line-height:1.4;">{p['aciklama']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    # ── KULLANICI ADI + SIFRE FORMU ──
                    with st.form(f"login_form_{key}", clear_on_submit=False):
                        _kullanici = st.text_input(
                            "Kullanıcı Adı",
                            key=f"login_user_{key}",
                            placeholder="kullanici.adi",
                        )
                        _sifre = st.text_input(
                            "Şifre",
                            type="password",
                            key=f"login_pass_{key}",
                            placeholder="••••••",
                        )
                        _bs1, _bs2 = st.columns(2)
                        with _bs1:
                            _login_clicked = st.form_submit_button(
                                f"🔐 Giriş",
                                type="primary",
                                use_container_width=True,
                            )
                        with _bs2:
                            _auto_clicked = st.form_submit_button(
                                f"⚡ Demo",
                                use_container_width=True,
                            )

                    if _login_clicked:
                        if not _kullanici.strip() or not _sifre:
                            st.error("❌ Kullanıcı adı ve şifre giriniz.")
                        else:
                            result = AuthManager.authenticate(
                                _kullanici.strip(), _sifre, tenant_id=login_tenant
                            )
                            if result and result.get("role") in p.get("roller", ()):
                                st.session_state["authenticated"] = True
                                st.session_state["auth_user"] = result
                                st.session_state["current_user"] = result
                                st.session_state["tenant_id"] = result.get("tenant_id", login_tenant)
                                st.session_state.pop("login_portal", None)
                                st.success(f"✓ Hoşgeldiniz, {result.get('name', '')}!")
                                st.rerun()
                            else:
                                st.error("❌ Kullanıcı adı veya şifre hatalı.")

                    if _auto_clicked:
                        success = AuthManager._auto_login_for_portal(key, login_tenant)
                        if success:
                            st.success(f"✓ {p['baslik']}'na hosgeldiniz!")
                            st.rerun()
                        else:
                            st.error(f"❌ Bu kurumda {p['baslik']} icin uygun kullanici bulunamadi.")

            # GERI BUTON
            st.markdown("")
            _g1, _gc, _g2 = st.columns([2, 1, 2])
            with _gc:
                if st.button("← Kurum Secimine Don", key="back_to_tenant",
                              use_container_width=True):
                    st.session_state.pop("login_tenant", None)
                    st.session_state.pop("login_portal", None)
                    st.session_state.pop("tenant_id", None)
                    st.session_state.pop("tenant_name", None)
                    st.rerun()

        # ════════════════════════════════════════════════════════════
        # FOOTER
        # ════════════════════════════════════════════════════════════
        st.markdown("""
        <div class="login-footer">
            <span class="login-footer-divider"></span>
            SmartCampus AI &copy; 2026
            <span class="login-footer-divider"></span>
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def _auto_login_for_portal(portal_key: str, tenant_id: str) -> bool:
        """
        Bir portal seciminde, o portala uygun ilk kullaniciyi tenant'ta bulup
        otomatik olarak oturum acar. Kullanici/sifre sorulmaz.

        Returns: True = giris yapildi, False = uygun kullanici bulunamadi.
        """
        p = AuthManager._PORTALS.get(portal_key)
        if not p:
            return False

        roller = p.get("roller", ())
        kademe = p.get("kademe", "")

        users = _load_users()
        # Aktif kullanicilarin icinde, uygun rol + tenant ile ilk eslesen
        adaylar = []
        for u in users:
            if not u.get("is_active", True):
                continue
            if u.get("role") not in roller:
                continue
            # SuperAdmin her tenant'ta calisir
            if u.get("role") == SUPER_ADMIN_ROLE:
                adaylar.append(u)
                continue
            u_tid = u.get("tenant_id", "")
            if tenant_id == "__global__":
                adaylar.append(u)
                continue
            if u_tid == tenant_id or u_tid == "":
                adaylar.append(u)

        if not adaylar:
            return False

        # ── ONCELIK 1: Veli portallari icin kademe filtresi (eski yapi — artik kullanilmiyor) ──
        if kademe:
            kademeli = [u for u in adaylar if u.get("kademe", "") == kademe]
            if kademeli:
                adaylar = kademeli

        # ── ONCELIK 2: Portalin BIRINCIL rolune oncelik ver ──
        # Ornek: "yonetici" portalinda Yonetici > Calisan > SuperAdmin
        # Boylelikle SuperAdmin secilen ucuncu tercih olur
        rol_oncelik = list(roller)
        # SuperAdmin'i sondan al (fallback)
        if SUPER_ADMIN_ROLE in rol_oncelik and rol_oncelik[0] != SUPER_ADMIN_ROLE:
            rol_oncelik.remove(SUPER_ADMIN_ROLE)
            rol_oncelik.append(SUPER_ADMIN_ROLE)

        # Tercih sirasiyla aday filtrele — BIRINCIL roldeki kullanici varsa onu kullan
        sec = None
        for tercih_rol in rol_oncelik:
            uygun = [u for u in adaylar if u.get("role") == tercih_rol]
            if uygun:
                # Bu rolde, en kuvvetli eslesmeyi sec:
                # Once tenant'i tam eslesen, sonra tenant_id'si bos olan
                tenant_eslesen = [u for u in uygun
                                   if u.get("tenant_id", "") == tenant_id]
                if tenant_eslesen:
                    sec = tenant_eslesen[0]
                else:
                    sec = uygun[0]
                break

        if not sec:
            sec = adaylar[0]

        result = {
            "username": sec["username"],
            "name": sec["name"],
            "role": sec["role"],
            "cinsiyet": sec.get("cinsiyet", ""),
            "tenant_id": "__global__" if sec.get("role") == SUPER_ADMIN_ROLE
                          else (sec.get("tenant_id", "") or tenant_id),
        }

        # Session'a yaz
        st.session_state["authenticated"] = True
        st.session_state["auth_user"] = result
        st.session_state["current_user"] = result
        st.session_state["tenant_id"] = result["tenant_id"]
        if kademe:
            st.session_state["veli_kademe"] = kademe
        st.session_state.pop("login_portal", None)
        st.session_state.pop("login_tenant", None)

        # Activity log
        try:
            from utils.activity_log import log_activity
            log_activity("login_auto", detail=f"portal={portal_key}, user={sec['username']}", module="auth")
        except Exception:
            pass

        return True

