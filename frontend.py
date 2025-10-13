import streamlit as st
import requests
import os
import base64
import uuid
from pathlib import Path

st.set_page_config(page_title="Whiteboard to PPT", layout="centered")

st.title("📊 Whiteboard to PowerPoint Agent")
st.markdown("Convert your whiteboard photos into beautiful presentations instantly!")

# Configuration
API_URL = "http://localhost:8000"
APP_NAME = "owl"
OUTPUT_FILE = "presentation.pptx"


def image_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode()


col1, col2 = st.columns(2)

with col1:
    LANGUAGE = st.selectbox(
        "Select Language",
        [
            "English",
            "Arabic",
            "French",
            "German",
            "Italian",
            "Japanese",
            "Korean",
            "Portuguese",
            "Russian",
            "Spanish",
            "Chinese",
            "Vietnamese",
        ],
    )
    st.subheader("Upload Image")
    uploaded_image = st.file_uploader(
        "Choose a whiteboard image",
        type=["jpg", "jpeg", "png", "webp"],
        help="Upload a photo of your whiteboard or canvas",
    )

    if uploaded_image:
        st.image(uploaded_image, use_column_width=True, caption="Uploaded Image")

with col2:
    st.subheader("Preview")
    if os.path.exists(OUTPUT_FILE):
        st.success("✓ Presentation ready!")

        file_size = Path(OUTPUT_FILE).stat().st_size / (1024 * 1024)
        st.metric("File Size", f"{file_size:.2f} MB")

        with open(OUTPUT_FILE, "rb") as f:
            st.download_button(
                label="📥 Download PPTX",
                data=f,
                file_name=OUTPUT_FILE,
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            )
    else:
        st.info("🔄 No presentation yet. Upload an image and process it.")

if uploaded_image:
    if st.button("🚀 Generate Presentation", use_container_width=True):
        with st.spinner("Processing your image..."):
            try:
                # Generate unique session IDs
                user_id = "user_123"
                session_id = f"session_{uuid.uuid4().hex[:8]}"

                # Encode image to base64 with proper format
                image_bytes = uploaded_image.getvalue()
                image_base64 = image_to_base64(image_bytes)
                mime_type = f"image/{uploaded_image.type.split('/')[-1]}"  # Get MIME type from uploaded file

                # Create session
                session_response = requests.post(
                    f"{API_URL}/apps/{APP_NAME}/users/{user_id}/sessions/{session_id}",
                    json={},
                    timeout=10,
                )

                if session_response.status_code not in [200, 201]:
                    st.error(f"❌ Failed to create session: {session_response.text}")
                    st.stop()

                st.success("✓ Session created")

                # Step 2: Send image to agent
                st.info("Sending the Whiteboard image to the agent...")

                # Send image to agent as base64
                run_response = requests.post(
                    f"{API_URL}/run",
                    json={
                        "appName": APP_NAME,  # changed to camelCase
                        "userId": user_id,
                        "sessionId": session_id,
                        "newMessage": {
                            "role": "user",
                            "parts": [
                                {
                                    "text": f"Describe this image strictly in the following Language: \n{LANGUAGE}"  # add text part if desired
                                },
                                {
                                    "inlineData": {
                                        "data": image_base64,  # just base64
                                        "mimeType": mime_type,  # "image/jpeg"
                                    }
                                },
                            ],
                        },
                        "streaming": False,
                    },
                    timeout=60,
                )

                if run_response.status_code != 200:
                    st.error(f"❌ Error: {run_response.text}")
                    st.stop()

                st.success("✓ Agent processed image")

                if os.path.exists(OUTPUT_FILE):
                    st.success("✅ Presentation generated successfully!")
                    st.rerun()
                else:
                    st.warning(
                        "⚠️ Agent executed but PPTX file not found. Check agent logs."
                    )

            except requests.exceptions.ConnectionError:
                st.error(
                    "❌ Cannot connect to backend. Make sure Google ADK server is running on localhost:8000"
                )
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.markdown("---")
st.markdown(
    """
    Made with ❤️ for the Agents for Impact Hackathon
    
    **How it works:**
    1. Upload a whiteboard image
    2. Google ADK agent analyzes the content
    3. Generates a professional presentation
    4. Download your PPTX
    """
)
