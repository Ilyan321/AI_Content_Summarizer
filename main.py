import streamlit as st
import requests
from openai import OpenAI
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()
client= OpenAI()
api_key = os.getenv("OPENAI_API_KEY")


# article colletinga nd scraping paragraphs
def fetch_Article(url):
    try:
        header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response=requests.get(url,headers=header)

        if response.status_code==404:
            return None, "404 error. Article does not exists"
        
        response.raise_for_status()    # to check error

        soup=BeautifulSoup(response.text,"html.parser")
        paragraphs=soup.find_all('p')
        content=" ".join([p.get_text() for p in paragraphs])

        if not content.strip():
            return None, "Pages loaded but no paragraphs found"
        
        return content,"Success"

    except Exception as e:
        print("Extracting Error")

# Openai integration 

def summarize_and_translate(text,target_language,summary_length):
    prompt=("Please,summarize the following text in approximately "+str(summary_length)+" sentences."+" Then translate the summary into "+str(target_language)+"\n\n"+" Text: "+text[:4000])

    try:
        response=client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role":"system","content":"You are highly skilled summarizer and translator"},
                {"role":"user","content":prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("An AI errpr occured."+str(e))


# UI design with streamlit
st.title("AI Content Summarizer and Translator")
st.sidebar.header("Settings")
target_lang=st.sidebar.selectbox("Choose Output language: ",["English","Spanish","German","Urdu","French","Sindhi","Japanese"])
length_slider=st.sidebar.slider("Length of Summary (sentences): ",min_value=1,max_value=20,value=7)

url_input=st.text_input("Enter URL here")

if st.button("Analyze Content"):
    if url_input:
        with st.spinner("AI is analyzing Article..."):
            text,status=fetch_Article(url_input)
        if text:
            with st.spinner("AI is summarizing and translating..."):
                final_output=summarize_and_translate(text,target_lang,length_slider)

            st.success("Done!")
            st.write("Review your summary: ")
            st.info(final_output)
        else:
            st.error(status)
    else:
        st.warning("Please Enter the URL.")


