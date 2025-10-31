import streamlit as st 
from story_narrator import generate_story, generate_transcription
from PIL import Image


st.title("AI Multimodel Vision Narrator")
st.markdown("Upload images choose style and the let the AI narrate or write the story for you.")

styles = ["Comedy","Thriller", "Sci-Fi", "Mystery", "Adventure", "Moral"]

with st.sidebar:
    st.title("Controls")
    upload_files = st.file_uploader("Upload your Images",type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    story = st.selectbox("Choose a Story Style:",styles)
    generate_button = st.button("Generate the Story", type="primary") 



#main logic

if generate_button:
    if not upload_files:
        st.warning("Please upload atleast 1 Image")
    elif len(upload_files)>10:
        st.warning("Please upload maximum 10 Images")
    else:
        with st.spinner("The AI is generating the story and its Narration...This may take few moments..."):
            try:
                pil_image = [Image.open(i) for i in upload_files]
                st.subheader("Your Visual Inspiration")
                image_col = st.columns(len(pil_image))
                for i, image in enumerate(pil_image):
                    with image_col[i]:
                        resized = image.resize((300,200))
                        st.image(resized, use_container_width=True)
                
                st.subheader(f"Your {story} Story:")
                response = generate_story(pil_image,story)

                if "Error" in response or  "failed" in response or "API key" in response:
                    st.error(response)
                else:
                    st.success(response)

                st.subheader("Listen to your Story")
                audio_trans = generate_transcription(response)
                if audio_trans:
                    st.audio(audio_trans, format="audio/mp3")
                


            except Exception as e:
                st.error(e)
        