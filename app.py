# -*- coding: utf-8 -*-
"""
Burslu Master / PhD Program Bulucu
----------------------------------
Profil: Türkiye'den, English Language Teaching (ELT) yüksek lisansı (GPA 3.44, tez aşaması),
sosyal bilimler ağırlıklı, tam burs + vize/oturum sponsorluğu hedefi.

Çalıştırma (VS Code terminali):
    pip install streamlit
    streamlit run app.py
"""

from urllib.parse import quote_plus

import streamlit as st

from data import COUNTRIES, PROGRAMS, SEARCH_PORTALS

# Veri: bkz. data.py

# ----------------------------- Arayüz -----------------------------

st.set_page_config(page_title="Burslu Program Bulucu", page_icon="🎓", layout="wide")

st.title("🎓 Burslu Master / PhD Program Bulucu")
st.caption(
    "Profil: ELT yüksek lisansı (tez aşaması, GPA 3.44) · Türkiye · "
    "Hedef: tam burs/maaş + vize-oturum sponsorluğu · Sosyal bilimler ağırlıklı"
)

with st.sidebar:
    st.header("Filtreler")
    sel_countries = st.multiselect("Ülke", COUNTRIES, default=COUNTRIES)
    sel_degree = st.radio("Derece", ["Hepsi", "PhD", "Master"], index=0)
    sel_funding = st.multiselect(
        "Fon türü",
        ["Tam Burs", "Maaşlı Kadro", "Burs (kısmi/değişken)"],
        default=["Tam Burs", "Maaşlı Kadro"],
    )
    keyword = st.text_input("Anahtar kelime (isteğe bağlı)", placeholder="ör. linguistics, education")

    st.divider()
    st.subheader("🔎 Canlı arama linkleri")
    live_q = st.text_input(
        "Portal arama sorgusu",
        value="applied linguistics PhD scholarship",
        help="Aşağıdaki portallarda bu sorguyla arama linki üretilir.",
    )
    for portal_name, tmpl in SEARCH_PORTALS:
        st.markdown(f"- [{portal_name}]({tmpl.format(q=quote_plus(live_q))})")

# Filtreleme
results = []
kw = keyword.strip().lower()
for p in PROGRAMS:
    if p["country"] not in sel_countries:
        continue
    if sel_degree != "Hepsi" and sel_degree not in p["degree"]:
        continue
    if p["funding"] not in sel_funding:
        continue
    if kw and kw not in " ".join(str(v) for v in p.values()).lower():
        continue
    results.append(p)

st.subheader(f"Sonuçlar ({len(results)} program/burs)")

if not results:
    st.info("Filtrelere uyan sonuç yok. Filtreleri genişletmeyi deneyin.")

FUNDING_COLORS = {"Tam Burs": "🟢", "Maaşlı Kadro": "🔵", "Burs (kısmi/değişken)": "🟡"}

for p in results:
    with st.expander(f"{FUNDING_COLORS[p['funding']]} {p['name']} — {p['country']} · {p['degree']}"):
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(f"**Alan:** {p['field']}")
            st.markdown(f"**Profil uyumu:** {p['fit']}")
            st.markdown(f"**Sponsorluk / vize:** {p['sponsor_note']}")
            if p.get("requirements"):
                st.markdown("**📋 Başvuru için gerekenler:**")
                for item in p["requirements"]:
                    st.checkbox(item, key=f"{p['name']}::{item}")
        with c2:
            st.markdown(f"**Fon:** {p['funding']}")
            st.markdown(f"**Son başvuru (yaklaşık):** {p['deadline_hint']}")
            st.link_button("Resmi sayfa →", p["url"])

st.divider()
st.markdown(
    """
**Strateji notları (profiline göre):**
1. **En güçlü rota: maaşlı PhD kadroları** (Hollanda, Almanya, İsviçre). Bunlar burs değil *iş sözleşmesi* — vize sponsorluğu otomatik gelir ve GPA yerine araştırma önerisi/tez konusu belirleyicidir.
2. **Tezini koz olarak kullan:** ELT tezinden bir yayın/bildiri çıkarmak, doktora başvurularında GPA'den daha etkili.
3. **İtalya'yı atlama:** Doktora bursları neredeyse standart, yabancı kontenjanları var ve rekabet Kuzey Avrupa'ya göre düşük.
4. **Paralel başvuru:** DAAD + Swiss Excellence + la Caixa + Erasmus Mundus takvimleri çakışmaz; aynı yıl hepsine başvurulabilir.
"""
)
