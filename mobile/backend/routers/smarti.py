"""Smarti AI Chat — sesli/yazili asistan."""
from __future__ import annotations

import os
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from ..core.deps import get_current_user, get_data_adapter
from ..core.data_adapter import DataAdapter


router = APIRouter(prefix="/smarti", tags=["Smarti AI"])


class ChatRequest(BaseModel):
    mesaj: str = Field(..., min_length=1, max_length=2000)
    context: str = ""  # opsiyonel — hangi ekrandan geliyor


class ChatResponse(BaseModel):
    cevap: str
    kaynak: str = "openai"
    timestamp: str


def _get_openai_key() -> str | None:
    """OpenAI API key'i bul."""
    # 1. Env variable
    key = os.environ.get("OPENAI_API_KEY") or os.environ.get("openai_api_key")
    if key:
        return key

    # 2. .env dosyasından
    env_paths = [
        os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env"),
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".env"),
    ]
    for p in env_paths:
        if os.path.exists(p):
            try:
                with open(p, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("OPENAI_API_KEY=") or line.startswith("openai_api_key="):
                            return line.split("=", 1)[1].strip().strip("'\"")
            except Exception:
                pass
    return None


SYSTEM_PROMPT = """Sen SmartCampus AI'nin Smarti isimli yapay zeka asistanısın.
Türk eğitim kurumlarına hizmet veren bir yazılımın parçasısın.
Kısa, net ve yardımcı cevaplar ver. Kullanıcının rolüne uygun konuş.
Roller: Yönetici, Öğretmen, Veli, Öğrenci, Rehber.
Türkçe konuş. Emoji kullanabilirsin ama abartma."""


@router.post("/chat", response_model=ChatResponse)
async def chat(
    req: ChatRequest,
    user: Annotated[dict, Depends(get_current_user)],
):
    """Smarti AI ile sohbet — OpenAI GPT-4o-mini."""
    role = user.get("role", "ogrenci")
    ad = user.get("ad_soyad", "Kullanıcı")

    api_key = _get_openai_key()

    if api_key:
        # OpenAI ile cevap
        try:
            import httpx
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}",
                            "Content-Type": "application/json"},
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT
                             + f"\nKullanıcı: {ad} (Rol: {role})"},
                            {"role": "user", "content": req.mesaj},
                        ],
                        "max_tokens": 500,
                        "temperature": 0.7,
                    },
                )
                if resp.status_code == 200:
                    data = resp.json()
                    cevap = data["choices"][0]["message"]["content"]
                    return ChatResponse(
                        cevap=cevap,
                        kaynak="openai-gpt4o-mini",
                        timestamp=datetime.now().isoformat(),
                    )
                else:
                    # API hatasi — fallback
                    pass
        except Exception:
            pass

    # Fallback — basit kural bazli cevap
    cevap = _fallback_cevap(req.mesaj, role, ad)
    return ChatResponse(
        cevap=cevap,
        kaynak="fallback",
        timestamp=datetime.now().isoformat(),
    )


def _fallback_cevap(mesaj: str, role: str, ad: str) -> str:
    """OpenAI yokken basit kural bazli cevap."""
    m = mesaj.lower()

    if any(k in m for k in ("merhaba", "selam", "hey")):
        return f"Merhaba {ad}! 👋 Ben Smarti, SmartCampus AI asistanınım. Size nasıl yardımcı olabilirim?"

    if any(k in m for k in ("sınav", "sinav", "yazılı", "yazili")):
        return "📝 Sınav bilgileri için Akademik Takvim'e bakabilirsiniz. Yaklaşan sınavları görmek ister misiniz?"

    if any(k in m for k in ("not", "ortalama", "puan")):
        if role in ("ogrenci", "veli"):
            return "📊 Notlarınızı 'Notlarım' bölümünden görebilirsiniz. Ders bazlı ortalamalar ve trend analizi mevcuttur."
        return "📊 Öğrenci notları için Akademik Takip modülüne bakabilirsiniz."

    if any(k in m for k in ("devamsız", "yoklama", "gelmedi")):
        return "📅 Devamsızlık bilgileri için 'Devamsızlık' bölümüne bakabilirsiniz. Özürsüz devamsızlık %10'u aşarsa uyarı gelir."

    if any(k in m for k in ("ödev", "odev", "teslim")):
        return "📚 Ödevlerinizi 'Ödevlerim' bölümünden takip edebilirsiniz. Geciken ödevler kırmızı işaretlenir."

    if any(k in m for k in ("randevu", "görüşme", "gorusme")):
        return "📅 Randevu almak için 'Randevu' bölümüne gidin. Öğretmen seçip tarih/saat belirleyebilirsiniz."

    if any(k in m for k in ("risk", "tehlike", "uyarı", "erken")):
        return "⚠️ Erken Uyarı Sistemi 20 boyutta risk analizi yapar. Detaylar için yönetici panelindeki 'Erken Uyarı' bölümüne bakın."

    if any(k in m for k in ("teşekkür", "tesekkur", "sağol", "sagol")):
        return "Rica ederim! 😊 Başka bir konuda yardımcı olabilir miyim?"

    if any(k in m for k in ("kimsin", "ne yapıyor", "nedir")):
        return ("🤖 Ben Smarti — SmartCampus AI'nin yapay zeka asistanıyım. "
                "33 modüllü eğitim yönetim platformunun her konusunda size yardımcı olurum. "
                "Not, devamsızlık, sınav, randevu, risk analizi ve daha fazlası hakkında sorabilirsiniz!")

    return (f"🤖 Anlıyorum {ad}. Bu konuda size en iyi şekilde yardımcı olmak istiyorum. "
            "Lütfen sorunuzu biraz daha detaylandırır mısınız? "
            "Not, devamsızlık, ödev, sınav, randevu gibi konularda uzmanım.")


@router.get("/onerileri")
async def onerileri(
    user: Annotated[dict, Depends(get_current_user)],
):
    """Rol bazli oneri sorulari."""
    role = user.get("role", "ogrenci")

    oneriler = {
        "yonetici": [
            "Bugün okulda ne var?",
            "Bu hafta riskli öğrenciler kimler?",
            "Devamsızlık durumu nasıl?",
            "Bütçe özeti göster",
            "Kayıt dönüşüm oranı nedir?",
        ],
        "ogretmen": [
            "Bugün hangi derslerim var?",
            "Sınav sonuçları nasıl?",
            "Yoklama durumu",
            "Ödev teslim oranları",
            "Riskli öğrencilerim",
        ],
        "veli": [
            "Çocuğumun notları nasıl?",
            "Devamsızlık durumu",
            "Bugün ne ödev var?",
            "Randevu almak istiyorum",
            "Günlük kapsül",
        ],
        "ogrenci": [
            "Notlarım nasıl?",
            "Yarın sınav var mı?",
            "Ödevlerim neler?",
            "Mood check-in",
            "Dil öğrenme önerileri",
        ],
        "rehber": [
            "Riskli öğrenciler",
            "Bugün mood durumu",
            "Açık vakalar",
            "İhbar listesi",
            "Aile görüşme planı",
        ],
    }

    return {"oneriler": oneriler.get(role, oneriler["ogrenci"])}
