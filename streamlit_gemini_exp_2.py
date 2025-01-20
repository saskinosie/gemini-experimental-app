import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
from datetime import datetime
import time
import tempfile
import os

def local_css():

    """Add custom CSS for styling chat messages and other UI elements.

    - Hides certain Streamlit container styles for a cleaner UI.
    - Defines custom styles for chat messages, including alignment, 
      background colors, border radius, and timestamp styling.
    """

    st.markdown("""
        <style>
            div[data-testid="stMarkdownContainer"] > style {
                display: none;
            }
            .chat-message {
                padding: 1rem;
                border-radius: 0.5rem;
                margin-bottom: 1rem;
                display: flex;
                flex-direction: column;
            }
            .user-message {
                background-color: #e6f3ff;
                margin-left: 2rem;
                border-bottom-right-radius: 0.2rem;
            }
            .assistant-message {
                background-color: #f0f2f6;
                margin-right: 2rem;
                border-bottom-left-radius: 0.2rem;
            }
            .message-content {
                margin-bottom: 0.5rem;
            }
            .message-timestamp {
                color: #666;
                font-size: 0.8em;
                align-self: flex-end;
            }
        </style>
    """, unsafe_allow_html=True)

def initialize_session_state():

    """Initialize session state variables for the app.

    - Ensures consistent behavior across sessions by setting default values
      for variables such as chat object, user messages, system prompt,
      selected model, and temperature.
    - Avoids errors when accessing session state keys that may not exist.
    """
    if "chat" not in st.session_state:
        st.session_state.chat = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "system_prompt" not in st.session_state:
        st.session_state.system_prompt = "You are a helpful AI assistant."
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "gemini-exp-1206"
    if "temperature" not in st.session_state:
        st.session_state.temperature = 0.7  # default temperature

def create_chat():

    """Start a Generative AI chat instance.

    - Configures the Generative AI API with the user's API key.
    - Creates a chat object using the selected model and generation
      temperature, allowing for interactive conversations.
    """
    if st.session_state.api_key:
        genai.configure(api_key=st.session_state.api_key)
        model = genai.GenerativeModel(
            st.session_state.selected_model,
            generation_config={"temperature": st.session_state.temperature}
        )
        st.session_state.chat = model.start_chat()

def process_video(video_file):
    """Handle video upload and processing."""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            tmp_file.write(video_file.getvalue())
            video_path = tmp_file.name
        
        with st.status("Processing video...") as status:
            status.write("Uploading file...")
            uploaded_video = genai.upload_file(path=video_path)
            status.write(f"Upload completed: {uploaded_video.uri}")
            
            # Check processing status
            while uploaded_video.state.name == "PROCESSING":
                status.write("Processing video...")
                time.sleep(10)
                uploaded_video = genai.get_file(uploaded_video.name)
            
            if uploaded_video.state.name == "FAILED":
                raise ValueError(f"Video processing failed: {uploaded_video.state.name}")
            
            status.write("Video processing completed!")
        
        # Clean up temporary file
        os.unlink(video_path)
        
        return uploaded_video
    
    except Exception as e:
        st.error(f"Error processing video: {str(e)}")
        return None

def save_conversation():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conversation_{timestamp}.json"
    data = {
        "messages": st.session_state.messages,
        "system_prompt": st.session_state.system_prompt,
        "selected_model": st.session_state.selected_model,
        "temperature": st.session_state.temperature  # Save temperature setting too
    }
    with open(filename, "w") as f:
        json.dump(data, f)
    return filename

def load_conversation(file):
    try:
        content = file.read()
        data = json.loads(content)
        st.session_state.messages = data["messages"]
        st.session_state.system_prompt = data.get("system_prompt", "")
        st.session_state.selected_model = data.get("selected_model", "gemini-exp-1206")
        st.session_state.temperature = data.get("temperature", 0.7)  # Load temperature setting
        create_chat()
        return True
    except Exception as e:
        st.error(f"Error loading conversation: {str(e)}")
        return False

def display_message(message, idx):
    """Display a chat message with styling."""
    role = message["role"]
    content = message["content"]
    timestamp = message.get("timestamp", "")
    
    # Create columns for better message alignment
    if role == "user":
        _, message_col = st.columns([1, 5])
    else:
        message_col, _ = st.columns([5, 1])
    
    with message_col:
        st.container()
        st.markdown(
            f"""
            <div class="chat-message {role}-message">
                <div class="message-content">{content}</div>
                <div class="message-timestamp">{timestamp}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

def main():
    st.set_page_config(
        page_title="Gemini Chat Interface",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize CSS
    local_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Main title and instructions
    st.title("💬 Chat with Gemini")
    st.markdown(
        'In order to use the app you will need to go to '
        '<a href="https://aistudio.google.com/" target="_blank">Google Cloud Studio</a>'
        ' and login with your gmail account and click on Get API Key and paste the API key into the API Configuration field to the left.',
        unsafe_allow_html=True
    )
    # Add this new section for feature explanations
    st.markdown("""
    ### Features:
    * **🔑 API Configuration**: Paste your API key here and press enter
    * **🤖 Model Selection**: Choose the Gemini model you want to use
    * **🌡️ Temperature**: How creative (higher) or analytical (lower) you want the model to behave
    * **⚙️ System Prompt**: Any special instructions for the model
    * **💾 Chat Management**: Erasing, saving, or loading chats
    """)
    st.markdown("---")
    
    # Sidebar configuration
    with st.sidebar:
        st.title("💬 Chat Settings")
        
        with st.expander("🔑 API Configuration", expanded=True):
            api_key = st.text_input("Enter your Gemini API key:", type="password")
            if api_key:
                st.session_state.api_key = api_key
                if st.session_state.chat is None:
                    create_chat()
        
        with st.expander("🤖 Model Selection", expanded=True):
            selected_model = st.selectbox(
                "Choose Gemini Model:",
                options=["gemini-exp-1206", "gemini-2.0-flash-exp"],
                help="Select which Gemini model to use for chat"
            )
            
            temperature = st.slider(
                "Temperature:",
                min_value=0.0,
                max_value=1.0,
                value=st.session_state.temperature,
                step=0.1,
                help="Lower values make responses more focused and deterministic. Higher values make responses more creative and varied."
            )
            
            if (selected_model != st.session_state.selected_model or 
                temperature != st.session_state.temperature):
                st.session_state.selected_model = selected_model
                st.session_state.temperature = temperature
                st.session_state.messages = []  # Clear messages when settings change
                create_chat()
                st.rerun()
        
        with st.expander("⚙️ System Settings", expanded=True):
            new_system_prompt = st.text_area(
                "System Prompt:",
                value=st.session_state.system_prompt,
                height=100
            )
            if new_system_prompt != st.session_state.system_prompt:
                st.session_state.system_prompt = new_system_prompt
                st.session_state.messages = []
                create_chat()
        
        with st.expander("💾 Chat Management", expanded=True):
            if st.button("Clear Chat", type="secondary"):
                st.session_state.messages = []
                create_chat()
                st.rerun()
            
            if st.button("Save Chat"):
                filename = save_conversation()
                st.success(f"Saved as {filename}")
            
            uploaded_file = st.file_uploader("Load Chat", type="json")
            if uploaded_file is not None:
                if load_conversation(uploaded_file):
                    st.success("Chat loaded successfully!")
                    st.rerun()
    
    # Display chat messages
    for idx, message in enumerate(st.session_state.messages):
        display_message(message, idx)
    
    # Chat input area
    with st.container():
        st.markdown("---")
        
        # Text input at the top
        user_input = st.text_input("Message Gemini...", key="user_input")
        
        # Media upload tabs
        tab1, tab2 = st.tabs(["📎 Upload Media", "👁️ Media Preview"])
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                uploaded_image = st.file_uploader("📷 Upload Image", type=["jpg", "jpeg", "png"])
            with col2:
                uploaded_video = st.file_uploader(
                    "🎥 Upload Video",
                    type=["mp4", "mpeg", "mpg", "mov", "avi", "flv", "webm", "wmv", "3gpp"],
                    help="Supported formats: MP4, MPEG, MOV, AVI, FLV, WebM, WMV, 3GPP"
                )
        
        with tab2:
            if uploaded_image:
                st.image(uploaded_image, caption="Image Preview", use_container_width=False, width=300)
            if uploaded_video:
                st.video(uploaded_video)
        
        send_button = st.button("Send 📤", use_container_width=True)
    
    if send_button and (user_input or uploaded_image or uploaded_video):
        if not st.session_state.api_key:
            st.error("Please enter your API key in the sidebar.")
            return
        
        try:
            timestamp = datetime.now().strftime("%I:%M %p")
            
            # Determine content type for display
            if uploaded_video:
                display_content = f"{user_input}\n[Video attached]" if user_input else "[Video attached]"
            elif uploaded_image:
                display_content = f"{user_input}\n[Image attached]" if user_input else "[Image attached]"
            else:
                display_content = user_input
            
            st.session_state.messages.append({
                "role": "user",
                "content": display_content,
                "timestamp": timestamp
            })
            
            with st.spinner("Gemini is thinking... 🤔"):
                if uploaded_video:
                    # Handle video with same pattern as images
                    processed_video = process_video(uploaded_video)
                    if processed_video:
                        video_model = genai.GenerativeModel(
                            "gemini-1.5-pro",
                            generation_config={"temperature": st.session_state.temperature}
                        )
                        response = video_model.generate_content(
                            [processed_video, user_input or "Describe this video."]
                        )
                        # Use same response handling as images
                        response_text = response.parts[0].text if hasattr(response, 'parts') else response.text
                    else:
                        response_text = "Error processing video."
                else:
                    # Use the original working response handling for text and images
                    if uploaded_image:
                        img = Image.open(uploaded_image)
                        response = st.session_state.chat.send_message([user_input or "Describe this image.", img], stream=False)
                    else:
                        if len(st.session_state.messages) == 1:
                            user_input = f"{st.session_state.system_prompt}\n\nUser: {user_input}"
                        response = st.session_state.chat.send_message(user_input, stream=False)
                    
                    response_text = response.parts[0].text if hasattr(response, 'parts') else response.text
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text,
                    "timestamp": datetime.now().strftime("%I:%M %p")
                })
                
            if uploaded_image or uploaded_video:
                st.rerun()
            
        except Exception as e:
            st.error(f"Error details: {type(e).__name__}")
            st.error(f"Error message: {str(e)}")

if __name__ == "__main__":
    main()