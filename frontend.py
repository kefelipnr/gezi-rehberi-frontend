import streamlit as st
import requests

#Bu bölümü sonradan makyaj için ekledik
# Yan menü (Sidebar) hazırlığı
with st.sidebar:
    st.image("https://via.placeholder.com/150", caption="BÖTE Dijital Dönüşüm")
    st.title("📌 Navigasyon")
    st.info("Bu proje Görsel Programlama dersi kapsamında geliştirilmiştir.")

# Ana sayfa başlığını renklendirelim
# ... importlar ve ayarlar ...

# TASARIM BURAYA (Makyajı burada tanımlıyoruz)
st.markdown("""
    <style>
    .main h1 { color: #007BFF; font-family: 'Trebuchet MS', sans-serif; }
    .streamlit-expanderHeader { background-color: #f0f2f6; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌍 Dinamik Gezi Rehberi") # Başlık artık mavi olacak





# ==============================
# ⚙️ AYARLAR
# ==============================
BASE_URL = "https://gezi-rehberi-backend.onrender.com"
STRAPI_TOKEN = "2b9fa02c202faf09ec188533c0551d974e2e7bbf63dce9c562330a505327c0100b6be8eaed09c3ea083bd747444773f1133937dbfd782213791679b2cc513837be27a0d81257865dcc0d581f133cb4cc67073df8e494a31d41c9c55ebd7c130a07c58568cfd9d67fe4c3179de692e47827a686f64e3a41e1335bf7af9fab99ed"

headers = {
    "Authorization": f"Bearer {STRAPI_TOKEN}",
    "Content-Type": "application/json"
}

# Web sayfasının sekme ayarları
st.set_page_config(page_title="Gezi Rehberi", page_icon="🌍", layout="centered")

# ==============================
# 🎨 TASARIM (UI) BAŞLIYOR
# ==============================

st.title("🌍 Dinamik Gezi Rehberi")
st.markdown("Bu web sitesi gücünü **Strapi Headless CMS** ve **Python Streamlit**'ten almaktadır.")
st.divider() # Araya şık bir çizgi çektik

# ==============================
# 📡 STRAPI'DEN VERİ ÇEKME 
# ==============================
# @st.cache_data, sayfa her yenilendiğinde Strapi'yi yormamak için veriyi hafızada tutar

@st.cache_data
def makaleleri_getir():
    # En garantili v5 URL'si
    url = f"{BASE_URL}/api/articles?populate=*"
    
    res = requests.get(url, headers=headers)
    if res.ok:
        # Gelen veriyi terminale basıp görelim (Hata ayıklama için)
        ham_veri = res.json().get("data", [])
        return ham_veri
    return []

# Fonksiyonu çalıştırıp makaleleri alıyoruz
articles = makaleleri_getir()  

# ==============================
# 🖥️ EKRANA BASTIRMA
# ==============================
if not articles:
    st.warning("Henüz hiç makale bulunamadı veya sunucu uyanamadı.")
else:
    for a in articles:
        # Strapi v5'ten verileri güvenle alıyoruz
        baslik = a.get("Baslik", "Başlıksız Makale")
        icerik = a.get("Icerik", "İçerik yüklenemedi...")
        
        # Streamlit'in harika "Expander" (Açılır-Kapanır Kutu) özelliği
        with st.expander(f"📰 {baslik}"):
            st.write(icerik)
            
            # Alt kısma şık bir buton ekleyelim (Şu anlık işlevsiz, sadece görsel)
            st.button("Devamını Oku", key=a.get("documentId"))
            
st.sidebar.success("Sistem Durumu: Çevrimiçi ✅")
st.sidebar.info("Görsel Programlama - MYO C# Ders Grubu Final Projesi")