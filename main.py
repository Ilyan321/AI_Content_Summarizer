import streamlit as st
import requests
from groq import Groq 
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
client= Groq(api_key=my_api_key)



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
        st.error("Extracting Error")

# Openai integration 

def summarize_and_translate(text,target_language,summary_length):
    prompt = (
        "Analyze the following text.\n"+
        "Write a summary that contains EXACTLY "+str(summary_length-3)+" sentences. Not one sentence more, and not one sentence less. Count your sentences carefully.\n"+
        "The entire text MUST be written exclusively in "+str(target_language)+". Do NOT write a single word of English or any other language.\n"+
        "Do NOT include conversational filler like 'Here is the summary'. Output ONLY the final "+str(target_language)+" text.\n\n"+
        "Text to summarize:\n"+text[:4000] )

    try:
        response=client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role":"system","content":"You are highly skilled summarizer and translator"},
                {"role":"user","content":prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        st.error("An AI errpr occured."+str(e))


# UI design with streamlit
st.set_page_config(page_title="AI Content Summarizer and Translator",page_icon="🗣️")

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


