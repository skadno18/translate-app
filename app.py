import streamlit as st
from gtts import gTTS
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Set your Gemini API key
API_KEY = "AIzaSyCjfeJXVm6IdKn34sBsZ0waccc26j9sw9o"

# Set up Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=API_KEY
)

# Streamlit UI
st.set_page_config(page_title="SKAD Translator", page_icon="🌍")

st.title("SKAD Translator")
st.write("Translate any sentence into your preferred language and hear it spoken aloud!")

# Text inputs
query = st.text_input("Enter the text to translate:")
language = st.text_input("Enter target language to translate:")

# Translate on button click
if st.button("Translate and Speak"):
    if not query or not language:
        st.warning("Please enter both text and target language.")
    else:
        prompt = f"""
        You are a helpful assistant that translates text into a specific language.

        Translate this to the provided language:
        {query}

        Only provide the translated script without any additional text or explanation.
        Translate this to {language} language.
        """

        with st.spinner("Translating..."):
            try:
                response = llm.invoke(prompt)
                translated_text = response.content.strip()

                st.success("Translation:")
                st.markdown(f"**{translated_text}**")

                # Convert to speech
                with st.spinner("Generating speech..."):
                    # Map common language names to language codes
                    lang_codes = {
                        "tamil": "ta",
                        "english": "en",
                        "hindi": "hi",
                        "telugu": "te",
                        "kannada": "kn",
                        "malayalam": "ml",
                        "french": "fr",
                        "german": "de",
                        "spanish": "es"
                    }

                    lang_code = lang_codes.get(language.lower(), "en")  # default to English
                    tts = gTTS(text=translated_text, lang=lang_code)
                    tts.save("output.mp3")

                    # Play the audio
                    audio_file = open("output.mp3", "rb")
                    st.audio(audio_file.read(), format="audio/mp3")

            except Exception as e:
                st.error(f"Error: {str(e)}")
