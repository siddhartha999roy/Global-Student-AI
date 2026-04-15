import streamlit as st
from groq import Groq

# ১. নতুন পেজ সেটআপ এবং আইকন/টাইটেল পরিবর্তন
st.set_page_config(page_title="Medi-Assistant AI", page_icon="💊")

# ২. CSS ব্যবহার করে নিচের বার এবং প্রোফাইল লুকানো (আপনার অনুরোধ অনুযায়ী)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stAppDeployButton {display:none;}
            [data-testid="stToolbar"] {visibility: hidden !important;}
            [data-testid="stDecoration"] {display:none !important;}
            /* নিচের প্রোফাইল এবং লাল 'Hosted with Streamlit' বার লুকানোর জন্য */
            div[data-testid="stStatusWidget"] {display:none !important;}
            div[data-testid="stStatusWidget"] + div {display:none !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("🤖 Medi-Assistant AI")
st.markdown("---")

# Groq চাবি কানেক্ট করা
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Secrets-এ GROQ_API_KEY খুঁজে পাওয়া যায়নি! অনুগ্রহ করে Streamlit Cloud এর Secrets-এ এটি যোগ করুন।")
    st.stop()

# সাইডবারে ফাইল আপলোড সেকশন
with st.sidebar:
    st.header("📄 Medical Records / Research")
    uploaded_file = st.file_uploader("আপনার প্রেসক্রিপশন বা রিসার্চ ফাইল আপলোড করুন...", type=['png', 'jpg', 'jpeg', 'pdf'])
    if uploaded_file is not None:
        st.success(f"ফাইল: {uploaded_file.name} আপলোড হয়েছে!")
    
    st.info("আমি আপনাকে ওষুধ, জেনেটিক ইঞ্জিনিয়ারিং এবং স্বাস্থ্য বিষয়ক তথ্য দিয়ে সাহায্য করতে পারি।")

# চ্যাট হিস্ট্রি মেনটেইন করা
if "messages" not in st.session_state:
    st.session_state.messages = []

# পুরনো মেসেজগুলো প্রদর্শন করা
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ইউজার ইনপুট এবং AI রেসপন্স
if prompt := st.chat_input("ওষুধ বা স্বাস্থ্য নিয়ে কিছু জিজ্ঞাসা করুন..."):
    
    # ইউজার মেসেজ হিস্ট্রিতে যোগ করা
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI রেসপন্স জেনারেট করা
    with st.chat_message("assistant"):
        try:
            # সিস্টেম ইন্সট্রাকশন (আপনার পছন্দ অনুযায়ী নামও আপডেট করা হয়েছে)
            system_instruction = {
                "role": "system", 
                "content": "You are Medi-Assistant AI. You specialize in Biotechnology and Medical information. Answer in Bengali if the user asks in Bengali. Always provide a disclaimer that medical information should be verified by a doctor."
            }
            
            # API কল করা
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[system_instruction] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )
            
            response = completion.choices[0].message.content
            st.markdown(response)
            
            # রেসপন্স হিস্ট্রিতে যোগ করা
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {e}")

# ফুটারে ডিসক্লেইমার
st.markdown("---")
st.caption("⚠️ এটি একটি AI সাহায্যকারী। গুরুতর প্রয়োজনে অভিজ্ঞ ডাক্তারের পরামর্শ নিন।")
