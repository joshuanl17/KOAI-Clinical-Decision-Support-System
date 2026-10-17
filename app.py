import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Halaman & AI
st.set_page_config(page_title="KOAI - Asisten Klinis", page_icon="🩺", layout="wide")

try:
    # Mengambil kunci rahasia dari Streamlit Secrets
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Menggunakan model Gemini 1.5 Pro (paling cerdas untuk nalar medis)
    model = genai.GenerativeModel('gemini-1.5-pro')
except Exception as e:
    st.error("⚠️ Kunci API belum dipasang di pengaturan Secrets Streamlit!")
    st.stop()

# 2. Antarmuka UI (Judul & Formulir)
st.title("🩺 KOAI: Asisten Klinis (CDSS)")
st.markdown("Sistem Pendukung Keputusan Klinis 100% Berbasis Pedoman")

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
    
    keluhan_utama = st.text_area("Keluhan Utama & Kronologi", height=100)
    riwayat = st.text_area("Riwayat Penyakit, Obat Rutin & Alergi", height=100)
    pemeriksaan_fisik = st.text_area("Pemeriksaan Fisik", height=100)
    pemeriksaan_penunjang = st.text_area("Pemeriksaan Penunjang (Lab/Radiologi) - Opsional", height=100)
    
    submitted = st.form_submit_button("Analisis Pasien", type="primary", use_container_width=True)

# 3. Logika Pemrosesan AI
if submitted:
    if not keluhan_utama:
        st.warning("Mohon isi Keluhan Utama pasien terlebih dahulu.")
    else:
        # Menampilkan animasi loading
        with st.spinner("🧠 KOAI sedang menganalisis data klinis dan mencocokkan pedoman..."):
            
            # Menyusun instruksi mutlak (The System Prompt)
            prompt_medis = f"""
            Anda adalah KOAI, Clinical Decision Support System (CDSS) tingkat lanjut untuk dokter umum internship di IGD/Poli.
            Anda harus menoleransi typo dan singkatan medis.
            
            DATA PASIEN SAAT INI:
            - Demografi: {jenis_kelamin}, {usia}, BB: {berat_badan} kg, TB: {tinggi_badan} cm
            - Tanda Vital: TD {td}, Nadi {nadi}, Suhu {suhu}, RR {rr}, SpO2 {spo2}%, Kesadaran {kesadaran}
            - Keluhan & Kronologi: {keluhan_utama}
            - Riwayat & Alergi: {riwayat}
            - Pemeriksaan Fisik: {pemeriksaan_fisik}
            - Penunjang: {pemeriksaan_penunjang}

            ATURAN MUTLAK KESELAMATAN KLINIS:
            1. Jika ada data penting (terutama BB anak) yang kosong, minta data tersebut, JANGAN MENEBAK.
            2. Gunakan peringkat kemungkinan kualitatif, JANGAN membuat persentase probabilitas acak.
            3. Berikan tatalaksana farmakologis secara transparan (tampilkan perhitungan dosis mg/kgBB).
            4. Selalu beri label sumber rekomendasi. Jika dari pengetahuan AI umum, beri peringatan: "SUMBER: Pengetahuan Umum AI — WAJIB VERIFIKASI DOSIS DENGAN BUKU SAKU ANDA."
            
            Berikan output terstruktur dalam format berikut:
            1. Triage & Tanda Bahaya (Stabilisasi darurat jika ada)
            2. Diagnosis Banding (Peringkat kemungkinan, alasan pendukung, dan data yang tidak sesuai)
            3. Rencana Pemeriksaan Lanjutan
            4. Tatalaksana Farmakologis (Lengkap dengan dosis per hari/kali, rute, frekuensi, dan peringatan kontraindikasi/alergi)
            5. Tatalaksana Non-Farmakologis & Edukasi Pasien
            6. Indikasi Rujukan
            """
            
            try:
                # Mengirimkan data ke otak AI
                respon = model.generate_content(prompt_medis)
                
                # Menampilkan hasil
                st.success("Analisis Selesai!")
                st.markdown("---")
                st.markdown(respon.text)
                
                # Menambahkan jejak audit klinis sesuai SRS
                st.checkbox("Saya telah memverifikasi dosis dan tatalaksana ini dengan pedoman klinis (Jejak Audit CDSS)")
                
            except Exception as e:
                st.error(f"Terjadi kesalahan saat menghubungi AI: {e}")
