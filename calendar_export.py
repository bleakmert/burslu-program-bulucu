# -*- coding: utf-8 -*-
"""
deadline_hint metinlerinden yaklaşık son-başvuru hatırlatıcıları üretip
bir .ics dosyasına yazar. Tarihler kesin değildir (deadline_hint serbest
metin) — her etkinlik açıklamasında resmi sayfadan teyit uyarısı bulunur.

Çalıştırma:
    python3 calendar_export.py
Çıktı:
    burslu_program_takvimi.ics  (Mac Calendar.app'e çift tıklayarak içe aktarılır)
"""

import re
import uuid
from datetime import date, timedelta

from data import PROGRAMS

MONTHS = {
    "ocak": 1, "şubat": 2, "subat": 2, "mart": 3, "nisan": 4, "mayıs": 5, "mayis": 5,
    "haziran": 6, "temmuz": 7, "ağustos": 8, "agustos": 8, "eylül": 9, "eylul": 9,
    "ekim": 10, "kasım": 11, "kasim": 11, "aralık": 12, "aralik": 12,
}

OUTPUT_FILE = "burslu_program_takvimi.ics"
REMINDER_DAYS_BEFORE = 30


def _first_month_in_hint(hint: str):
    """deadline_hint içindeki metinden ilk geçen ay adını bulur."""
    lowered = hint.lower()
    found = [(idx, month) for name, month in MONTHS.items()
             for idx in [lowered.find(name)] if idx != -1]
    if not found:
        return None
    found.sort(key=lambda t: t[0])
    return found[0][1]


def _target_year(month: int, today: date) -> int:
    """Ay bugünden geçmişse bir sonraki yıla kaydır."""
    year = today.year
    if month < today.month:
        year += 1
    return year


def _escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;").replace("\n", "\\n")


def build_ics(programs, today=None) -> str:
    today = today or date.today()
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Burslu Program Bulucu//TR",
        "CALSCALE:GREGORIAN",
    ]

    skipped = []
    for p in programs:
        month = _first_month_in_hint(p.get("deadline_hint", ""))
        if not month:
            skipped.append(p["name"])
            continue

        year = _target_year(month, today)
        event_date = date(year, month, 1)
        alarm_trigger_days = REMINDER_DAYS_BEFORE

        uid = f"{uuid.uuid4()}@burslu-program-bulucu"
        summary = f"🎓 Son başvuru yaklaşıyor (yaklaşık): {p['name']}"
        description = (
            f"Ülke: {p['country']} | Derece: {p['degree']} | Fon: {p['funding']}\n"
            f"Not: {p.get('deadline_hint', '')}\n"
            f"Bu tarih kesin değildir — başvurmadan önce resmi sayfadan teyit et: {p['url']}"
        )

        lines += [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{today.strftime('%Y%m%dT000000Z')}",
            f"DTSTART;VALUE=DATE:{event_date.strftime('%Y%m%d')}",
            f"DTEND;VALUE=DATE:{(event_date + timedelta(days=1)).strftime('%Y%m%d')}",
            f"SUMMARY:{_escape(summary)}",
            f"DESCRIPTION:{_escape(description)}",
            f"URL:{p['url']}",
            "BEGIN:VALARM",
            "ACTION:DISPLAY",
            f"DESCRIPTION:{_escape(summary)}",
            f"TRIGGER:-P{alarm_trigger_days}D",
            "END:VALARM",
            "END:VEVENT",
        ]

    lines.append("END:VCALENDAR")

    if skipped:
        print("Tarih çıkarılamayan (etkinlik oluşturulmadı):")
        for name in skipped:
            print(f"  - {name}")

    return "\r\n".join(lines) + "\r\n"


if __name__ == "__main__":
    ics_content = build_ics(PROGRAMS)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(ics_content)
    print(f"\n{OUTPUT_FILE} oluşturuldu. Çift tıklayarak Calendar.app'e aktarabilirsin.")
