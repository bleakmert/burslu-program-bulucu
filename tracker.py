# -*- coding: utf-8 -*-
"""Kişisel başvuru takip durumu (yerel, senkronize edilen data.py'den ayrı tutulur).

application_status.json .gitignore'da — aylık otomatik bot data.py'yi günceller ama
bu dosyaya hiç dokunmaz, kişisel ilerleme notların bot tarafından ezilmez.
"""

import json
import os

STATUS_FILE = os.path.join(os.path.dirname(__file__), "application_status.json")

STATUSES = [
    "İncelenmedi",
    "Değerlendiriliyor",
    "Hazırlanıyor",
    "Onay bekliyor",
    "Başvuruldu",
    "Vazgeçildi",
]


def load_status():
    if not os.path.exists(STATUS_FILE):
        return {}
    with open(STATUS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_status(all_status):
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(all_status, f, ensure_ascii=False, indent=2, sort_keys=True)


def get_entry(program_name):
    data = load_status()
    return data.get(program_name, {"status": STATUSES[0], "note": "", "checked": {}})


def set_entry(program_name, status, note):
    data = load_status()
    entry = data.get(program_name, {"status": STATUSES[0], "note": "", "checked": {}})
    entry["status"] = status
    entry["note"] = note
    data[program_name] = entry
    save_status(data)


def set_checked(program_name, item, value):
    data = load_status()
    entry = data.get(program_name, {"status": STATUSES[0], "note": "", "checked": {}})
    entry.setdefault("checked", {})[item] = value
    data[program_name] = entry
    save_status(data)
