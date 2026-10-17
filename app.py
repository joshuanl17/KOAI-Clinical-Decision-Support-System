import streamlit as st

# Mengatur nama tab di browser
st.set_page_config(page_title="KOAI - Asisten Klinis", page_icon="🩺", layout="wide")

# Judul Aplikasi
st.title("🩺 KOAI: Asisten Klinis (CDSS)")
st.markdown("Sistem Pendukung Keputusan Klinis untuk Dokter Umum")

# Membuat Form Input Pasien
with st.form("form_pasien"):
    st.subheader("Data Pasien & Tanda Vital")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    with col2:
        usia = st.text_input("Usia (thn/bln)", placeholder="Contoh: 5 thn 2 bln")
    with col3:
        berat_badan = st.number_input("Berat Badan (kg)", min_value=0.0, step=0.1)
    with col4:
        tinggi_badan = st.number_input("Tinggi Badan (cm)", min_value=0.0, step=1.0)
        
    st.markdown("---")
    
    col_v1, col_v2, col_v3 = st.columns(3)
    with col_v1:
        td = st.text_input("Tekanan Darah (mmHg)", placeholder="120/80")
        nadi = st.text_input("Nadi (x/m)", placeholder="80")
    with col_v2:
        suhu = st.text_input("Suhu (°C)", placeholder="36.5")
        rr = st.text_input("Laju Napas (x/m)", placeholder="20")
    with col_v3:
        spo2 = st.text_input("SpO2 (%)", placeholder="98")
        kesadaran = st.selectbox("Kesadaran", ["Compos Mentis", "Apatis", "Delirium", "Somnolen", "Sopor", "Koma"])

    st.markdown("---")
    st.subheader("Pemeriksaan Klinis")
    
    keluhan_utama = st.text_area("Keluhan Utama & Kronologi", height=100, placeholder="Ketik keluhan dan kronologi. Boleh disingkat, AI akan memahaminya (contoh: dmm 3hr, bapil...)")
    riwayat = st.text_area("Riwayat Penyakit, Obat Rutin & Alergi", height=100)
    pemeriksaan_fisik = st.text_area("Pemeriksaan Fisik", height=100, placeholder="Status lokalis, temuan abnormal...")
    pemeriksaan_penunjang = st.text_area("Pemeriksaan Penunjang (Lab/Radiologi) - Opsional", height=100)
    
    # Tombol Submit
    submitted = st.form_submit_button("Analisis Pasien", type="primary", use_container_width=True)

# Logika respon jika tombol diklik (sementara)
if submitted:
    st.info("✅ Formulir berhasil dikirim! (Sistem AI sedang menunggu dihubungkan pada tahap selanjutnya).")
