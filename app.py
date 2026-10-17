import streamlit as st

# Mengatur nama tab di browser
st.set_page_config(page_title="KOAI - Asisten Klinis", page_icon="🩺", layout="wide")

# Membuat judul halaman
st.title("🩺 KOAI: Asisten Klinis (CDSS)")
st.success("Selamat! Website KOAI berhasil menyala, dr. Joshua.")

# Membuat teks informasi
st.write("Aplikasi web ini sudah berhasil mengudara. Tahap selanjutnya adalah:")
st.write("1. Membuat formulir anamnesis dan pemeriksaan fisik.")
st.write("2. Menyambungkan Kunci Otak AI (API Key) secara rahasia.")

st.info("Status Sistem: Menunggu Milestone 3 (Pembuatan Formulir UI).")
