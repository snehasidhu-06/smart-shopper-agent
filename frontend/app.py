import streamlit as st
import pandas as pd
import requests

API_URL = API_URL = "https://smart-shopper-agent.onrender.com/chat"

st.set_page_config(page_title="Smart Shopper Agent", page_icon="🛍️")

st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
    }
    h1 {
        color: #00D4FF;
        text-align: center;
    }
    .stChatMessage {
        background-color: #1C1F26;
        border-radius: 15px;
        padding: 12px;
        border: 1px solid #2A2E37;
    }
    div[data-testid="stImage"] img {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,212,255,0.15);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛍️ Smart E-Commerce Personal Shopper")
st.write("Tell me what you're looking for, and I'll recommend the best products!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("E.g. I need a casual polo shirt for men")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Finding the best products for you..."):
            try:
                response = requests.post(API_URL, json={"message": user_input})
                data = response.json()
                reply = data.get("reply", "Sorry, something went wrong.")
                results = data.get("products", [])
            except Exception as e:
                reply = f"Could not connect to backend API. Error: {e}"
                results = []

            st.markdown(reply)

            if results:
                st.write("---")
                st.write("**Matching Products:**")

                cols = st.columns(3)
                for i, product in enumerate(results):
                    with cols[i % 3]:
                        image_url = product.get("image_url")
                        if image_url and str(image_url).startswith("http"):
                            try:
                                st.image(image_url, use_container_width=True)
                            except:
                                st.image("https://via.placeholder.com/200x200.png?text=No+Image", use_container_width=True)
                        else:
                            st.image("https://via.placeholder.com/200x200.png?text=No+Image", use_container_width=True)

                        st.markdown(f"**{product['title'][:50]}...**")
                        st.markdown(f"""
                            <div style="background-color:#1C1F26; padding:10px; border-radius:8px; margin-top:5px; border: 1px solid #2A2E37;">
                                <span style="color:#00D4FF; font-weight:bold;">${product['price']}</span> | ⭐ {product['rating']}<br>
                                <span style="font-size:12px; color:#AAAAAA;">{product['brand']}</span><br>
                                <span style="font-size:12px; color:#AAAAAA;">{product['category']} | {product['availability']}</span>
                            </div>
                        """, unsafe_allow_html=True)

                        if product.get("product_link"):
                            st.link_button("🛒 Buy Now", product["product_link"], use_container_width=True)

    st.session_state.messages.append({"role": "assistant", "content": reply})