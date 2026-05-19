import streamlit as st
from groq import Groq
from PIL import Image
import requests
from io import BytesIO
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="AI Vehicle Comparison System",
    page_icon="🚗",
    layout="wide"
)

# Initialize Groq Client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Title
st.title("🚗 AI-Powered Vehicle Comparison & Recommendation System")

st.markdown(
    """
    Compare any two vehicles using AI and get:
    - Engine Specifications
    - Mileage
    - Top Speed
    - Features
    - Pros & Cons
    - Price Comparison
    - AI Recommendation
    """
)

# Sidebar
st.sidebar.header("⚙️ Filters")

fuel_type = st.sidebar.selectbox(
    "Select Fuel Type",
    ["Any", "Petrol", "Diesel", "Electric", "Hybrid"]
)

budget = st.sidebar.selectbox(
    "Select Budget",
    [
        "Any",
        "Under 5 Lakhs",
        "5 - 10 Lakhs",
        "10 - 20 Lakhs",
        "20+ Lakhs"
    ]
)

vehicle_type = st.sidebar.selectbox(
    "Vehicle Type",
    ["Any", "Car", "Bike", "SUV", "Sports"]
)

# User Inputs
col1, col2 = st.columns(2)

with col1:
    vehicle1 = st.text_input("🚘 Enter First Vehicle")

with col2:
    vehicle2 = st.text_input("🏍️ Enter Second Vehicle")

# Function to fetch images
def get_vehicle_image(vehicle_name):

    try:
        url = f"https://source.unsplash.com/600x400/?{vehicle_name},vehicle"

        response = requests.get(url)

        img = Image.open(BytesIO(response.content))

        return img

    except:
        return None

# Compare Button
if st.button("🔍 Compare Vehicles"):

    if vehicle1 == "" or vehicle2 == "":
        st.warning("Please enter both vehicle names")

    else:

        st.divider()

        # Display Images
        st.subheader("📸 Vehicle Images")

        img_col1, img_col2 = st.columns(2)

        image1 = get_vehicle_image(vehicle1)
        image2 = get_vehicle_image(vehicle2)

        with img_col1:

            if image1:
                st.image(
                    image1,
                    caption=vehicle1,
                    use_container_width=True
                )
            else:
                st.error("Image not found")

        with img_col2:

            if image2:
                st.image(
                    image2,
                    caption=vehicle2,
                    use_container_width=True
                )
            else:
                st.error("Image not found")

        st.divider()

        # AI Prompt
        prompt = f"""
        Compare these two vehicles in detail.

        Vehicle 1: {vehicle1}
        Vehicle 2: {vehicle2}

        User Preferences:
        Fuel Type: {fuel_type}
        Budget: {budget}
        Vehicle Type: {vehicle_type}

        Provide comparison based on:
        1. Engine Specifications
        2. Mileage
        3. Top Speed
        4. Key Features
        5. Safety Features
        6. Pros and Cons
        7. Approximate Price
        8. Which vehicle is better and why

        Give the response in a clean structured format.
        """

        with st.spinner("🤖 AI is generating comparison..."):

            try:

                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert automobile analyst."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=1500
                )

                result = response.choices[0].message.content

                st.subheader("📊 AI Vehicle Comparison Result")

                st.markdown(result)

                st.success("✅ Comparison Generated Successfully")

            except Exception as e:

                st.error(f"Error: {e}")

# Footer
st.divider()

st.caption(
    "Built using Streamlit + Groq API + Llama 3.1"
)