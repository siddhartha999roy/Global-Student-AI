import streamlit as st
import google.generativeai as genai

# পেজ সেটআপ
st.set_page_config(page_title="Global Student AI", page_icon="🎓")
st.title("🎓 Global Student AI")

# Streamlit Secrets থেকে সরাসরি API Key নেওয়া (নিরাপদ পদ্ধতি)
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
else:
    st.error("API Key খুঁজে পাওয়া যায়নি! দয়া করে Streamlit Secrets চেক করুন।")
    st.stop()

# মডেল ইনিশিয়ালাইজ (Flash মডেলটি দ্রুত এবং ফ্রি কোটা বেশি দেয়)
model = genai.GenerativeModel('gemini-1.5-flash')

# চ্যাট হিস্ট্রি
if "messages" not in st.session_state:
    st.session_state.messages = []

# চ্যাট হিস্ট্রি প্রদর্শন
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ইউজার ইনপুট ও এআই রেসপন্স
if prompt := st.chat_input("Ask me anything about Genetic Engineering or more..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # যদি কোটা শেষ হয়ে যায় তবে এই মেসেজটি দেখাবে
            st.error(f"দুঃখিত, গুগল এপিআই লিমিট শেষ হয়েছে। কিছুক্ষণ পর আবার চেষ্টা করুন। বিস্তারিত: {e}")
