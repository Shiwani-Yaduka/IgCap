import streamlit as st
from PIL import Image
import google.generativeai as genai
import random
import io

# Set Streamlit layout
st.set_page_config(page_title="Vibe Caption Generator", layout="centered")
st.title("🎶 Igcap — Insta Caps n songs ")

# 🔐 Set your Gemini API key
genai.configure(api_key="API_KEY")  # Replace with your actual Gemini key

# Load the Gemini Flash Vision model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Function to generate caption + song
def generate_caption_with_song(image: Image.Image):
    # Convert image to bytes
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)

    prompt = """
    Analyze this photo and give me:
    1. A Gen-Z, aesthetic Instagram-style caption — like something vibey, cozy, modern and fun.
    2. A song suggestion that matches the emotion, style or vibe of this image (new age, chill, lo-fi or pop vibe).

    Format:
    Caption: <your caption>
    Song: <artist - song name>
    """

    try:
        response = model.generate_content([
            prompt,
            {"mime_type": "image/png", "data": image_bytes.read()}
        ])
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Generate Caption with Song Vibe"):
        with st.spinner("Analyzing image & vibin’... 🎧"):
            output = generate_caption_with_song(image)

        # Display results
        if "Caption:" in output and "Song:" in output:
            caption = output.split("Caption:")[1].split("Song:")[0].strip()
            song = output.split("Song:")[1].strip()

            st.subheader("📝 Insta-Ready Caption")
            st.markdown(f"{caption}")

            st.subheader("🎵 Song Suggestion")
            st.markdown(f"{song}")
        else:
            st.warning("Didn't receive expected response. Here's the raw output:")
            st.text(output)
