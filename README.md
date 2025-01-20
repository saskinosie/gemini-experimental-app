# gemini-experimental-app


# Gemini Chat Interface

## Overview
The Gemini Chat Interface is a Streamlit application that allows users to interact with Google's Gemini Generative AI running both gemini-exp-1206 and gemini-2.0-flash-exp models. The app supports:

- Customizable system prompts for tailored AI behavior.
- Uploading and processing of media files (images and videos).
- Chatting with a selected model using adjustable creativity levels (temperature settings).
- Saving and loading conversations for later use.

This README provides an overview of the app's features, installation instructions, and usage details.

---

## Features

### Chat with Gemini
- **Interactive Conversations**: Users can type messages and receive responses from the selected Gemini model.
- **Custom Styling**: Messages are displayed in a visually appealing format with user/assistant-specific styles.

### Media Upload and Processing
- **Image Support**: Upload images and have the model provide descriptions or context.
- **Video Support**: Upload videos for processing, with progress tracked in real-time.

### Customization
- **System Prompt**: Modify the behavior of the AI by providing specific instructions.
- **Model Selection**: Choose between available Gemini models.
- **Temperature Control**: Adjust the creativity of responses from highly analytical to more imaginative.

### Chat Management
- **Save Conversations**: Export chat histories in JSON format for future reference.
- **Load Conversations**: Import previous chat files to continue discussions.
- **Clear Chats**: Reset the conversation to start fresh.

---

## Installation

### Prerequisites
- Python 3.8+
- API key for Google Generative AI (available from [Google Cloud Studio](https://aistudio.google.com/)).

### Required Libraries
Install the dependencies with:
```bash
pip install streamlit google-generativeai pillow
```

---

## How to Run the Application

1. Clone the repository or download the source code.
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. Open the app in your browser at `http://localhost:8501` (or the port specified in the terminal).

---

## Usage

### Sidebar Settings
1. **API Key**: Enter your Google Gemini API key to authenticate.
2. **Model Selection**: Choose the Gemini model to use.
3. **Temperature**: Adjust the model's response creativity.
4. **System Prompt**: Provide specific instructions to guide the model's responses.
5. **Chat Management**: Save, load, or clear chat histories.

### Main Interface
1. **Chat Input**: Type your message in the text box.
2. **Media Upload**: Upload images or videos to interact with the model.
3. **Message Display**: View the chat history with timestamps and AI responses.

---

## File Structure
- `app.py`: Main Streamlit application.
- `requirements.txt`: List of required libraries.

---

## Known Issues
- Video processing may take longer depending on file size and model availability.
- Ensure the API key is valid; otherwise, the app will not function correctly.

---

## Future Enhancements
- Add support for additional file formats.
- Include advanced analytics for chat responses.
- Optimize performance for large media files.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgments
- [Streamlit](https://streamlit.io/) for the framework.
- [Google Generative AI](https://aistudio.google.com/) for the API support.
- Icons from [Emoji One](https://emojione.com/).

