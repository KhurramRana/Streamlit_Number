import os
import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

st.title("Chat with CSV")

st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your API Key")

if api_key:
    llm = OpenAI(api_token=api_key)
    uploaded_file = st.file_uploader("Upload a csv file to analysis", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df.head(5))

        prompt = st.text_area("Enter Your Question:")

        generate = st.button("Generate")

        if generate:
            if prompt:
                with st.spinner("AI is generating an answer, please wait..."):
                    df = SmartDataframe(df, config={"llm": llm})
                    response = df.chat(prompt)

                    if isinstance(response, (str, int, float)):
                        if isinstance(response, str) and response.endswith('.png') and os.path.exists(response):
                            st.image(response, caption="Generated Chart")
                        else:
                            st.write(response)
                    else:
                        st.write("Unexpected response type:", type(response))
            else:
                st.warning("Please upload a csv file and enter your prompt")
else:
    st.sidebar.warning("Please enter your API Key")