import streamlit as st 
import mimetypes   
import openai 
from pydub import AudioSegment
import tempfile 
import ast

import prompts  
import gpt

openai.api_key = st.secrets['OPENAI_API_KEY'] 

def blank(): return st.text('')

def check_file_type(file):
    file_type, encoding = mimetypes.guess_type(file.name)
    return file_type  

def whisper_transcribe(file, prompt=prompts.whisper_prompt): 
    transcription = openai.Audio.transcribe("whisper-1", file, prompt=prompt) 
    return transcription 

def convert_to_wav(file):
    # Create temporary wav file
    tmp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    # Load audio file
    audio = AudioSegment.from_mp3(file)
    # Save as wav
    audio.export(tmp_wav.name, format="wav")
    return tmp_wav.name  


st.set_page_config(layout="wide")  

password = st.sidebar.text_input("Password")  
if password.lower().strip() == st.secrets['PASSWORD']: 
    valid_user = True 
else: 
    valid_user = False


st.subheader("AI Call Parsing") 
if valid_user: 
    st.success("password accepted") 
else: 
    st.warning("invalid password") 

blank()  



with st.form(key='f'):   

    upload_type = st.selectbox("Input Type", ['File Upload', "Transcription Pasted"])

    with st.expander("File Upload"):
        audio_upload = st.file_uploader("Upload Call") 
    with st.expander("Transcription"): 
        text_upload = st.text_area("Paste transcription here") 

    p = st.text_area("GPT Instructions", value=prompts.base)

    go = st.form_submit_button("Go") 

if go:   
    if valid_user:
        if upload_type == 'File Upload': 
            upload = audio_upload

            ftype = check_file_type(upload) 
            st.write(f"File type: **{ftype}**")  
            st.audio(upload)

            # Convert to wav
            if ftype == 'audio/mpeg':
                with st.spinner("Converting to wav"):
                    wav_file = convert_to_wav(upload) 
                    st.success("converted to .wav")

                with st.spinner("Transcribing"): 
                    trans = whisper_transcribe(wav_file)   
            else:  
                with st.spinner("Transcribing"): 
                    trans = whisper_transcribe(upload) 
        else:  
            upload = text_upload 

            trans = {'text': upload} 

        with st.expander("Transcription"): 
            trans = trans.get('text', '')
            st.write(trans.replace("$", "\\$")) 

        with st.spinner("Pulling Data"): 
            bot = gpt.ai(None, system_prompt=p) 
            res = bot.answer(trans)  
            try:
                res = ast.literal_eval(res)  
                st.json(res)
            except: 
                st.write(res)  
    else: 
        st.warning("Please input valid passowrd in the sidebar")

