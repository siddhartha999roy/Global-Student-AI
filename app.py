import streamlit as st
from groq import Groq

# ১. পেজ সেটআপ
st.set_page_config(page_title="Medi-Assistant AI", page_icon="💊")

# ২. কঠোরভাবে প্রোফাইল এবং ক্লিক ব্লক করার CSS
hide_and_block_style = """
    <style>
    /* মেনু, ফুটার এবং ড্যাপ্লয় বাটন হাইড করা */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display:none;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    [data-testid="stDecoration"] {display:none !important;}

    /* ৩. নিচের 'Hosted with Streamlit' বার এবং প্রোফাইল আইকন ক্লিক ব্লক করা */
    /* এটি এলিমেন্টটিকে স্ক্রিন থেকে সরিয়ে দিবে এবং ক্লিক করার ক্ষমতা কেড়ে নিবে */
    div[data-testid="stStatusWidget"] {
        display: none !important;
        pointer-events: none !important;
    }
    
    /* বাড়তি সুরক্ষা: যদি কোনোভাবে আইকনটি দেখা যায়ও, তবে ক্লিক যেন কাজ না করে */
    a[href*="streamlit.io/cloud"] {
        pointer-events: none !important;
        cursor: default !important;
    }

    /* ৪. পুরো অ্যাপের নিচের সেকশনে ক্লিক প্রতিরোধ করা */
    .stApp > header {
        display: none !important;
    }
    </style>
    """
st.markdown(hide_and_block_style, unsafe_allow_html=True)

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
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            system_instruction = {
                "role": "system", 
                "content": "You are Medi-Assistant AI. You specialize in Biotechnology and Medical information. Answer in Bengali if the user asks in Bengali. Always provide a disclaimer that medical information should be verified by a doctor."
            }
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[system_instruction] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )
            
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {e}")

st.markdown("---")
st.caption("⚠️ এটি একটি AI সাহায্যকারী। গুরুতর প্রয়োজনে অভিজ্ঞ ডাক্তারের পরামর্শ নিন।")
