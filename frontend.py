import streamlit as st
import requests

# ==============================
# ⚙️ AYARLAR & GÜVENLİK
# ==============================
# Sayfa ayarlarını her şeyden önce yapmalıyız (Hata almamak için)
st.set_page_config(page_title="Gezi Rehberi", page_icon="🌍", layout="wide")

BASE_URL = "https://gezi-rehberi-backend.onrender.com"
STRAPI_TOKEN = "2b9fa02c202faf09ec188533c0551d974e2e7bbf63dce9c562330a505327c0100b6be8eaed09c3ea083bd747444773f1133937dbfd782213791679b2cc513837be27a0d81257865dcc0d581f133cb4cc67073df8e494a31d41c9c55ebd7c130a07c58568cfd9d67fe4c3179de692e47827a686f64e3a41e1335bf7af9fab99ed"

headers = {
    "Authorization": f"Bearer {STRAPI_TOKEN}",
    "Content-Type": "application/json"
}

# ==============================
# 🎨 GÖRSEL MAKYAJ (CSS)
# ==============================
st.markdown("""
    <style>
    /* Ana başlık stili */
    .main h1 { color: #1E3A8A; font-family: 'Trebuchet MS', sans-serif; text-align: center; }
    
    /* Kartların (Expander) arka planını yumuşatma */
    .streamlit-expanderHeader {
        background-color: #F3F4F6 !important;
        border-radius: 8px !important;
        border: 1px solid #E5E7EB !important;
        font-weight: bold;
        color: #1F2937;
    }
    
    /* Yan menü (Sidebar) estetiği */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC;
    }
    
    /* Butonları özelleştirme */
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        background-color: #2563EB;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================
# 📌 YAN MENÜ (SIDEBAR)
# ==============================
with st.sidebar:
    st.image("https://via.placeholder.com/150", caption="DİJİF - Dijital Fener Topluluğu")
    st.title("📌 Navigasyon")
    st.info("Bu portal, Görsel Programlama dersi kapsamında Strapi v5 ve Streamlit kullanılarak geliştirilmiştir.")
    st.divider()
    st.success("Sistem Durumu: Çevrimiçi ✅")
    st.caption("Danışman: Dr. Pınar KEFELİ")

# ==============================
# 📡 VERİ ÇEKME FONKSİYONU
# ==============================
@st.cache_data(ttl=600) # Veriyi 10 dakika hafızada tutar
def makaleleri_getir():
    url = f"{BASE_URL}/api/articles?populate=*"
    try:
        res = requests.get(url, headers=headers)
        if res.ok:
            return res.json().get("data", [])
    except:
        return []
    return []

# ==============================
# 🖥️ ANA SAYFA ARAYÜZÜ
# ==============================
st.title("🌍 Dinamik Gezi Rehberi Portalı")
st.markdown("<p style='text-align: center;'>Headless CMS mimarisi ile gerçek zamanlı içerik yönetimi</p>", unsafe_allow_html=True)
st.divider()

articles = makaleleri_getir()

if not articles:
    st.warning("🔄 İçerikler yükleniyor veya henüz makale eklenmedi...")
else:
    # Sayfayı iki sütuna bölüyoruz (Daha modern bir görünüm için)
    sol_sutun, sag_sutun = st.columns(2)

    for index, a in enumerate(articles):
        # Makaleleri sırayla bir sola bir sağa yerleştiriyoruz
        hedef_sutun = sol_sutun if index % 2 == 0 else sag_sutun
        
        # Strapi v5 verilerini çekme (Attributes kontrolü ile)
        # v5'te veriler bazen doğrudan gelir, bazen attributes içindedir
        data = a.get("attributes", a) 
        baslik = data.get("Baslik", "Başlıksız")
        icerik = data.get("Icerik", "İçerik bulunamadı...")
        doc_id = a.get("documentId", "0")

        with hedef_sutun:
            with st.expander(f"📍 {baslik}"):
                st.markdown(f"**Özet:** {icerik[:150]}...")
                st.write("---")
                st.write(icerik)
                st.button(f"Detayları İncele", key=doc_id)

st.divider()
st.caption("© 2026 - BÖTE Akademik İçerik Yönetimi Projesi")