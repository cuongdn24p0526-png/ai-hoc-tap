import streamlit as st
from openai import OpenAI
import speech_recognition as sr

# ===============================
# CẤU HÌNH TRANG
# ===============================
st.set_page_config(page_title="AI HỌC TẬP TOÀN DIỆN", page_icon="📘")
st.title("📘 AI HỖ TRỢ HỌC TẬP")

# ===============================
# KẾT NỐI OPENAI
# ===============================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ===============================
# CHỌN CHẾ ĐỘ
# ===============================
mode = st.selectbox(
    "Chọn chức năng:",
    ["Giải Toán",
     "Phân tích Văn",
     "So sánh với câu trả lời học sinh",
     "Phân tích lỗi tư duy"]
)

# ===============================
# NHẬP BẰNG GIỌNG NÓI
# ===============================
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Đang nghe...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            return text
        except:
            return "Không nhận diện được giọng nói"

if st.button("🎤 Nhập bằng giọng nói"):
    user_input = speech_to_text()
    st.write("Bạn nói:", user_input)
else:
    user_input = st.text_area("Nhập câu hỏi của bạn:")

# ===============================
# TẠO PROMPT THEO CHẾ ĐỘ
# ===============================
def build_prompt(mode, question):
    if mode == "Giải Toán":
        return f"""
        Giải bài toán sau một cách chi tiết, giải thích từng bước rõ ràng:
        {question}
        """
    elif mode == "Phân tích Văn":
        return f"""
        Phân tích bài văn sau theo cấu trúc luận đề - luận điểm - dẫn chứng:
        {question}
        """
    elif mode == "So sánh với câu trả lời học sinh":
        return f"""
        So sánh câu trả lời của học sinh với đáp án chuẩn.
        Chỉ ra điểm đúng, sai và mức điểm phù hợp:
        {question}
        """
    elif mode == "Phân tích lỗi tư duy":
        return f"""
        Phân tích lỗi tư duy nếu có trong lời giải sau:
        {question}
        """

# ===============================
# GỬI YÊU CẦU ĐẾN OPENAI
# ===============================
if st.button("🚀 Phân tích"):
    if user_input.strip() == "":
        st.warning("Vui lòng nhập câu hỏi")
    else:
        prompt = build_prompt(mode, user_input)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        st.subheader("📌 Kết quả:")
        st.write(response.choices[0].message.content)