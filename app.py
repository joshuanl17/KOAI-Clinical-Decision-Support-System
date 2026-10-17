import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Halaman & AI
st.set_page_config(page_title="KOAI - Asisten Klinis", page_icon="🩺", layout="wide")

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-pro')
except Exception as e:
    st.error("⚠️ Kunci API belum dipasang di pengaturan Secrets Streamlit!")
    st.stop()

# 2. Antarmuka UI
st.title("🩺 KOAI: Asisten Klinis (CDSS)")
st.markdown("Sistem Pendukung Keputusan Klinis 100% Berbasis Pedoman Lokal")

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
    pemeriksaan_penunjang = st.text_area("Pemeriksaan Penunjang (Lab/Radiologi)", height=100)
    
    submitted = st.form_submit_button("Analisis Pasien", type="primary", use_container_width=True)

# 3. Logika Pemrosesan AI
if submitted:
    if not keluhan_utama:
        st.warning("Mohon isi Keluhan Utama pasien terlebih dahulu.")
    else:
        with st.spinner("🧠 KOAI sedang membaca dokumen referensi Anda dan menganalisis data klinis..."):
            try:
                # Menarik dokumen PDF yang sudah Anda unggah di Google AI Studio
                daftar_referensi = list(genai.list_files())
                
                prompt_medis = f"""
                Anda adalah KOAI, Clinical Decision Support System (CDSS) untuk dokter umum internship di IGD/Poli.
                
                DATA PASIEN SAAT INI:
                - Demografi: {jenis_kelamin}, {usia}, BB: {berat_badan} kg, TB: {tinggi_badan} cm
                - Tanda Vital: TD {td}, Nadi {nadi}, Suhu {suhu}, RR {rr}, SpO2 {spo2}%, Kesadaran {kesadaran}
                - Keluhan & Kronologi: {keluhan_utama}
                - Riwayat & Alergi: {riwayat}
                - Pemeriksaan Fisik: {pemeriksaan_fisik}
                - Penunjang: {pemeriksaan_penunjang}

                ATURAN MUTLAK KESELAMATAN KLINIS:
                1. JAWAB HANYA BERDASARKAN DOKUMEN REFERENSI YANG DILAMPIRKAN. Jika penyakitnya tidak ada di referensi, gunakan pengetahuan medis standar dan beri peringatan tebal.
                2. Jika BB anak kosong atau 0, minta data tersebut, JANGAN MENEBAK dosis anak.
                3. Berikan perhitungan rumus dosis mg/kgBB secara transparan agar bisa diverifikasi manual.
                
                Format Output:
                1. Triage & Tanda Bahaya
                2. Diagnosis Banding (Peringkat probabilitas)
                3. Rencana Pemeriksaan Lanjutan
                4. Tatalaksana Farmakologis (Sertakan dosis hari/kali dan Label Sumber Referensi PDF-nya)
                5. Tatalaksana Non-Farmakologis & Edukasi
                6. Indikasi Rujukan
                """
                
                # Menggabungkan data pasien dengan tumpukan PDF referensi Anda
                konten_analisis = [prompt_medis]
                if daftar_referensi:
                    konten_analisis.extend(daftar_referensi)
                    st.info(f"📚 Membaca {len(daftar_referensi)} dokumen referensi medis dari brankas Anda...")
                else:
                    st.warning("⚠️ Belum ada referensi PDF yang ditemukan. AI akan murni menggunakan pengetahuan bawaannya.")
                
                # Mengirimkan data ke AI
                respon = model.generate_content(konten_analisis)
                
                st.success("Analisis Selesai!")
                st.markdown("---")
                st.markdown(respon.text)
                
                # Tombol jejak audit legal medis
                st.checkbox("Saya telah memverifikasi dosis dan tatalaksana ini dengan buku pedoman klinis (Jejak Audit CDSS)")
                
            except Exception as e:
                st.error(f"Terjadi kesalahan saat menghubungi AI: {e}")
