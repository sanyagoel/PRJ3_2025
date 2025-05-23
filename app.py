import streamlit as st
import asyncio
from Agents.orchestratorAgent import orchestratorAgent
from Agents.orchestrator2Agent import orchestrator2Agent

import requests
from PIL import Image
from io import BytesIO


import os

st.set_page_config(page_title="Ask advices", layout="centered")
# Custom CSS styles
st.markdown("""
    <style>
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%);
        color: #000000;
    }

    /* Sidebar title */
    .sidebar .css-1d391kg {
        font-size: 24px;
        color: #5B2C6F;
        font-weight: bold;
    }

    /* Buttons */
    .stButton > button {
        background-color: #FF69B4;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: background-color 0.3s;
    }

    .stButton > button:hover {
        background-color: #FF1493;
        color: #fff;
    }

    /* Input boxes */
    .stTextInput > div > div > input {
        background-color: #F0F8FF;
        border: 2px solid #87CEFA;
        border-radius: 8px;
    }

    .stSlider > div > div {
        background-color: #E6E6FA;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)


# --- PAGE NAVIGATION (for multipage setup) ---
if "page" not in st.session_state:
    st.session_state.page = "Ask advices"

# --- Async orchestrator function as provided ---
async def process_query(user_input):
    try:
        orchestrator = orchestratorAgent()
        return await orchestrator.run([{"role": "user", "content": user_input}])
    except Exception as e:
        return {"error": str(e)}
    
async def process_secondhalf(user_input):
    try:
        
        orchestrator2 = orchestrator2Agent()
        return await orchestrator2.run([{"role": "user", "content": user_input}])
        
    except Exception as e:
        return {"error" : str(e)}
    

def show_Products(brand, product_lists):
    if not product_lists:
        return

    st.markdown(f"### 🧾 Results from **{brand.capitalize()}**")

    cols = st.columns(3)
    index = 0

    for group in product_lists:
        for product in group:
            if index >= 5:
                break

            with cols[index % 3]:
                with st.container(border=True):
                    img_url = product.get('image_url')
                    if img_url:
                        try:
                            img_data = requests.get(img_url).content
                            img = Image.open(BytesIO(img_data))
                            st.image(img, use_container_width=True)
                        except:
                            st.warning("Image unavailable")

                    st.markdown(f"**{product.get('name', 'Unnamed Product')}**")
                    st.markdown(f"Description ->  \n {product.get('description')}", unsafe_allow_html=True)

                    price = product.get('price', 'N/A')
                    rating = product.get('rating')
                    st.markdown(f"💰 {price}" + (f" | ⭐ {rating}" if rating else ""))

                    if product.get('url'):
                        st.markdown(f"[View Product 🔎]({product['url']})", unsafe_allow_html=True)

                    reviews = [
                        r.strip() for r in product.get('review', [])
                        if r.strip() and "no review" not in r.lower()
                    ]
                    if reviews:
                        with st.expander("🗨 Reviews"):
                            for r in reviews:
                                st.markdown(f"- {r}")

            index += 1

    st.markdown("---")



        

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🧑‍💼 Event Advisor")
    st.write("Get personalized advice for your next event.")
    if st.button("Ask advices", key="nav_ask_advices"):
        st.session_state.page = "Ask advices"

# --- PAGE 1: Ask advices ---
if st.session_state.page == "Ask advices":
    st.header("🎯 Ask for Event Advice")

    uploaded_image = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"], key="event_image")
    event_type = st.text_input("What type of event are you going to?", key="event_type")
    price_range = st.slider(
        "Select your preferred price range",
        min_value=0,
        max_value=10000,
        value=(1000, 5000),
        step=100,
        key="price_range"
    )
    gender = st.text_input("What is your gender?", key="gender")

    if st.button("Get Advice", key="submit_advice"):
        if not event_type.strip():
            st.warning("Please specify the event type.")
        else:
            user_input = {
                "event_type": event_type,
                "price_range": price_range,
                "has_image": uploaded_image is not None,
                "gender": gender
            }
            if uploaded_image:
                image_path = f"./user_images/userimage.jpeg"
                with open(image_path, "wb") as f:
                    f.write(uploaded_image.getbuffer())
                user_input["image_path"] = image_path

            with st.spinner("Fetching advice..."):
                result = asyncio.run(process_query(user_input))

            if "error" in result:
                st.error(result["error"])
            else:
                st.success("Here's your personalized advice!")
                # Save results in session state and switch to next page
                st.session_state.page = "Show Images"
                st.session_state.dress_types = result.get("scraped_content").get("dress_types", [])
                st.session_state.gender_result = result.get("scraped_content").get("gender")
                st.session_state.price_range2 = result.get("scraped_content").get("price range")


import os

if st.session_state.page == "Show Images":
    st.header("🖼️ Select Your Favorite Outfits")
    selected_images = []
    if "dress_types" in st.session_state:
        for idx, dress_items in enumerate(st.session_state.dress_types):
            item_paths = []
            for item in dress_items:
                item_filename = item.strip().lower().replace(' ', '_') + '.jpg'
                img_path = os.path.join(".", "Outputs", "dress_type_images", item_filename)
                # print(f"Looking for: {img_path}")  
                item_paths.append((item, img_path))
            # print('ITEM PATHS',item_paths)
            if all(os.path.exists(path) for _, path in item_paths):
                st.markdown(f"**Outfit {idx+1}:**")
                checked = st.checkbox(
                    ", ".join(item for item, _ in item_paths),
                    key=f"checkbox_outfit_{idx}"
                )
                cols = st.columns(len(item_paths))
                for col, (item, path) in zip(cols, item_paths):
                    with col:
                        st.image(path, caption=item, width=150)
                if checked:
                    selected_images.append([item for item, _ in item_paths])
        if st.button("Send similar outfits"):
            print('SELECTED IMAGES : ',selected_images)

   # min_range = content["price_range"][0]
        # max_range = content["price_range"][1]
        # gender = content["gender"]
        # selected_list = content["selected_dresses"]
            content = {
                "price_range" : st.session_state.price_range2,
                "gender" : st.session_state.gender_result,
                "selected_dresses" : selected_images
            }
            
            # st.json(selected_images)
            # st.json(selected_images)
            result2 = asyncio.run(process_secondhalf(content))
            print('RESULT2', result2)
            if "messages" in result2:
                messages = result2["messages"]
                if "myntra" in messages or "flipkart" in messages or "tata" in messages:
                    st.success("Here are some similar outfits:")

                    if "myntra" in messages:
                        show_Products("Myntra", messages["myntra"])

                    if "flipkart" in messages:
                        show_Products("Flipkart", messages["flipkart"])

                    if "tata" in messages:
                        show_Products("Tata CLiQ", messages["tata"])
                else:
                    st.warning("Could not find similar products.")
            else:
                st.warning("No messages found in result.")



            
            

