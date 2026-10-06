import platform
import streamlit as st

st.title("Status")
st.write("Ringkasan kondisi aplikasi saat ini.")

# --- Info sistem ---
st.subheader("System")
col1, col2 = st.columns(2)
col1.metric("OS", platform.system())
col2.metric("Release", platform.release())

# --- Status browser (dibaca dari session_state yang dibagi antar halaman) ---
st.subheader("Browser")
proc = st.session_state.get("browser_proc")
if proc is not None and proc.poll() is None:
    st.success(f"Browser berjalan (PID {proc.pid}).")
else:
    st.info("Browser belum dijalankan dari app ini.")

# --- Statistik chat ---
st.subheader("Chat")
messages = st.session_state.get("messages", [])
user_count = sum(1 for m in messages if m["role"] == "user")
st.metric("Pesan dari user", user_count)

with st.expander("Lihat semua pesan"):
    for m in messages:
        st.write(f"**{m['role']}**: {m['content']}")