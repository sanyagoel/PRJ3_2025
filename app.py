import streamlit as st
import asyncio
from Agents.orchestratorAgent import orchestratorAgent

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

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🧑‍💼 Event Advisor")
    st.write("Get personalized advice for your next event.")
    # Navigation button for this page
    if st.button("Ask advices", key="nav_ask_advices"):
        st.session_state.page = "Ask advices"

# --- MAIN PAGE ---
if st.session_state.page == "Ask advices":
    st.header("🎯 Ask for Event Advice")

    # --- IMAGE UPLOAD ---
    uploaded_image = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"], key="event_image")

    # --- USER QUERY ---
    event_type = st.text_input("What type of event are you going to?", key="event_type")

    # --- PRICE RANGE SLIDER ---
    price_range = st.slider(
        "Select your preferred price range",
        min_value=0,
        max_value=10000,
        value=(1000, 5000),
        step=100,
        key="price_range"
    )

    # --- GENDER INPUT ---
    gender = st.text_input("What is your gender?", key="gender")

    # --- SUBMIT BUTTON ---
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
                st.write(result.get("dresstypes"))
