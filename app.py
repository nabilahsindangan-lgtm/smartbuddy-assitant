import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Productivity AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Personal Productivity & Study Assistant")
st.caption("Chatbot berbasis AI untuk membantu produktivitas, manajemen waktu, dan belajar.")

# Input API Key di Sidebar
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    api_key = st.text_input("Masukkan Google Gemini API Key:", type="password")
    
    st.markdown("---")
    st.markdown("### 💡 Fitur Cepat")
    if st.button("📝 Rangkum Catatan Belajar"):
        st.session_state.prompt_preset = "Bantu saya merangkum poin-poin penting dari teks berikut:"
    if st.button("📅 Buat Schedule Pomodoro"):
        st.session_state.prompt_preset = "Buatkan jadwal belajar 2 jam menggunakan teknik Pomodoro untuk topik:"

if not api_key:
    st.warning("Silakan masukkan Google Gemini API Key Anda di sidebar untuk memulai.")
    st.stop()

# Inisialisasi API
genai.configure(api_key=api_key)

# Inisialisasi Model dengan System Instruction
system_instruction = """
Anda adalah 'SmartBuddy', seorang asisten personal produktivitas dan belajar yang ramah, santai, namun profesional.
Tugas utama Anda:
1. Membantu pengguna mengatur jadwal dan teknik manajemen waktu (seperti Pomodoro/Eisenhower Matrix).
2. Membantu merangkum materi pelajaran atau catatan.
3. Memberikan tips motivasi dan fokus belajar.
Gunakan bahasa Indonesia yang santai, jelas, dan menyemangati. Gunakan emoji agar obrolan menarik.
"""

model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    system_instruction=system_instruction
)

# Inisialisasi Chat Memory di Session State
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Menampilkan Riwayat Chat
for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Menangani Preset Prompt jika diklik dari Sidebar
initial_prompt = ""
if "prompt_preset" in st.session_state:
    initial_prompt = st.session_state.pop("prompt_preset")

# Input Pengguna
if user_input := st.chat_input("Ketik pesan Anda di sini...", key="chat_input") or initial_prompt:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = st.session_state.chat_session.send_message(user_input)
        message_placeholder.markdown(response.text)
