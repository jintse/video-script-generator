import streamlit as st
from utils import generate_script

st.title("😆Video Script generator")

with st.sidebar:
    openai_api_key = st.text_input("Enter OpenAI API password: ", type="password")
    st.markdown("[get OpenAI API password](https://openai.com/index/openai-api/)")

subject = st.text_input("Enter the subject of the video")
language = st.text_input("Enter the language of the video")
video_length = st.number_input("Enter the video length (unit: minute)", value=1.0, min_value=0.1, step=0.1)
creativity = st.slider("Enter the creativity of the video (smaller->more valid, larger->more variety)", min_value=0.1, max_value=1.0, value=0.2, step=0.1)

submitted = st.button("Generate script")

if submitted and not openai_api_key:
    st.info("please enter your OpenAI API")
    st.stop()
if submitted and not subject:
    st.info("please enter the subject")
    st.stop()
if submitted and not video_length>=0.1:
    st.info("video length should larger or equal to 0.1 minutes")
    st.stop()
if submitted and not language:
    st.info("please enter the language of the video")
    st.stop()
if submitted:
    with st.spinner("AI is thinking, please wait..."):
        search_result, title, script = generate_script(subject, video_length, creativity, language, openai_api_key)
    st.success("the script is generated!")
    st.subheader("Title: " )
    st.write(title)
    st.subheader("Script")
    st.write(script)
    with st.expander("Wikipedia search result: "):
        st.info(search_result)
