import platform, atexit, subprocess, os, time, urllib.request
import streamlit as st
import os

PORT_BROWSER=9222

class OSIdentifier:
    def __init__(self) -> None:
        self.os_name = platform.system()
        self.os_version = platform.version()
        self.os_release = platform.release()

    def identify(self):
        return f"{self.os_name} {self.os_release} ({self.os_version})"

st.set_page_config(page_title="Knowledge Engine POC", layout="wide")

st.title("Knowledge Engine POC")

# ---------- Chat helpers ----------
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "kind": "text", "content": "Welcome to the Streamlit demo! Silakan ketik pesan di bawah."}
    ]

def render_message(msg):
    with st.chat_message(msg["role"]):
        kind = msg["kind"]
        if kind == "success":
            st.success(msg["content"])
        elif kind == "warning":
            st.warning(msg["content"])
        elif kind == "info":
            st.info(msg["content"])
        elif kind == "error":
            st.error(msg["content"])
        else:
            st.write(msg["content"])

def add_message(role, content, kind="text"):
    """Simpan ke history dan langsung tampilkan."""
    msg = {"role": role, "kind": kind, "content": content}
    st.session_state["messages"].append(msg)
    render_message(msg)

# ---------- Sidebar (tombol-tombol) ----------
with st.sidebar:
    st.header("Controls")
    launch_clicked = st.button("Check OS and Launch Browser", use_container_width=True)
    if st.button("Clear chat", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()

# ---------- Tampilkan history chat ----------
for msg in st.session_state["messages"]:
    render_message(msg)

# ---------- Input chat (pengganti text_input + Submit) ----------
user_input = st.chat_input("Enter some text...")

if user_input:
    add_message("user", user_input)
    add_message("assistant", f"You entered: {user_input}", kind="success")

# ---------- Logic Check OS and Launch Browser (tidak diubah) ----------
if launch_clicked:
    add_message("user", "Check OS and Launch Browser")

    os_id = OSIdentifier()
    os_info = os_id.identify()
    add_message("assistant", f"Current OS: {os_info}")

    pid_file = ".browser_pid"
    current_os = platform.system()

    if current_os in ["Linux", "Darwin"]:
        is_running = False
        if "browser_proc" in st.session_state:
            is_running = st.session_state.browser_proc.poll() is None
        if os.path.exists(pid_file):
            try:
                with open(pid_file, "r") as f:
                    pid = int(f.read().strip())
                os.kill(pid, 0)
                print("is true")
                is_running = True
            except (OSError, ValueError, ProcessLookupError):
                print("is false")
                is_running = False

        if is_running:
            add_message("assistant", f"Browser started by this app is already running on {current_os}.", kind="warning")
        else:
            add_message("assistant", f"{current_os} detected. Launching Browser...", kind="info")
            try:
                if current_os == "Linux":
                    process = subprocess.Popen(["chromium-browser",f"--remote-debugging-port={PORT_BROWSER}"])
                    st.session_state["browser_proc"] = process
                else: # Darwin (macOS)
                    process = subprocess.Popen(["open", "-a", "Google Chrome"])
                    st.session_state["browser_proc"] = process

                with open(pid_file, "w") as f:
                    f.write(str(process.pid))
                add_message("assistant", "Browser launched successfully!", kind="success")
            except FileNotFoundError:
                add_message("assistant", "Browser command not found.", kind="error")
    else:
        add_message("assistant", "Browser launch is only supported on Linux and macOS in this POC.", kind="warning")