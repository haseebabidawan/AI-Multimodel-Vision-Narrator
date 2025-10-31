from dotenv import load_dotenv
from google import genai
from google.genai import types
import base64
from gtts import gTTS
from io import BytesIO

import wave


import os



load_dotenv()


api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API Key not Found")


client = genai.Client(api_key= api_key)


def create_advanced_prompt(style):
       # --- Base prompt ---
    base_prompt = f"""
    **Your Persona:** You are a friendly and engaging storyteller. Your goal is to tell a story that is fun and easy to read.
    **Your Main Goal:** Write a story in simple, clear, and modern English.
    **Your Task:** Create one single story that connects all the provided images in order.
    **Style Requirement:** The story must fit the '{style}' genre.
    **Core Instructions:**
    1.  **Tell One Single Story:** Connect all images into a narrative with a beginning, middle, and end.
    2.  **Use Every Image:** Include a key detail from each image.
    3.  **Creative Interpretation:** Infer the relationships between the images.
    4.  **Nationality**: Use only Indian Names,Characters, Places , Persona Etc.
    **Output Format:**
    -   **Title:** Start with a simple and clear title.
    -   **Length:** The story must be between 4 and 5 paragraphs.
    """

    # --- Add Style-Specific Instructions ---
    style_instruction = ""
    if style == "Moral":
        style_instruction = "\n**Special Section:** After the story, you MUST add a section starting with the exact tag `[MORAL]:` followed by the single-sentence moral of the story."
    elif style == "Mystery":
        style_instruction = "\n**Special Section:** After the story, you MUST add a section starting with the exact tag `[SOLUTION]:` that reveals the culprit and the key clue."
    elif style == "Thriller":
        style_instruction = "\n**Special Section:** After the story, you MUST add a section starting with the exact tag `[TWIST]:` that reveals a final, shocking twist."

    return base_prompt + style_instruction



def generate_story(images,style):
    
    response = client.models.generate_content(
    model = "gemini-2.5-flash-lite",
    contents = [images, create_advanced_prompt(style)]
    )

    return response.text



def generate_transcription(text):
    try: 
        tts = gTTS(text = text, lang="en", slow = False)
        audio_fp = BytesIO() # TEmporary storage of File
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)     #always start the audio form the begining
        return audio_fp

    except Exception as e:
        return f"An error occured {e}"

