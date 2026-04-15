import streamlit as st
from groq import Groq

# নতুন পেজ সেটআপ
st.set_page_config(page_title="Medi-Assistant AI", page_icon="🤖")

# প্রোফাইল নাম এবং টাইটেল আপডেট
st.title("🤖 Medi-Assistant AI")
st.caption("Developed by: East West University Genetic Engineering Department")
st.markdown("---")

# Groq চাবি কানেক্ট করা
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Secrets-এ GROQ_API_KEY খুঁজে পাওয়া যায়নি! অনুগ্রহ করে Streamlit Cloud এর Secrets-এ এটি যোগ করুন।")
    st.stop()

# সাইডবারে ফাইল আপলোড সেকশন
with st.sidebar:
    st.header("📄 Medical Records")
    uploaded_file = st.file_uploader("আপনার প্রেসক্রিপশন বা রিসার্চ ফাইল আপলোড করুন...", type=['png', 'jpg', 'jpeg', 'pdf'])
    if uploaded_file is not None:
        st.success(f"ফাইল: {uploaded_file.name} আপলোড হয়েছে!")
    
    st.markdown("---")
    st.info("আমি আপনাকে ওষুধ, জেনেটিক ইঞ্জিনিয়ারিং এবং স্বাস্থ্য বিষয়ক তথ্য দিয়ে সাহায্য করতে পারি।")
    
    # চ্যাট হিস্ট্রি ক্লিয়ার করার বাটন
    if st.sidebar.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# চ্যাট হিস্ট্রি মেনটেইন করা
if "messages" not in st.session_state:
    st.session_state.messages = []

# পুরনো মেসেজগুলো প্রদর্শন করা
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ইউজার ইনপুট এবং AI রেসপন্স
if prompt := st.chat_input("ওষুধ বা স্বাস্থ্য নিয়ে কিছু জিজ্ঞাসা করুন..."):
    
    # ইউজার মেসেজ হিস্ট্রিতে যোগ করা
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI রেসপন্স জেনারেট করা
    with st.chat_message("assistant"):
        try:
            # আপডেট করা সিস্টেম ইন্সট্রাকশন
            system_instruction = {
                "role": "system", 
                "content": "You are Medi-Assistant AI, a specialized tool for the Medi-Directory platform created by the Genetic Engineering Department of East West University. You specialize in Biotechnology, Molecular Biology, and Medical information. Answer in Bengali if the user asks in Bengali. Always emphasize that medical information must be verified by a registered physician."
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
            st.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {e}")

# ফুটারে ডিসক্লেইমার
st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 12px; color: gray;'>"
    "Made by East West University Genetic Engineering Department<br>"
    "⚠️ এটি একটি AI সাহায্যকারী। গুরুতর প্রয়োজনে অভিজ্ঞ ডাক্তারের পরামর্শ নিন।"
    "</div>", 
    unsafe_allow_html=True
)
