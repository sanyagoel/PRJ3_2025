import streamlit as st
import asyncio
from Agents.orchestratorAgent import orchestratorAgent
from Agents.orchestrator2Agent import orchestrator2Agent

import os

st.set_page_config(page_title="Ask advices", layout="centered")

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
            # print('RESULT2', result2)
            st.json(result2)
            
            

