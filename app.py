import streamlit as st
import pytesseract
from PIL import Image
from gtts import gTTS
import openai

st.title("📄🔊 IA que Explica Contas com Voz")

if 'openai_key' not in st.session_state:
    st.session_state.openai_key = ""

if not st.session_state.openai_key:
    st.info("Para começar, insira sua chave da OpenAI (API Key).")
    key_input = st.text_input("Chave da OpenAI:", type="password")
    if key_input:
        st.session_state.openai_key = key_input
        st.experimental_rerun()
else:
    openai.api_key = st.session_state.openai_key

    uploaded_file = st.file_uploader("Envie uma conta ou boleto (imagem)", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagem recebida", use_column_width=True)

        with st.spinner("Lendo a imagem..."):
            texto_extraido = pytesseract.image_to_string(image, lang='por')

        st.subheader("Texto Detectado:")
        st.write(texto_extraido)

        with st.spinner("Gerando explicação..."):
            prompt = f"Explique em linguagem simples o conteúdo dessa conta:\n\n{texto_extraido}"
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            explicacao = response["choices"][0]["message"]["content"]

        st.subheader("Explicação da Conta:")
        st.write(explicacao)

        with st.spinner("Convertendo para voz..."):
            tts = gTTS(text=explicacao, lang='pt-br')
            audio_path = "explicacao.mp3"
            tts.save(audio_path)
            st.audio(audio_path, format="audio/mp3")
