import streamlit as st
import google.generativeai as genai

# এখানে আপনার API Key-টি সাবধানে দিন
API_KEY = "আপনার_API_KEY_এখানে_দিন"
genai.configure(api_key="AIzaSyCD5zEfMr1dMc7JXpEFC1V_75AbI8W4KPs")

st.title("🎓 Global Student AI")

# এটি আপনার Key দিয়ে কোন মডেল চলবে তা নিজে খুঁজে নেবে
@st.cache_resource
def get_working_model():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # যদি flash থাকে তবে সেটা নেবে, না হলে প্রথম যেটা পায় সেটা নেবে
    for m_name in available_models:
        if 'gemini-1.5-flash' in m_name:
            return m_name
    return available_models[0] if available_models else None

try:
    working_model_name = get_working_model()
    model = genai.GenerativeModel(working_model_name)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = model.generate_content(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    st.error(f"Error: {e}")
    st.info("আপনার Google AI Studio-তে গিয়ে দেখুন API Key-টি Active আছে কি না।")
